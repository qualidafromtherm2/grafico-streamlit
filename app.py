import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Gráfico referência")
st.write("By Leandro Santos")

# Valores default
default_pressao_inicial = 180
default_pressao_final = 300
default_temp_min = 16
default_temp_max = 40
default_tick_x = 10      # intervalo para eixo x (pressão)
default_tick_y = 2       # intervalo para eixo y (temperatura)

# Funções de transformação para TRI 380 e TRI 220
def temp_to_tri380(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (15.5 - 9.5) + 9.5

def temp_to_tri220(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (28.5 - 22.5) + 22.5

# Função para gerar o gráfico com os parâmetros definidos
def gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y):
    # Gera 13 pontos para temperatura e pressão
    temp = np.linspace(temp_min, temp_max, 13)
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
    
    # Configurações do eixo x e y (esquerdo)
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

# --- Layout da página ---

# Primeiro, cria uma linha com duas colunas: 
# - Na coluna da esquerda, os parâmetros da água (dispostos verticalmente).
# - Na coluna da direita, o gráfico.
col_esquerda, col_direita = st.columns([1, 3])

with col_esquerda:
    st.subheader("Parâmetros da água")
    # Esses inputs serão dispostos verticalmente
    agua_temp_min = st.number_input("Mínimo temperatura água", value=default_temp_min, key="agua_temp_min")
    agua_temp_max = st.number_input("Máximo temperatura água", value=default_temp_max, key="agua_temp_max")
    agua_tick_y   = st.number_input("Intervalo da temperatura", value=default_tick_y, key="agua_tick_y")

with col_direita:
    # Cria um placeholder para o gráfico (ele será atualizado in place)
    graph_placeholder = st.empty()
    # Exibe o gráfico com os parâmetros atuais
    # Aqui usamos valores default inicialmente (os inputs abaixo serão utilizados para atualizar)
    fig = gerar_grafico(default_pressao_inicial, default_pressao_final,
                        agua_temp_min, agua_temp_max,
                        default_tick_x, agua_tick_y)
    graph_placeholder.pyplot(fig)

# Em seguida, abaixo do gráfico, cria uma linha para os parâmetros de pressão,
# dispostos horizontalmente (um ao lado do outro).
st.subheader("Parâmetros de pressão")
col_pressao1, col_pressao2, col_pressao3 = st.columns(3)
with col_pressao1:
    pressao_inicial = st.number_input("Mínimo Pressão inicial", value=default_pressao_inicial, key="pressao_inicial")
with col_pressao2:
    pressao_final   = st.number_input("Máximo Pressão final", value=default_pressao_final, key="pressao_final")
with col_pressao3:
    pressao_tick = st.number_input("Intervalo da pressão", value=default_tick_x, key="pressao_tick")

# --- Atualização do gráfico em tempo real ---

# Toda vez que algum dos valores for alterado, o script é reexecutado,
# atualizando o gráfico no mesmo placeholder.
fig = gerar_grafico(pressao_inicial, pressao_final,
                    agua_temp_min, agua_temp_max,
                    pressao_tick, agua_tick_y)
graph_placeholder.pyplot(fig)
