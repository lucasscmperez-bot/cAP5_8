import scipy.stats
import streamlit as st
import pandas as pd
import time

st.header('Jogando uma moeda')

# 1. Inicializa o estado da sessão se não existir
if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['Tentativa', 'Media_Final'])

# Container para o gráfico e o DataFrame
chart_container = st.empty()
means = []

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    outcome_no = 0
    outcome_1_count = 0
    current_mean = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        current_mean = outcome_1_count / outcome_no
        means.append(current_mean)
        
        chart_container.line_chart(pd.DataFrame(means))
        time.sleep(0.05)

    return current_mean

number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')
    final_mean = toss_coin(number_of_trials)
    
    # 2. Adiciona o resultado ao DataFrame no session_state
    new_result = pd.DataFrame({'Tentativa': [number_of_trials], 'Media_Final': [final_mean]})
    st.session_state['df_experiment_results'] = pd.concat([st.session_state['df_experiment_results'], new_result], ignore_index=True)
    
    st.success("Experimento concluído!")

# 3. Exibe a tabela com o histórico
st.subheader("Histórico de Resultados")
st.table(st.session_state['df_experiment_results'])