import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
import uuid

st.set_page_config(layout="wide")

st.title("GERADOR DE GRÁFICO")

# --------------------------------------------------
# Cabeçalho com "By Leandro Santos" e botão para adicionar registro
# --------------------------------------------------
col_header = st.columns([8, 2])
with col_header[0]:
    st.write("By Leandro Santos")
if "show_expander" not in st.session_state:
    st.session_state["show_expander"] = False
with col_header[1]:
    if st.button("Adicionar Registro"):
        st.session_state["show_expander"] = True

# --------------------------------------------------
# Expander para inserir novo registro (usado para ambos os gráficos)
# --------------------------------------------------
if st.session_state["show_expander"]:
    with st.expander("Novo Registro", expanded=True):
        with st.form("registro_form"):
            temp_val = st.number_input("Temperatura da água", value=30.0, step=0.1)
            pressao_val = st.number_input("Parâmetros de pressão", value=250.0, step=1.0)
            tri_modelo = st.radio("Modelo TRI", options=["TRI 380", "TRI 220"])
            tri_valor = st.number_input("Valor TRI", value=12.4, step=0.1)
            
            enviar = st.form_submit_button("Enviar Registro")
            if enviar:
                if "registros" not in st.session_state:
                    st.session_state["registros"] = []
                st.session_state["registros"].append({
                    "temp": temp_val,
                    "pressao": pressao_val,
                    "tri_modelo": tri_modelo,
                    "tri_valor": tri_valor
                })
                st.success("Registro adicionado!")
                st.session_state["show_expander"] = False
                try:
                    st.set_query_params(_=str(uuid.uuid4()))
                except AttributeError:
                    try:
                        st.query_params = {"_": str(uuid.uuid4())}
                    except Exception:
                        st.experimental_set_query_params(_=str(uuid.uuid4()))
                # Não chamamos st.stop() para que o gráfico seja renderizado em seguida

# --------------------------------------------------
# Parâmetros default para o primeiro gráfico (com TRI)
# --------------------------------------------------
default_pressao_inicial = 180
default_pressao_final   = 300
default_temp_min        = 16
default_temp_max        = 40
default_tick_x          = 10
default_tick_y          = 2

default_tri380_min      = 9.5
default_tri380_max      = 15.5
default_tri380_tick     = 0.5

default_tri220_min      = 22.5
default_tri220_max      = 28.5
default_tri220_tick     = 0.5

# --------------------------------------------------
# Função para gerar o gráfico com parâmetros TRI
# --------------------------------------------------
def gerar_grafico(
    pressao_inicial, pressao_final,
    temp_min, temp_max,
    tick_x, tick_y,
    tri380_min, tri380_max, tri380_tick,
    tri220_min, tri220_max, tri220_tick
):
    """Gera o gráfico base + pontos/linhas dos registros (com parâmetros TRI)."""
    temp = np.linspace(temp_min, temp_max, 13)
    x = np.linspace(pressao_inicial, pressao_final, 13)

    fig, ax1 = plt.subplots(figsize=(8,6))
    ax1.plot(x, temp, color='blue', label='Temperatura da água')
    ax1.set_xlabel('Pressão alta')
    ax1.set_ylabel('Temperatura da água', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_title('Temperatura da água com escalas para TRI 380 e TRI 220')
    ax1.grid(True)

    ax1.set_xlim(pressao_inicial, pressao_final)
    ax1.set_xticks(np.arange(pressao_inicial, pressao_final + tick_x, tick_x))
    ax1.tick_params(axis='x', labelrotation=90)
    ax1.set_ylim(temp_min, temp_max)
    ax1.set_yticks(np.arange(temp_min, temp_max + tick_y, tick_y))

    ax2 = ax1.twinx()
    ax2.set_ylabel('TRI 380', color='red')
    ax2.set_ylim(tri380_min, tri380_max)
    ax2.set_yticks(np.arange(tri380_min, tri380_max + tri380_tick/10, tri380_tick))
    ax2.tick_params(axis='y', labelcolor='red')

    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.set_ylabel('TRI 220', color='green')
    ax3.set_ylim(tri220_min, tri220_max)
    ax3.set_yticks(np.arange(tri220_min, tri220_max + tri220_tick/10, tri220_tick))
    ax3.tick_params(axis='y', labelcolor='green')

    if "registros" in st.session_state:
        for reg in st.session_state["registros"]:
            # Ponto azul no eixo da água
            ax1.scatter(reg["pressao"], reg["temp"], color="blue", s=100, zorder=5)
            if reg["tri_modelo"] == "TRI 380":
                ax2.scatter(reg["pressao"], reg["tri_valor"], color="red", s=100, zorder=5)
                con = ConnectionPatch(
                    xyA=(reg["pressao"], reg["temp"]), coordsA=ax1.transData,
                    xyB=(reg["pressao"], reg["tri_valor"]), coordsB=ax2.transData,
                    color="gray", linewidth=2, zorder=1
                )
                ax2.add_artist(con)
            else:
                ax3.scatter(reg["pressao"], reg["tri_valor"], color="green", s=100, zorder=5)
                con = ConnectionPatch(
                    xyA=(reg["pressao"], reg["temp"]), coordsA=ax1.transData,
                    xyB=(reg["pressao"], reg["tri_valor"]), coordsB=ax3.transData,
                    color="gray", linewidth=2, zorder=1
                )
                ax3.add_artist(con)

    return fig

# --------------------------------------------------
# Layout dos parâmetros fixos para o primeiro gráfico
# --------------------------------------------------
col_agua, col_graf, col_tri = st.columns([1, 3, 1])
with col_agua:
    st.subheader("Temperatura da água")
    row = st.columns([0.7, 1])
    row[0].write("Máximo")
    agua_temp_max = row[1].number_input("", value=default_temp_max, key="agua_temp_max", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Mínimo")
    agua_temp_min = row[1].number_input("", value=default_temp_min, key="agua_temp_min", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Intervalo")
    agua_tick_y = row[1].number_input("", value=default_tick_y, key="agua_tick_y", label_visibility="collapsed")

with col_tri:
    st.subheader("Parâmetros TRI")
    # TRI 380
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Máximo**")
    tri380_max = row[1].number_input("", value=default_tri380_max, key="tri380_max", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Mínimo**")
    tri380_min = row[1].number_input("", value=default_tri380_min, key="tri380_min", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 380 - Intervalo**")
    tri380_tick = row[1].number_input("", value=default_tri380_tick, key="tri380_tick", label_visibility="collapsed")
    # TRI 220
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Máximo**")
    tri220_max = row[1].number_input("", value=default_tri220_max, key="tri220_max", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Mínimo**")
    tri220_min = row[1].number_input("", value=default_tri220_min, key="tri220_min", label_visibility="collapsed")
    row = st.columns([1, 1])
    row[0].markdown("**TRI 220 - Intervalo**")
    tri220_tick = row[1].number_input("", value=default_tri220_tick, key="tri220_tick", label_visibility="collapsed")

with col_graf:
    graph_placeholder = st.empty()
    fig = gerar_grafico(
        pressao_inicial=180,
        pressao_final=300,
        temp_min=st.session_state["agua_temp_min"],
        temp_max=st.session_state["agua_temp_max"],
        tick_x=10,
        tick_y=st.session_state["agua_tick_y"],
        tri380_min=st.session_state["tri380_min"],
        tri380_max=st.session_state["tri380_max"],
        tri380_tick=st.session_state["tri380_tick"],
        tri220_min=st.session_state["tri220_min"],
        tri220_max=st.session_state["tri220_max"],
        tri220_tick=st.session_state["tri220_tick"],
    )
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

fig = gerar_grafico(
    pressao_inicial=st.session_state["pressao_inicial"],
    pressao_final=st.session_state["pressao_final"],
    temp_min=st.session_state["agua_temp_min"],
    temp_max=st.session_state["agua_temp_max"],
    tick_x=st.session_state["pressao_tick"],
    tick_y=st.session_state["agua_tick_y"],
    tri380_min=st.session_state["tri380_min"],
    tri380_max=st.session_state["tri380_max"],
    tri380_tick=st.session_state["tri380_tick"],
    tri220_min=st.session_state["tri220_min"],
    tri220_max=st.session_state["tri220_max"],
    tri220_tick=st.session_state["tri220_tick"],
)
graph_placeholder.pyplot(fig)

# --------------------------------------------------
# Segundo Gráfico: Temperatura Ambiente x Pressão baixa
# --------------------------------------------------
st.markdown("---")
st.subheader("Temperatura Ambiente x Pressão baixa")

# Layout: 2 colunas; a primeira para os parâmetros de Temperatura Ambiente (à esquerda) e a segunda para o gráfico
col_ta2, col_graph2 = st.columns([1, 3])
with col_ta2:
    st.subheader("Temperatura Ambiente")
    row = st.columns([0.7, 1])
    row[0].write("Máximo")
    ta_max = row[1].number_input("", value=40, key="ta_max", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Mínimo")
    ta_min = row[1].number_input("", value=0, key="ta_min", label_visibility="collapsed")
    row = st.columns([0.7, 1])
    row[0].write("Intervalo")
    ta_tick = row[1].number_input("", value=5, key="ta_tick", label_visibility="collapsed")

with col_graph2:
    graph_placeholder2 = st.empty()
    def gerar_grafico_sem_tri(pressao_inicial, pressao_final, temp_min, temp_max, tick_x, tick_y):
        """Gera um gráfico base (Temperatura Ambiente vs. Pressão baixa)."""
        temp = np.linspace(temp_min, temp_max, 13)
        x = np.linspace(pressao_inicial, pressao_final, 13)
    
        fig, ax = plt.subplots(figsize=(8,6))
        ax.plot(x, temp, color='blue', label='Temperatura Ambiente')
        ax.set_xlabel('Pressão baixa')
        ax.set_ylabel('Temperatura Ambiente', color='blue')
        ax.tick_params(axis='y', labelcolor='blue')
        ax.set_title('Temperatura Ambiente x Pressão baixa')
        ax.grid(True)
    
        ax.set_xlim(pressao_inicial, pressao_final)
        ax.set_xticks(np.arange(pressao_inicial, pressao_final + tick_x, tick_x))
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylim(temp_min, temp_max)
        ax.set_yticks(np.arange(temp_min, temp_max + tick_y, tick_y))
    
        if "registros" in st.session_state:
            for reg in st.session_state["registros"]:
                ax.scatter(reg["pressao"], reg["temp"], color="blue", s=100, zorder=5)
        return fig
    
    fig2 = gerar_grafico_sem_tri(
        pressao_inicial=st.session_state.get("pb_min", 26),
        pressao_final=st.session_state.get("pb_max", 95),
        temp_min=st.session_state.get("ta_min", 0),
        temp_max=st.session_state.get("ta_max", 40),
        tick_x=st.session_state.get("pb_tick", 10),
        tick_y=st.session_state.get("ta_tick", 5)
    )
    graph_placeholder2.pyplot(fig2)

# Configuração de Pressão baixa (colocada abaixo do segundo gráfico)
st.subheader("Configuração de Pressão baixa")
col_pb1, col_pb2, col_pb3 = st.columns(3)
with col_pb1:
    st.write("Mínimo")
    pb_min = st.number_input("", value=26, key="pb_min", label_visibility="collapsed")
with col_pb2:
    st.write("Máximo")
    pb_max = st.number_input("", value=95, key="pb_max", label_visibility="collapsed")
with col_pb3:
    st.write("Intervalo")
    pb_tick = st.number_input("", value=10, key="pb_tick", label_visibility="collapsed")


fig2 = gerar_grafico_sem_tri(
    pressao_inicial=pb_min,
    pressao_final=pb_max,
    temp_min=st.session_state.get("ta_min", 0),
    temp_max=st.session_state.get("ta_max", 40),
    tick_x=pb_tick,
    tick_y=st.session_state.get("ta_tick", 5)
)
graph_placeholder2.pyplot(fig2)
