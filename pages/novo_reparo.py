import streamlit as st

st.set_page_config(
    page_title="Novo Reparo",
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 Novo Reparo")

st.text_input(
    "📱 Modelo do Celular"
)

st.text_input(
    "🔧 Defeito Identificado"
)

st.text_input(
    "💰 Valor do Reparo"
)

st.text_input(
    "👤 Nome do Cliente"
)

st.text_input(
    "📞 Contato do Cliente"
)

st.text_area(
    "📝 Observações Adicionais",
    height=120
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.button(
        "💾 Salvar",
        use_container_width=True
    )

with col2:
    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("pages/ordem_servico.py")