import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Grafico referencia")
st.write("Por Leandro Santos")

# Dados e parâmetros
pressao_inicial = st.number_input("Pressão inicial", value=180)
pressao_final = st.number_input("Pressão final", value=300)

# Dados para Temperatura da água (de 16 a 40) com 13 pontos
temp = np.linspace(16, 40, 13)
x = np.linspace(pressao_inicial, pressao_final, 13)

# Funções de transformação para TRI 380 e TRI 220
def temp_to_tri380(T):
    return (T - 16) / (40 - 16) * (15.5 - 9.5) + 9.5

def temp_to_tri220(T):
    return (T - 16) / (40 - 16) * (28.5 - 22.5) + 22.5

tri380 = [temp_to_tri380(t) for t in temp]
tri220 = [temp_to_tri220(t) for t in temp]

# Criação do gráfico com Matplotlib
fig, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(x, temp, marker='o', color='blue', label='Temperatura da água')
ax1.set_xlabel('Pressão alta')
ax1.set_ylabel('Temperatura da água', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title('Temperatura da água com escalas para TRI 380 e TRI 220')
ax1.grid(True)

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

# Exibir o gráfico no Streamlit
st.pyplot(fig)
