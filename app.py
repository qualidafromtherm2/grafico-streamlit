import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Grafico referência")
st.write("By Leandro Santos")

# Valores padrão
default_pressao_inicial = 180
default_pressao_final = 300
default_temp_min = 16
default_temp_max = 40
default_tick_x = 10      # intervalo para eixo x
default_tick_y = 2       # intervalo para eixo y

# Funções de transformação para TRI 380 e TRI 220 (usando os limites de temperatura)
def temp_to_tri380(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (15.5 - 9.5) + 9.5

def temp_to_tri220(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (28.5 - 22.5) + 22.5

# Função para gerar o gráfico
def gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y):
    # Dados para Temperatura da água com 13 pontos
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
    
    # Configuração do eixo x e y (esquerdo) com os intervalos definidos
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

# Usamos um placeholder para o gráfico, assim o mesmo local é atualizado
fig_placeholder = st.empty()

# Carregar os valores iniciais a partir dos defaults
pressao_inicial = st.number_input("Mínimo Pressão inicial", value=default_pressao_inicial, key="pressao_inicial", label_visibility="collapsed")
pressao_final   = st.number_input("Máximo Pressão final", value=default_pressao_final, key="pressao_final", label_visibility="collapsed")
tick_x          = st.number_input("Intervalo da pressão alta", value=default_tick_x, key="tick_x", label_visibility="collapsed")

temp_min = st.number_input("Mínimo temperatura água", value=default_temp_min, key="temp_min", label_visibility="collapsed")
temp_max = st.number_input("Máximo temperatura água", value=default_temp_max, key="temp_max", label_visibility="collapsed")
tick_y   = st.number_input("Intervalo da temperatura da água", value=default_tick_y, key="tick_y", label_visibility="collapsed")

# Exibe o gráfico inicialmente
fig = gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y)
fig_placeholder.pyplot(fig)

st.write("## Atualize os parâmetros do gráfico")

# Organiza os inputs em duas colunas abaixo do gráfico:
col_temp, col_pressao = st.columns(2)

with col_temp:
    new_temp_min = st.number_input("Mínimo temperatura água", value=temp_min, key="new_temp_min")
    new_temp_max = st.number_input("Máximo temperatura água", value=temp_max, key="new_temp_max")
    new_tick_y   = st.number_input("Intervalo da temperatura da água", value=tick_y, key="new_tick_y")

with col_pressao:
    new_pressao_inicial = st.number_input("Mínimo Pressão inicial", value=pressao_inicial, key="new_pressao_inicial")
    new_pressao_final   = st.number_input("Máximo Pressão final", value=pressao_final, key="new_pressao_final")
    new_tick_x          = st.number_input("Intervalo da pressão alta", value=tick_x, key="new_tick_x")

# Quando os valores são alterados, re-renderizamos o gráfico com os novos parâmetros
# (Como Streamlit reexecuta o script, a mudança nos widgets já atualiza os valores.)
fig = gerar_grafico(new_pressao_inicial, new_pressao_final, new_temp_min, new_temp_max, new_tick_x, new_tick_y)
fig_placeholder.pyplot(fig)
