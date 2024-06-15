# Importar as biliotecas
import streamlit as st
import streamlit.components.v1 as components
from botao_download import download_button
from loader import load_data_from_url, load_data_from_file, configurar_pagina
from eda import eda_report_sweetviz
from outliers import detectar_e_ajustar_outliers
from treinamento import treina_modelo
from nulos import identificar_colunas_com_nulos, encontrar_melhor_estrategia, aplicar_transformacoes, mostrar_resultados, gerar_info_dataframe

# Função principal
def main():
    # Executa a função de configuração da página
    configurar_pagina()

    # Define um cabeçalho no formato HTML com alinhamento central e estilo de título h2
    st.markdown("<h2 style='text-align: center;'>Visualização da Base de Dados</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # Define o título da barra lateral   
    st.sidebar.title("Carregue a base de dados")

    # Adiciona um menu dropdown na barra lateral para selecionar o método de upload da base de dados  
    upload_method = st.sidebar.selectbox("Método de Upload", ("URL do GitHub", "Arquivo Local"))
    
    # Verifica se o método de upload selecionado é "URL do GitHub"
    if upload_method == "URL do GitHub":
        url = st.sidebar.text_input("Digite a URL do arquivo CSV no GitHub")
        
        # Adiciona um botão na barra lateral para carregar os dados
        if st.sidebar.button("Carregar Dados"):
            data = load_data_from_url(url)
            
            # Verifica se os dados foram carregados corretamente
            if data is not None:
                st.dataframe(data, use_container_width=True)
                st.markdown("---")
                
                # Define um cabeçalho no formato HTML com alinhamento central e estilo de título h2
                st.markdown("<h2 style='text-align: center;'>Análise Exploratória de Dados</h2>", unsafe_allow_html=True)
                st.markdown("---")

                # Inicializa a barra de progresso
                progress_bar = st.progress(0)
                progress_text = st.empty()
                
                report_html = eda_report_sweetviz(data, progress_text, progress_bar)
                components.html(report_html, height=800, scrolling=True)

                download_button(report_html)

            # Define um cabeçalho no formato HTML com alinhamento central e estilo de título h2
            st.markdown("<h2 style='text-align: center;'>Pré-Processamento de Dados</h2>", unsafe_allow_html=True)
            st.markdown("---")

            # Identifica colunas com nulos
            colunas_numericas, colunas_categoricas = identificar_colunas_com_nulos(data)

            # Encontra a melhor estratégia de imputação
            resultados = encontrar_melhor_estrategia(data, colunas_numericas, colunas_categoricas)

            # Aplica transformações
            df_sem_nulos = aplicar_transformacoes(data, resultados)

            # Mostra resultados de testes das estratégias
            mostrar_resultados(resultados)

            # Gera estrutura do dataframe antes e depois da substituição de dados nulos
            gerar_info_dataframe(data, df_sem_nulos)

            # Chama a função de detecção e ajuste de outiliers
            detectar_e_ajustar_outliers(df_sem_nulos)

            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>Experimento de Aprendizado de Máquina</h2>", unsafe_allow_html=True)

            # Amostra aleatoriamente 40.000 linhas do DataFrame df_sem_nulos
            dataset = df_sem_nulos.sample(20000)

            # Remove as colunas 'data_ref' e 'index' do DataFrame 'dataset'
            dataset.drop(['data_ref', 'index'], axis=1, inplace=True)

            # Chama a função para treinar o modelo
            treina_modelo(dataset)                       

    # Verifica se o método de upload selecionado é "Arquivo Local"        
    elif upload_method == "Arquivo Local":
        uploaded_file = st.sidebar.file_uploader("Carregue o arquivo CSV", type="csv")
       
        # Verifica se foi carregado o arquivo
        if uploaded_file is not None:          
            data = load_data_from_file(uploaded_file)
            
            # Verifica se os dados foram carregados corretamente
            if data is not None:
                st.dataframe(data, use_container_width=True)
                st.markdown("---")
                
                # Define um cabeçalho no formato HTML com alinhamento central e estilo de título h2
                st.markdown("<h2 style='text-align: center;'>Análise Exploratória de Dados</h2>", unsafe_allow_html=True)
                st.markdown("---")

                # Inicializa a barra de progresso
                progress_bar = st.progress(0)
                progress_text = st.empty()
                
                report_html = eda_report_sweetviz(data, progress_text, progress_bar)
                components.html(report_html, height=800, scrolling=True)

                download_button(report_html)
            
            # Define um cabeçalho no formato HTML com alinhamento central e estilo de título h2
            st.markdown("<h2 style='text-align: center;'>Pré-Processamento de Dados</h2>", unsafe_allow_html=True)
            st.markdown("---")

            # Identifica colunas com nulos
            colunas_numericas, colunas_categoricas = identificar_colunas_com_nulos(data)

            # Encontra a melhor estratégia de imputação
            resultados = encontrar_melhor_estrategia(data, colunas_numericas, colunas_categoricas)

            # Aplica transformações
            df_sem_nulos = aplicar_transformacoes(data, resultados)

            # Mostra resultados
            mostrar_resultados(resultados)

            # Gera estrutura do dataframe antes e depois da substituição de nulos
            gerar_info_dataframe(data, df_sem_nulos)

            # Chama a função e armazenar o resultado
            detectar_e_ajustar_outliers(df_sem_nulos)

            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>Experimento de Aprendizado de Máquina</h2>", unsafe_allow_html=True)

            # Chama a função para treinar o modelo
            treina_modelo(df_sem_nulos)

if __name__ == "__main__":
    main()