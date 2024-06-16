# README

# Aplicação Web de Análise de Dados e Machine Learning

Esta é uma aplicação web construída utilizando Streamlit que permite aos usuários carregar um conjunto de dados, realizar análise exploratória de dados (EDA), pré-processar os dados, detectar e ajustar outliers, lidar com valores ausentes e executar experimentos de machine learning.

# Visão Geral da Aplicação

## Funcionalidades

- **Upload de Dados**: Carregue um conjunto de dados a partir de uma URL (GitHub) ou de um arquivo local.
- **Análise Exploratória de Dados**: Gere um relatório abrangente de EDA utilizando Sweetviz.
- **Pré-processamento de Dados**: Identifique e trate valores ausentes, e detecte e ajuste outliers.
- **Experimentos de Machine Learning**: Execute experimentos de machine learning e exiba os resultados.

## Upload de Dados
Na barra lateral, você pode escolher o método para carregar seu conjunto de dados:

- **URL do GitHub**: Insira a URL https://raw.githubusercontent.com/AdiltonCarvalho/Pre_processamento/main/credit_scoring.csv.
- **Arquivo Local**: Baixe a base de dados credit_scoring.csv nesse reporitório e carregue na aplicação.

## Visualização dos Dados
Após carregar o conjunto de dados, a aplicação exibe os dados em formato de tabela.

## Análise Exploratória de Dados
O relatório de EDA inclui uma análise detalhada e visualizações do conjunto de dados. Isso é feito utilizando o Sweetviz, e o relatório é exibido dentro da aplicação.

## Pré-processamento de Dados
As etapas de pré-processamento incluem:

- **Tratamento de Valores Ausentes**: Identificação de colunas com valores ausentes, encontrando a melhor estratégia de imputação e aplicando transformações.
- **Detecção e Ajuste de Outliers**: Detecção e ajuste de outliers no conjunto de dados.

## Experimento de Machine Learning
O experimento de machine learning inclui:

- Configuração do ambiente para o experimento.
- Execução do experimento para prever a probabilidade de um candidato ser classificado como 'mau' pagador de crédito.
- Exibição dos resultados do experimento e seleção do melhor modelo.

## Estrutura dos Arquivos
Os principais componentes da aplicação estão organizados da seguinte forma:

- **pre_processamento.py**: O script principal que executa a aplicação Streamlit.
- **botao_download.py**: Módulo para criação de links de download.
- **loader.py**: Módulo para carregar dados de uma URL ou arquivo e configurar a página.
- **eda.py**: Módulo para gerar relatórios de EDA utilizando Sweetviz.
- **outliers.py**: Módulo para detectar e ajustar outliers.
- **nulos.py**: Módulo para tratamento de valores ausentes.
- **experimento.py**: Módulo para execução de experimentos de machine learning.
- **treino.py**: Módulo para treinamento de modelos de machine learning.

## Dependências
As principais bibliotecas utilizadas neste projeto são:

- Streamlit
- Sweetviz
- PyCaret
- Pandas

Certifique-se de verificar o `requirements.txt` para a lista completa de dependências.

## Amostra
[ad962899-f693-4689-9eee-a735769aab5e.webm](https://github.com/AdiltonCarvalho/Pre_processamento/assets/141254502/c70881ed-dd64-4593-90fa-5b31e47114d7)

# Instalação e Execução da Aplicação Python

## Passo 1: Clonar o Repositório
git clone https://github.com/AdiltonCarvalho/Pre_processamento.git

## Passo 2: Navegar até o Diretório do Projeto
cd Pre_processamento

## Passo 3: Criar um Ambiente Virtual
python -m venv venv

## Passo 4: Ativar o Ambiente Virtual
- Windows:
  
  venv\Scripts\activate

- macOS e Linux:
  
  source venv/bin/activate

## Passo 5: Instalar as Dependências
pip install -r requirements.txt

## Passo 6: Executar a Aplicação
streamlit run app.py

## Passo 7: Acessar a Aplicação
Após executar o comando acima, a aplicação estará disponível em seu navegador padrão. Se necessário, você pode acessá-la manualmente através do endereço exibido no terminal, geralmente "http://localhost:8501".


