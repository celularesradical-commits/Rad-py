import streamlit as st
from ai_client import AIOnlineClient

# Configuração da página
st.set_page_config(
    page_title="Compatibilidade de Películas",
    page_icon="📱",
    layout="centered"
)

# Título
st.title("📱 Compatibilidade de Películas")

st.write(
    "Digite o modelo do smartphone para pesquisar películas compatíveis."
)

# Campo de pesquisa
modelo = st.text_input(
    "Modelo do smartphone",
    placeholder="Ex.: iPhone 13, Galaxy S23, Redmi Note 12"
)

# Botão
if st.button("Pesquisar"):

    if not modelo.strip():
        st.warning("Digite um modelo de smartphone.")

    else:
        try:
            cliente = AIOnlineClient()

            with st.spinner("Pesquisando compatibilidade..."):
                resposta = cliente.pesquisar(modelo)

            st.success("Pesquisa concluída!")

            st.markdown(resposta)

        except Exception as erro:
            st.error(f"Erro ao consultar a IA:\n\n{erro}")