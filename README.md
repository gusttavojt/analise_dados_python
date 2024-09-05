# Análise de Dados com Flask

Este é um projeto de aplicação web usando Flask para análise de dados, e SQLite para banco de dados. A aplicação permite o upload de arquivos Excel, e realiza análises e exibe resultados gráficos.

## Funcionalidades

- Upload de arquivos Excel.
- Análise de dados dos arquivos enviados.
- Geração de gráficos de correlação, histograma, boxplot e gráfico de regressão.
- Visualização em formato png.

## Estrutura do Projeto

- `app.py`: Código principal do aplicativo Flask.
- `requirements.txt`: Lista de dependências do projeto.
- `templates/`: Contém arquivos de template HTML e Bootstrap para a interface do usuário.
- `static/`: Diretório para arquivos estáticos como imagens.
- `uploads/`: Diretório onde os arquivos enviados são armazenados.



## Instalação

1. Clone o repositório:

   ```bash

   git clone https://github.com/gusttavojt/analise_dados_python.git

2. Navegue até o diretório do projeto:
   
   ```bash

   cd analise_dados_python

3. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
 No Windows: 
    
      python -m venv venv
      venv\Scripts\activate

4. Instale as dependências:
  
   ```bash

   pip install -r requirements.txt

## Uso
 
  ```bash

  python app.py
