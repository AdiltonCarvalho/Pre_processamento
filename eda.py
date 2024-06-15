import sweetviz as sv
import streamlit as st
import time

# Função para gerar análise exploratória de dados com Sweetviz
def eda_report_sweetviz(data, progress_text, progress_bar):
    
    # Analisando Variáveis
    for i in range(70):
        progress_text.text(f"Analisando Variáveis... ({i}%)")
        progress_bar.progress(i)
        time.sleep(0.04)
    
    # Gerando Relatório EDA
    progress_text.text(f"Gerando Relatório EDA... (70%)")
    progress_bar.progress(70)
    report = sv.analyze(data)  # Gera o relatório EDA
    time.sleep(0.04) 
    
    # Salvando Relatório EDA
    for i in range(71, 100):
        progress_text.text(f"Salvando Relatório EDA... ({i}%)")
        progress_bar.progress(i)
        time.sleep(0.04)
    
    report.show_html(filepath='EDA_Report.html', open_browser=False)  # Salva o relatório EDA
    
    # Conclusão do processamento
    progress_bar.progress(100)
    progress_text.text("Relatório EDA gerado com sucesso!")
    
    # Abre o arquivo EDA_Report.html no modo de leitura, faz a leitura e retorna o conteúdo
    with open("EDA_Report.html", "r", encoding='utf-8') as file:
        report_html = file.read()

    return report_html