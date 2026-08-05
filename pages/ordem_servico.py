import streamlit as st

st.set_page_config(
    page_title="Ordem de Serviço",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Ordem de Serviço")
st.write("Selecione uma opção:")

st.divider()

if st.button(
    "➕ Novo Reparo",
    use_container_width=True
):
    st.switch_page("pages/novo_reparo.py")

if st.button(
    "🔎 Pesquisar Reparo",
    use_container_width=True
):
    st.switch_page("pages/pesquisar_reparo.py")

if st.button(
    "🔧 Reparos em Andamento",
    use_container_width=True
):
    st.switch_page("pages/reparos_andamento.py")

if st.button(
    "✅ Entregar Aparelho",
    use_container_width=True
):
    st.switch_page("pages/entregar_aparelho.py")

st.divider()

if st.button(
    "⬅️ Voltar ao Menu",
    use_container_width=True
):
    st.switch_page("app.py")