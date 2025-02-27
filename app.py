import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")  # Usa toda a largura da página

st.title("Gráfico referência")
st.write("By Leandro Santos")

# Valores default
default_pressao_inicial = 180
default_pressao_final   = 300
default_temp_min        = 16
default_temp_max        = 40
default_tick_x          = 10      # intervalo para eixo x (pressão)
default_tick_y          = 2       # intervalo para eixo y (água)

default_tri380_min      = 9.5
default_tri380_max      = 15.5
default_tri380_tick     = 0.5

default_tri220_min      = 22.5
default_tri220_max      = 28.5
default_tri220_tick     = 0.5

# Funções de transformação para TRI (apenas para referência visual)
def temp_to_tri380(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (default_tri380_max - default_tri380_min) + default_tri380_min

def temp_to_tri220(T, tmin, tmax):
    return (T - tmin) / (tmax - tmin) * (default_tri220_max - default_tri220_min) + default_tri220_min

# Função para gerar o gráfico com todos os parâmetros
def gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y,
                  tri380_min, tri380_max, tri380_tick, tri220_min, tri220_max, tri220_tick):
    # Gera 13 pontos para a temperatura e pressão
    temp = np.linspace(temp_min, temp_max, 13)
    x = np.linspace(pressao_inicial, pressao_final, 13)
    
    # Valores TRI para referência
    tri380 = [temp_to_tri380(t, temp_min, temp_max) for t in temp]
    tri220 = [temp_to_tri220(t, temp_min, temp_max) for t in temp]

    fig, ax1 = plt.subplots(figsize=(8,6))
    
    # Plot principal: Temperatura da água
    ax1.plot(x, temp, marker='o', color='blue', label='Temperatura da água')
    ax1.set_xlabel('Pressão alta')
    ax1.set_ylabel('Temperatura da água', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Temperatura da água com escalas para TRI 380 e TRI 220')
    ax1.grid(True)
    
    # Configuração do eixo x e y (água)
    ax1.set_xlim(pressao_inicial, pressao_final)
    ax1.set_xticks(np.arange(pressao_inicial, pressao_final + tick_x, tick_x))
    ax1.tick_params(axis='x', labelrotation=90)  # Rótulos do eixo x na vertical
    
    ax1.set_ylim(temp_min, temp_max)
    ax1.set_yticks(np.arange(temp_min, temp_max + tick_y, tick_y))
    
    # Primeiro eixo à direita: TRI 380 (configurado pelos inputs)
    ax2 = ax1.twinx()
    ax2.set_ylabel('TRI 380', color='red')
    ax2.set_ylim(tri380_min, tri380_max)
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_yticks(np.arange(tri380_min, tri380_max + tri380_tick/10, tri380_tick))
    
    # Segundo eixo à direita: TRI 220 (configurado pelos inputs)
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.set_ylabel('TRI 220', color='green')
    ax3.set_ylim(tri220_min, tri220_max)
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_yticks(np.arange(tri220_min, tri220_max + tri220_tick/10, tri220_tick))
    
    return fig

# --- Layout da página ---

# Linha superior: 3 colunas
# Coluna 1: Parâmetros da água
# Coluna 2: Gráfico
# Coluna 3: Parâmetros TRI (divididos em 2 sub-colunas)
col_agua, col_graf, col_tri = st.columns([1, 3, 1])

with col_agua:
    st.subheader("Temperatura da água")
    st.text("Mínimo")
    agua_temp_min = st.number_input("", value=default_temp_min, key="agua_temp_min")
    st.text("Máximo")
    agua_temp_max = st.number_input("", value=default_temp_max, key="agua_temp_max")
    st.text("Intervalo")
    agua_tick_y   = st.number_input("", value=default_tick_y, key="agua_tick_y")

with col_tri:
    st.subheader("Parâmetros TRI")
    col_tri380, col_tri220 = st.columns(2)
    with col_tri380:
        st.markdown("**TRI 380**")
        st.text("Mínimo")
        tri380_min  = st.number_input("", value=default_tri380_min, key="tri380_min")
        st.text("Máximo")
        tri380_max  = st.number_input("", value=default_tri380_max, key="tri380_max")
        st.text("Intervalo")
        tri380_tick = st.number_input("", value=default_tri380_tick, key="tri380_tick")
    with col_tri220:
        st.markdown("**TRI 220**")
        st.text("Mínimo")
        tri220_min  = st.number_input("", value=default_tri220_min, key="tri220_min")
        st.text("Máximo")
        tri220_max  = st.number_input("", value=default_tri220_max, key="tri220_max")
        st.text("Intervalo")
        tri220_tick = st.number_input("", value=default_tri220_tick, key="tri220_tick")

with col_graf:
    # Placeholder para o gráfico que será atualizado in place
    graph_placeholder = st.empty()
    fig = gerar_grafico(default_pressao_inicial, default_pressao_final,
                        agua_temp_min, agua_temp_max,
                        default_tick_x, agua_tick_y,
                        tri380_min, tri380_max, tri380_tick,
                        tri220_min, tri220_max, tri220_tick)
    graph_placeholder.pyplot(fig)

# Linha inferior para os parâmetros de pressão (organizados horizontalmente)
st.subheader("Parâmetros de pressão")
col_pressao1, col_pressao2, col_pressao3 = st.columns(3)
with col_pressao1:
    st.text("Mínimo")
    pressao_inicial = st.number_input("", value=default_pressao_inicial, key="pressao_inicial")
with col_pressao2:
    st.text("Máximo")
    pressao_final   = st.number_input("", value=default_pressao_final, key="pressao_final")
with col_pressao3:
    st.text("Intervalo")
    pressao_tick = st.number_input("", value=default_tick_x, key="pressao_tick")

# Atualiza o gráfico in place com os novos parâmetros
fig = gerar_grafico(pressao_inicial, pressao_final,
                    agua_temp_min, agua_temp_max,
                    pressao_tick, agua_tick_y,
                    tri380_min, tri380_max, tri380_tick,
                    tri220_min, tri220_max, tri220_tick)
graph_placeholder.pyplot(fig)
