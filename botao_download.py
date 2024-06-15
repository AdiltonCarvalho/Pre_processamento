import streamlit as st

# Função para adicionar o botão de download
def download_button(report_html, file_name="EDA_Report.html"):    
    st.download_button(
        label="Download do Relatório EDA em HTML",
        data=report_html,
        file_name=file_name,
        mime="text/html"
    )
    st.markdown("---")