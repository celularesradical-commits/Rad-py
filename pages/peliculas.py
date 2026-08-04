

import streamlit as st
from ai_client import AIOnlineClient


def tela():

    st.title("🔍 Pesquisar Películas")

    st.write(
        "Digite o modelo do smartphone para pesquisar películas compatíveis."
    )

    modelo = st.text_input(
        "Modelo do smartphone",
        placeholder="Ex.: iPhone 13, Galaxy S23, Redmi Note 12"
    )

    if st.button("Pesquisar", use_container_width=True):

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