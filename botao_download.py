import streamlit as st
import base64

# Função para adicionar o link de download
def download_link(report_html, file_name="EDA_Report.html"):
    # Codifica o conteúdo HTML em base64
    b64 = base64.b64encode(report_html.encode()).decode()

    # Cria o link HTML
    href = f'<a href="data:text/html;base64,{b64}" download="{file_name}">Download do Relatório EDA em HTML</a>'
    
    # Adiciona o link de download no Streamlit
    st.markdown(href, unsafe_allow_html=True)
    st.markdown("---")