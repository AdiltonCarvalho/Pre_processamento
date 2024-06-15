import pandas as pd
import numpy as np
import streamlit as st
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from io import StringIO

# Função para identificar colunas com nulos
def identificar_colunas_com_nulos(data):
    colunas_com_nulos = data.columns[data.isnull().any()]
    tipos_de_dados_nulos = data[colunas_com_nulos].dtypes
    colunas_numericas = [col for col in colunas_com_nulos if tipos_de_dados_nulos[col] in ['float64', 'int64']]
    colunas_categoricas = [col for col in colunas_com_nulos if tipos_de_dados_nulos[col] == 'object']
    return colunas_numericas, colunas_categoricas

# Função para testar estratégias de substituição
def testar_estrategia_de_imputacao(estrategia, X, colunas):
    imputador = SimpleImputer(strategy=estrategia)
    X_imputado = imputador.fit_transform(X[colunas])
    if X_imputado.ndim == 1:
        X_imputado = X_imputado.reshape(-1, 1)
    return X_imputado, imputador.statistics_

# Função para encontrar a melhor estratégia de imputação de dados
def encontrar_melhor_estrategia(data, colunas_numericas, colunas_categoricas):
    estrategias = ['mean', 'median', 'most_frequent']
    pontuacao_estrategias = {}
    
    for coluna in colunas_numericas:
        scores = {}
        for estrategia in estrategias:
            X_imputado, _ = testar_estrategia_de_imputacao(estrategia, data, [coluna])
            score = np.mean(X_imputado)
            scores[estrategia] = score
        melhor_estrategia = max(scores, key=scores.get)
        pontuacao_estrategias[coluna] = {
            'tipo': 'numérico',
            'scores': scores,
            'melhor_estrategia': melhor_estrategia
        }

    for coluna in colunas_categoricas:
        scores = {}
        for estrategia in ['most_frequent']:
            X_imputado, _ = testar_estrategia_de_imputacao(estrategia, data, [coluna])
            score = pd.Series(X_imputado.flatten()).value_counts().max()
            scores[estrategia] = score
        melhor_estrategia = max(scores, key=scores.get)
        pontuacao_estrategias[coluna] = {
            'tipo': 'categórico',
            'scores': scores,
            'melhor_estrategia': melhor_estrategia
        }
    
    return pontuacao_estrategias

# Função para criar e aplicar o ColumnTransformer
def aplicar_transformacoes(data, resultados):
    transformers = [(col, SimpleImputer(strategy=resultados[col]['melhor_estrategia']), [col]) for col in resultados]
    column_transformer = ColumnTransformer(transformers, remainder='passthrough')
    df_sem_nulos = column_transformer.fit_transform(data)
    df_sem_nulos = pd.DataFrame(df_sem_nulos, columns=['tempo_emprego','data_ref','index','sexo','posse_de_veiculo','posse_de_imovel','qtd_filhos',
                                                  'tipo_renda','educacao','estado_civil','tipo_residencia','idade','qt_pessoas_residencia',
                                                   'renda','mau'])
    df_sem_nulos = df_sem_nulos.reindex(columns=['data_ref','index','sexo','posse_de_veiculo','posse_de_imovel','qtd_filhos','tipo_renda',
                                             'educacao','estado_civil','tipo_residencia','idade','tempo_emprego','qt_pessoas_residencia',
                                             'renda', 'mau'])

    # Manter tipos originais
    type_mapping = data.dtypes.to_dict()
    for column, dtype in type_mapping.items():
        df_sem_nulos[column] = df_sem_nulos[column].astype(dtype)
    
    return df_sem_nulos

# Função para mostrar os resultados das estratégias de imputação de dados.
def mostrar_resultados(resultado_pontuacao_estrategia):

    st.write("### Substituição de dados nulos")
    st.write("Nessa etapa são analisadas as colunas com dados nulos e seus tipos de dados. A análise contempla o teste de estratégias média e mediana para inserir dados nas colunas com dados faltantes do tipo numérico e a estratégia valor mais frequente para colunas com dados categóricos. Seguem os resultados das estratégias de imputação de dados para colunas com dados nulos.")
    st.markdown('---')

    # Dicionário de tradução das estratégias
    traducao_estrategias = {
        "mean": "Média",
        "median": "Mediana",
        "most_frequent": "Valor mais frequênte"
    }
    
    for coluna, resultado in resultado_pontuacao_estrategia.items():
        st.write(f"Colunas com dados nulos: {coluna}")
        st.write(f"Tipo de dado           : {resultado['tipo']}")
        st.write("Scores de cada estratégia para complementar os dados nulos")

        for estrategia, score in resultado['scores'].items():
            # Verifica se a estratégia está no dicionário de tradução
            estrategia_traduzida = traducao_estrategias.get(estrategia, estrategia)
            st.write(f"{estrategia_traduzida}: {round(score, 2)}")

# Função para gerar a estrrutura do dataframe antes e após a substituição de dados nulos
def gerar_info_dataframe(data, df_sem_nulos):
    # Função para capturar informações do DataFrame
    def capturar_info_dataframe(df):
        buffer = StringIO()
        df.info(buf=buffer)
        saida_info = buffer.getvalue()
        # Processando a string capturada para extrair as informações desejadas
        linhas_info = saida_info.split('\n')[5:-3]  # Ignorando as 5 primeiras e as 3 últimas linhas
        dados_info = []
        for linha in linhas_info:
            partes = linha.split()
            coluna = partes[1]
            contagem_nao_nulos = partes[2]
            contagem_nulos = str(df.shape[0] - int(contagem_nao_nulos))
            tipo_dado = partes[-1]
            dados_info.append({'Colunas': coluna, 'Contagem de não nulos': contagem_nao_nulos, 'Contagem de nulos': contagem_nulos, 'Tipo de dado': tipo_dado})
        # Convertendo para DataFrame
        return pd.DataFrame(dados_info)

    # Obtendo as informações do DataFrame original
    info_df = capturar_info_dataframe(data)
    # Obtendo as informações do DataFrame sem nulos
    info_df_sem_nulos = capturar_info_dataframe(df_sem_nulos)

    # Configurando a aplicação em colunas
    col1, col2 = st.columns(2)

    # Exibindo os DataFrames com as informações
    col1.write("Informações do DataFrame antes da substituição de nulos")
    col1.table(info_df)
    col2.write("Informações do DataFrame após a substituição de nulos")
    col2.table(info_df_sem_nulos)