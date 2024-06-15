import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Função para carregar dados de uma URL
def load_data_from_url(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados da URL: {e}")
        return None

# Função para carregar dados de um arquivo
def load_data_from_file(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados do arquivo: {e}")
        return None

# Função para configurar a página    
def configurar_pagina():
    # Define a URL do ícone da página
    url_icone = "https://raw.githubusercontent.com/AdiltonCarvalho/Previsao_Credito/main/pesquisa-qualitativa.png"

    # Faz o download do ícone da página usando requests
    response = requests.get(url_icone)
    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            st.warning(f"Erro ao abrir a imagem do ícone: {e}")
            image = None
        
        st.set_page_config(page_title='Previsão de Crédito', page_icon=image, layout='wide', initial_sidebar_state='expanded')
    else:
        st.set_page_config(page_title='Previsão de Crédito', layout='wide', initial_sidebar_state='expanded')

    url_imagem = "https://raw.githubusercontent.com/AdiltonCarvalho/Previsao_Credito/main/Figura-menu.png"

    # Faz o download da imagem do menu usando requests
    response = requests.head(url_imagem)
    if response.status_code == 200:    
        image_response = requests.get(url_imagem)
        try:
            image = Image.open(BytesIO(image_response.content))
            st.sidebar.image(image, use_column_width=True)
        except Exception as e:
            st.sidebar.warning(f"Erro ao abrir a imagem do menu: {e}")
    else:
        st.sidebar.warning('Imagem não encontrada')