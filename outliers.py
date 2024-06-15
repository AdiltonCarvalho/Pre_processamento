import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# Função para identificar e ajustar outliers
def detectar_e_ajustar_outliers(df_sem_nulos):

    st.markdown('---')
    st.write("### Remoção de outliers")
    st.write("Nessa etapa são analisados os outliers em colunas com dados numéricos que possam influenciar o resultado. Foi utilizado o Método do IQR (Intervalo Interquartil) que identifica outliers como dados que estão fora de 1,5 vezes o intervalo interquartil (a distância entre o terceiro e o primeiro quartil) acima do terceiro quartil ou abaixo do primeiro quartil.")
    st.markdown('---')

    def detectar_outliers(coluna):
        q1 = coluna.quantile(0.25)
        q3 = coluna.quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        outliers = (coluna < limite_inferior) | (coluna > limite_superior)
        return outliers

    # Pipeline para identificar e ajustar outliers
    pipeline_outliers = Pipeline([
        ('outliers', FunctionTransformer(detectar_outliers)),
        ('imputer', SimpleImputer(strategy='mean'))  # Substituir outliers pela média
    ])

    # Aplicar o pipeline para cada coluna numérica e contar outliers ajustados
    outliers_ajustados_por_coluna = {}
    df_sem_nulos = df_sem_nulos.drop(['index'], axis=1)
    colunas_numericas = [coluna for coluna in df_sem_nulos.columns if df_sem_nulos[coluna].dtype in ['float64', 'int64']]

    # Gerar gráficos de boxplot para cada coluna numérica
    for coluna in colunas_numericas:
        outliers = pipeline_outliers.fit_transform(df_sem_nulos[[coluna]])
        outliers_ajustados = outliers.sum()
        outliers_ajustados_por_coluna[coluna] = outliers_ajustados

    # Converter o resultado para DataFrame
    df_outliers_ajustados = pd.DataFrame.from_dict(outliers_ajustados_por_coluna, orient='index', columns=['Outliers Ajustados'])
    df_outliers_ajustados.reset_index(inplace=True)
    df_outliers_ajustados.rename(columns={'index': 'Coluna'}, inplace=True)

    # Filtrar colunas com 0 outliers ajustados
    df_outliers_ajustados = df_outliers_ajustados[df_outliers_ajustados['Outliers Ajustados'] > 0]

    # Ordenar em ordem decrescente
    df_outliers_ajustados = df_outliers_ajustados.sort_values(by='Outliers Ajustados', ascending=True)

    # Configurando a aplicação em colunas
    col1,col2 = st.columns(2)

    # Converter Outliers Ajustados para string
    df_outliers_ajustados['Outliers Ajustados'] = df_outliers_ajustados['Outliers Ajustados'].astype(int).astype(str)

    # Exibir o DataFrame com a quantidade de outliers ajustados por coluna
    col1.write("Quantidade de outliers ajustados por coluna")
    col1.table(df_outliers_ajustados)

    # Criar colunas para os gráficos de boxplot
    boxplot_cols = st.columns(4)

    # Gerar gráficos de boxplot para cada coluna numérica com outliers ajustados
    for idx, (i, row) in enumerate(df_outliers_ajustados.iterrows()):
        coluna = row['Coluna']
        fig_box = px.box(df_sem_nulos, y=coluna, title=f'{coluna}')
        fig_box.update_layout(yaxis_title='')
        boxplot_cols[idx % 4].plotly_chart(fig_box)