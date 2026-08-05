import streamlit as st

st.set_page_config(
    page_title="Reparos em Andamento",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Reparos em Andamento")

st.write("Aqui serão exibidas todas as Ordens de Serviço que ainda não foram entregues.")

st.divider()

st.info("Nenhum reparo em andamento.")

st.divider()

if st.button("🔄 Atualizar Lista", use_container_width=True):
    st.success("A atualização automática será implementada junto com o banco de dados.")