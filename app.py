import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Grafico referência")
st.write("Por Leandro Santos")

# Valores padrão para os parâmetros
default_pressao_inicial = 180
default_pressao_final = 300
default_temp_min = 16
default_temp_max = 40
default_tick_x = 10      # exemplo: intervalo de 10 em 10 para o eixo x
default_tick_y = 2       # exemplo: intervalo de 2 em 2 para o eixo y

# Funções de transformação para TRI 380 e TRI 220 utilizando os limites de temperatura
def temp_to_tri380(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (15.5 - 9.5) + 9.5

def temp_to_tri220(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (28.5 - 22.5) + 22.5

# Função para gerar o gráfico, agora com tick_interval para os eixos x e y
def gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y):
    # Cria os dados para a Temperatura da água com 13 pontos
    temp = np.linspace(temp_min, temp_max, 13)
    # Utiliza np.linspace para os dados, mas os ticks serão definidos conforme o intervalo escolhido
    x = np.linspace(pressao_inicial, pressao_final, 13)
    
    tri380 = [temp_to_tri380(t, temp_min, temp_max) for t in temp]
    tri220 = [temp_to_tri220(t, temp_min, temp_max) for t in temp]

    fig, ax1 = plt.subplots(figsize=(8,6))
    ax1.plot(x, temp, marker='o', color='blue', label='Temperatura da água')
    ax1.set_xlabel('Pressão alta')
    ax1.set_ylabel('Temperatura da água', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Temperatura da água com escalas para TRI 380 e TRI 220')
    ax1.grid(True)
    
    # Define os ticks e limites do eixo x e y (esquerda)
    ax1.set_xlim(pressao_inicial, pressao_final)
    ax1.set_xticks(np.arange(pressao_inicial, pressao_final + tick_x, tick_x))
    ax1.set_ylim(temp_min, temp_max)
    ax1.set_yticks(np.arange(temp_min, temp_max + tick_y, tick_y))

    # Primeiro eixo à direita: TRI 380
    ax2 = ax1.twinx()
    ax2.set_ylabel('TRI 380', color='red')
    ax2.set_ylim(min(tri380), max(tri380))
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_yticks(np.arange(9.5, 15.5 + 0.1, 0.5))

    # Segundo eixo à direita: TRI 220
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.set_ylabel('TRI 220', color='green')
    ax3.set_ylim(min(tri220), max(tri220))
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_yticks(np.arange(22.5, 28.5 + 0.1, 0.5))

    return fig

# Exibe o gráfico inicial com os valores padrão
fig = gerar_grafico(default_pressao_inicial, default_pressao_final,
                    default_temp_min, default_temp_max,
                    default_tick_x, default_tick_y)
st.pyplot(fig)

# Formulário para atualizar os parâmetros: pressões, limites do eixo y e intervalos dos ticks
with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    with col1:
        pressao_inicial = st.number_input("Pressão inicial", value=default_pressao_inicial)
        temp_min = st.number_input("Mínimo eixo y", value=default_temp_min)
        tick_x = st.number_input("Intervalo dos ticks do eixo x", value=default_tick_x)
    with col2:
        pressao_final = st.number_input("Pressão final", value=default_pressao_final)
        temp_max = st.number_input("Máximo eixo y", value=default_temp_max)
        tick_y = st.number_input("Intervalo dos ticks do eixo y", value=default_tick_y)
    submit = st.form_submit_button(label="Atualizar gráfico")

# Se o formulário for enviado, atualiza o gráfico com os novos parâmetros
if submit:
    fig = gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y)
    st.pyplot(fig)
