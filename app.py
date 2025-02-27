import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")  # Usa toda a largura da página

st.title("Gráfico referência")
col_header = st.columns([8,2])
with col_header[0]:
    st.write("By Leandro Santos")
with col_header[1]:
if st.button("Adicionar Registro"):
    with st.expander("Novo Registro", expanded=True):
        temp_reg = st.number_input("Temperatura da água", value=20.0, step=0.1)
        modelo = st.radio("Parâmetros TRI", options=["TRI 380", "TRI 220"])
        pressao_reg = st.number_input("Parâmetros de pressão", value=200.0, step=1.0)
        if st.button("Enviar Registro"):
            if "registros" not in st.session_state:
                st.session_state["registros"] = []
            st.session_state["registros"].append({
                "temperatura": temp_reg,
                "modelo": modelo,
                "pressao": pressao_reg
            })
            st.success("Registro adicionado!")
            st.experimental_rerun()


# -------------------
# Valores default para o gráfico
default_pressao_inicial = 180
default_pressao_final   = 300
default_temp_min        = 16
default_temp_max        = 40
default_tick_x          = 10    # eixo x (pressão)
default_tick_y          = 2     # eixo y (água)

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

# Função para gerar o gráfico com os parâmetros e os registros (scatter)
def gerar_grafico(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y,
                  tri380_min, tri380_max, tri380_tick, tri220_min, tri220_max, tri220_tick):
    # Cria 13 pontos para a linha (temperatura vs pressão)
    temp = np.linspace(temp_min, temp_max, 13)
    x = np.linspace(pressao_inicial, pressao_final, 13)
    
    # Valores TRI para referência (apenas para plotagem da linha)
    tri380 = [temp_to_tri380(t, temp_min, temp_max) for t in temp]
    tri220 = [temp_to_tri220(t, temp_min, temp_max) for t in temp]

    fig, ax1 = plt.subplots(figsize=(8,6))
    
    # Linha principal: Temperatura da água
    ax1.plot(x, temp, marker='o', color='blue', label='Temperatura da água')
    ax1.set_xlabel('Pressão alta')
    ax1.set_ylabel('Temperatura da água', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Temperatura da água com escalas para TRI 380 e TRI 220')
    ax1.grid(True)
    
    # Configura os eixos para a água
    ax1.set_xlim(pressao_inicial, pressao_final)
    ax1.set_xticks(np.arange(pressao_inicial, pressao_final + tick_x, tick_x))
    ax1.tick_params(axis='x', labelrotation=90)
    ax1.set_ylim(temp_min, temp_max)
    ax1.set_yticks(np.arange(temp_min, temp_max + tick_y, tick_y))
    
    # Eixo à direita: TRI 380
    ax2 = ax1.twinx()
    ax2.set_ylabel('TRI 380', color='red')
    ax2.set_ylim(tri380_min, tri380_max)
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_yticks(np.arange(tri380_min, tri380_max + tri380_tick/10, tri380_tick))
    
    # Segundo eixo à direita: TRI 220
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.set_ylabel('TRI 220', color='green')
    ax3.set_ylim(tri220_min, tri220_max)
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_yticks(np.arange(tri220_min, tri220_max + tri220_tick/10, tri220_tick))
    
    # Se houver registros adicionados via modal, plota os pontos como scatter
    if "registros" in st.session_state:
        for reg in st.session_state["registros"]:
            # Para cada registro, plota no gráfico (x=pressão, y=temperatura)
            if reg["modelo"] == "TRI 380":
                cor = "red"
                marcador = "x"
            else:
                cor = "green"
                marcador = "x"
            ax1.scatter(reg["pressao"], reg["temperatura"], color=cor, marker=marcador, s=100, label=f"{reg['modelo']} (registro)")
    return fig

# --- Layout do gráfico (mantendo a estrutura anterior) ---

# Linhas de parâmetros (mantendo os mesmos controles de layout usados anteriormente)
col_agua, col_graf, col_tri = st.columns([1, 3, 1])

with col_agua:
    st.subheader("Temperatura da água")
    row = st.columns([0.7, 1])
    row[0].write("Mínimo")
    agua_temp_min = row[1].number_input("", value=default_temp_min, key="agua_temp_min", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Máximo")
    agua_temp_max = row[1].number_input("", value=default_temp_max, key="agua_temp_max", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Intervalo")
    agua_tick_y = row[1].number_input("", value=default_tick_y, key="agua_tick_y", label_visibility="collapsed")

with col_tri:
    st.subheader("Parâmetros TRI")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Mínimo**")
    tri380_min = row[1].number_input("", value=default_tri380_min, key="tri380_min", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Máximo**")
    tri380_max = row[1].number_input("", value=default_tri380_max, key="tri380_max", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Intervalo**")
    tri380_tick = row[1].number_input("", value=default_tri380_tick, key="tri380_tick", label_visibility="collapsed")
    
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Mínimo**")
    tri220_min = row[1].number_input("", value=default_tri220_min, key="tri220_min", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Máximo**")
    tri220_max = row[1].number_input("", value=default_tri220_max, key="tri220_max", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Intervalo**")
    tri220_tick = row[1].number_input("", value=default_tri220_tick, key="tri220_tick", label_visibility="collapsed")

with col_graf:
    graph_placeholder = st.empty()
    fig = gerar_grafico(default_pressao_inicial, default_pressao_final,
                        agua_temp_min, agua_temp_max,
                        default_tick_x, agua_tick_y,
                        tri380_min, tri380_max, tri380_tick,
                        tri220_min, tri220_max, tri220_tick)
    graph_placeholder.pyplot(fig)

st.subheader("Parâmetros de pressão")
col_pressao1, col_pressao2, col_pressao3 = st.columns(3)
with col_pressao1:
    st.write("Mínimo")
    pressao_inicial = st.number_input("", value=default_pressao_inicial, key="pressao_inicial", label_visibility="collapsed")
with col_pressao2:
    st.write("Máximo")
    pressao_final = st.number_input("", value=default_pressao_final, key="pressao_final", label_visibility="collapsed")
with col_pressao3:
    st.write("Intervalo")
    pressao_tick = st.number_input("", value=default_tick_x, key="pressao_tick", label_visibility="collapsed")

# Atualiza o gráfico com os parâmetros informados (incluindo os registros)
fig = gerar_grafico(pressao_inicial, pressao_final,
                    agua_temp_min, agua_temp_max,
                    pressao_tick, agua_tick_y,
                    tri380_min, tri380_max, tri380_tick,
                    tri220_min, tri220_max, tri220_tick)
graph_placeholder.pyplot(fig)
