import streamlit as st

st.set_page_config(
    page_title="Pesquisar Reparo",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Pesquisar Reparo")

st.write("Localize uma Ordem de Serviço pelo número, cliente, telefone ou aparelho.")

# Campo de pesquisa
pesquisa = st.text_input(
    "Pesquisar",
    placeholder="Digite o número da OS, cliente, telefone ou modelo..."
)

# Botão
if st.button("🔎 Pesquisar", use_container_width=True):
    if pesquisa.strip() == "":
        st.warning("Digite alguma informação para pesquisar.")
    else:
        st.info("A pesquisa no banco de dados será implementada na próxima etapa.")

st.divider()

st.subheader("Resultados")

st.info("Nenhuma pesquisa realizada.")