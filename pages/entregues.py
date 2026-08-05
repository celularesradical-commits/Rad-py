import streamlit as st

st.set_page_config(
    page_title="Entregues",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Reparos Entregues")

st.info("Nenhum reparo entregue.")

if st.button("🔄 Atualizar Lista", use_container_width=True):
    st.success("Em desenvolvimento.")