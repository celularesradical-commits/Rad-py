import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Compatibilidade de Películas",
    page_icon="📱",
    layout="centered"
)

# Título
st.title("📱 Compatibilidade de Películas")

st.write("Digite o modelo do smartphone para pesquisar películas compatíveis.")

# Campo de pesquisa
modelo = st.text_input(
    "Modelo do smartphone",
    placeholder="Ex.: iPhone 13, Galaxy S23, Redmi Note 12"
)

# Botão
if st.button("Pesquisar"):
    if modelo.strip():
        st.success(f"Pesquisando o modelo: {modelo}")
    else:
        st.warning("Digite um modelo de smartphone.")
