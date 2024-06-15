import streamlit as st
import numpy as np
import scipy
from pycaret.classification import setup, pull, models, compare_models, plot_model, save_model, load_model

# Alias temporário para scipy.interp para evitar erros de importação
scipy.interp = np.interp

def treina_modelo(dataset):

    st.markdown('---')
    st.write("### Análise de configuração")
    st.write("Configuração do ambiente para um experimento de aprendizado de máquina com normalização de dados, transformação em quantil e correção de desequilíbrios nas classes, quando houver. O objetivo de prever a probabilidade de um candidato a crédito ser considerado 'mau'.")
    st.markdown('---')

    experiment = setup(data=dataset, target='mau', experiment_name='credit_1',
                       normalize=True, normalize_method='zscore', 
                       transformation=True, transformation_method='quantile',
                       fix_imbalance=True, session_id=123)
    
    # Puxar a tabela com as informações da configuração
    setup_df = pull()

    # Configurar a aplicação em colunas
    col1, col2 = st.columns(2)

    # Exibir a tabela no Streamlit
    col1.table(setup_df)

    st.markdown('---')
    st.write("### Análise de modelos")
    st.write("Comparação do desempenho de vários modelos de classificação usando validação cruzada com 4 dobras, ordenando-os com base na área sob a curva ROC (AUC)")
    st.markdown('---')

    # Amostra aleatoriamente 80% das linhas do DataFrame 'dataset' e armazena em 'data'
    data = dataset.sample(frac=0.80, random_state=786)

    # Índices das linhas que serão removidas para criar 'data_unseen'
    indices_a_remover = data.index

    # Remove do DataFrame 'dataset' as linhas presentes em 'data', criando 'data_unseen'
    data_unseen = dataset.drop(indices_a_remover)

    # Reseta o índice do DataFrame 'data' após a amostragem
    data.reset_index(inplace=True, drop=True)

    # Reseta o índice do DataFrame 'data_unseen' após a remoção das linhas
    data_unseen.reset_index(inplace=True, drop=True)

    # Obter a lista de todos os modelos disponíveis
    modelos = models()
    modelos_nomes = modelos.index.tolist()
    num_modelos = len(modelos_nomes)  # Obter o número total de modelos

    # Imprime as amostras
    st.write('Conjunto de dados para modelagem (treino e teste): ' + str(data.shape))
    st.write('Conjunto de dados não usados no treino/teste, apenas como validação: ' + str(data_unseen.shape))
    st.write(f'Quantidade de modelos identificados: ', str(num_modelos))

    # Compara os desempenhos de vários modelos de classificação usando validação cruzada com 4 dobras,
    # ordenando-os com base na área sob a curva ROC (AUC)
    melhor_modelo = compare_models(fold=4, sort='AUC')

    # Pegar o DataFrame com os resultados dos modelos comparados
    resultados_df = pull()

    # Exibir os resultados da comparação dos modelos no Streamlit
    st.table(resultados_df)

    # Extrair apenas o nome do melhor modelo
    nome_melhor_modelo = type(melhor_modelo).__name__

    st.markdown('---')
    st.write("### Análise Gráfica")
    st.write(f"Geração dos gráficos de Importância de variáveis e Curva ROC com o modelo {nome_melhor_modelo} que apresentou o melhor resultado (AUC)")
    st.markdown('---')

    # Plotar e mostrar o gráfico de importância das features
    plot_model(melhor_modelo, plot='feature', save=True)
    st.image('Feature Importance.png')
    
    # Plotar e mostrar a curva ROC
    plot_model(melhor_modelo, plot='auc', save=True)
    st.image('AUC.png')

    st.markdown('---')
    st.write("### Pipeline")
    st.write(f"Geração do pipeline com o modelo {nome_melhor_modelo} que apresentou o melhor resultado (AUC)")
    st.markdown('---')

    # Salva o melhor modelo treinado em disco com o nome 'GBC Model 051924'
    save_model(melhor_modelo,'GBC Model 140624')

    # Carrega um modelo previamente treinado do disco com o nome 'GBC Model 051924'
    modelo_salvo = load_model('GBC Model 140624')

    # Verifica se o modelo salvo tem o atributo 'named_steps'
    if hasattr(modelo_salvo, 'named_steps'):
        pipeline_details = {}
        for step_name, step in modelo_salvo.named_steps.items():
            # Adiciona os detalhes do passo ao dicionário
            if hasattr(step, '__dict__'):
                step_details = {attr: getattr(step, attr) for attr in step.__dict__}
                pipeline_details[step_name] = step_details
            else:
                pipeline_details[step_name] = step
        st.write(pipeline_details)
    else:
        st.write("O modelo salvo não possui um pipeline com named_steps.")