import streamlit as st
from database import buscar_os, editar_os

st.set_page_config(
    page_title="Editar Reparo",
    page_icon="✏️",
    layout="centered"
)

# ===========================
# VERIFICA SE EXISTE UMA OS
# ===========================

if "os_editar" not in st.session_state:

    st.error("Nenhuma Ordem de Serviço selecionada.")

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("pages/pesquisar_reparo.py")

    st.stop()

numero = st.session_state["os_editar"]

os = buscar_os(numero)

if os is None:

    st.error("Ordem de Serviço não encontrada.")

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.session_state.pop("os_editar", None)
        st.switch_page("pages/pesquisar_reparo.py")

    st.stop()

# ===========================
# TÍTULO
# ===========================

st.title("✏️ Editar Ordem de Serviço")

# ===========================
# CAMPOS
# ===========================

st.text_input(
    "🆔 Número da OS",
    value=str(os["numero_os"]),
    disabled=True
)

st.text_input(
    "👤 Cliente",
    value=os["cliente"],
    disabled=True
)

st.text_input(
    "📱 Modelo",
    value=os["modelo"],
    disabled=True
)

st.text_area(
    "🔧 Defeito",
    value=os["defeito"],
    disabled=True
)

st.text_input(
    "📞 Contato",
    value=os["contato"],
    disabled=True
)

valor = st.number_input(
    "💰 Valor",
    value=float(os["valor"]),
    step=1.0,
    format="%.0f"
)

retirada = st.date_input(
    "📅 Data Prevista de Retirada",
    value=os["data_retirada"]
)

observacoes = st.text_area(
    "📝 Observações",
    value=os["observacoes"] or "",
    height=150
)

st.divider()

col1, col2 = st.columns(2)

# ===========================
# SALVAR
# ===========================

with col1:

    if st.button(
        "💾 Salvar Alterações",
        use_container_width=True
    ):

        editar_os(
            numero,
            valor,
            observacoes,
            retirada
        )

        st.session_state.pop("os_editar", None)

        st.success("Alterações salvas com sucesso!")

        st.switch_page("pages/pesquisar_reparo.py")

# ===========================
# VOLTAR
# ===========================

with col2:

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):

        st.session_state.pop("os_editar", None)

        st.switch_page("pages/pesquisar_reparo.py")