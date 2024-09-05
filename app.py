from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_analysis.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Modelo para armazenar análises
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    correlation_image = db.Column(db.String(150), nullable=False)


# Rota para a página inicial
@app.route('/')
def index():
    analyses = Analysis.query.all()
    return render_template('index.html', analyses=analyses)

# Rota para upload de arquivos e análise de dados
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Processar o arquivo
    data = pd.read_excel(file_path)
    analysis_result = analyze_data(data)

    # Salvar a análise no banco de dados
    new_analysis = Analysis(
        filename=file.filename,
        summary=analysis_result['summary'],
        correlation_image=analysis_result['correlation_image']
    )
    db.session.add(new_analysis)
    db.session.commit()

    return redirect(url_for('index'))

# Função de análise de dados
def analyze_data(data):
    correlation_matrix = data.corr()

    # Gerar gráfico de correlação
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    correlation_image = os.path.join('static', 'correlation.png')
    plt.savefig(correlation_image)
    plt.close()

    # Gerar outros gráficos
    histograms = generate_histogram(data)
    boxplots = generate_boxplot(data)
    regressions = generate_regression_plot(data, 'coluna1', 'coluna2')  # Ajuste 'coluna1' e 'coluna2'

    return {
        'correlation_image': 'correlation.png',
        'summary': data.describe().to_html(classes='table table-striped'),
        'histograms': histograms,
        'boxplots': boxplots,
        'regressions': regressions
    }

# Função para gerar histograma
def generate_histogram(data):
    histograms = []
    for column in data.select_dtypes(include=['float64', 'int64']):
        sns.histplot(data[column], kde=True)
        plt.title(f'Histograma de {column}')
        histogram_image = os.path.join('static', f'{column}_histogram.png')
        plt.savefig(histogram_image)
        plt.close()
        histograms.append(f'{column}_histogram.png')
    return histograms

# Função para gerar boxplot
def generate_boxplot(data):
    boxplots = []
    for column in data.select_dtypes(include=['float64', 'int64']):
        sns.boxplot(data[column])
        plt.title(f'Boxplot de {column}')
        boxplot_image = os.path.join('static', f'{column}_boxplot.png')
        plt.savefig(boxplot_image)
        plt.close()
        boxplots.append(f'{column}_boxplot.png')
    return boxplots

# Função para gerar gráfico de regressão
def generate_regression_plot(data, x_column, y_column):
    regressions = []
    sns.regplot(x=x_column, y=y_column, data=data)
    plt.title(f'Regressão Linear entre {x_column} e {y_column}')
    regression_image = os.path.join('static', f'{x_column}_vs_{y_column}_regression.png')
    plt.savefig(regression_image)
    plt.close()
    regressions.append(f'{x_column}_vs_{y_column}_regression.png')
    return regressions
if __name__ == '__main__':
    # Criar o contexto da aplicação para operações como criação de tabelas
    with app.app_context():
        db.create_all()  # Isso criará as tabelas no banco de dados se ainda não existirem

app.run(debug=True)