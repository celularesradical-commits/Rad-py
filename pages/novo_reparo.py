import streamlit as st
from database import salvar_os

st.set_page_config(
    page_title="Novo Reparo",
    page_icon="🔧",
    layout="centered"
)

# -------------------------
# Estado da página
# -------------------------

if "os_salva" not in st.session_state:
    st.session_state.os_salva = False

if "numero_os" not in st.session_state:
    st.session_state.numero_os = None


# -------------------------
# Após salvar
# -------------------------

if st.session_state.os_salva:

    st.success(
        f"✅ Nota salva com sucesso!\n\n"
        f"Ordem de Serviço Nº {st.session_state.numero_os}"
    )

    if st.button(
        "OK",
        use_container_width=True
    ):
        st.session_state.os_salva = False
        st.session_state.numero_os = None
        st.switch_page("app.py")

    st.stop()


# -------------------------
# Tela principal
# -------------------------

st.title("🔧 Novo Reparo")

modelo = st.text_input(
    "📱 Modelo do Celular"
)

defeito = st.text_area(
    "🔧 Defeito Identificado",
    height=100
)

valor = st.number_input(
    "💰 Valor do Reparo",
    min_value=0.0,
    step=1.0,
    format="%.2f"
)

cliente = st.text_input(
    "👤 Nome do Cliente"
)

contato = st.text_input(
    "📞 Contato do Cliente"
)

data_retirada = st.date_input(
    "📅 Data Prevista para Retirada"
)

observacoes = st.text_area(
    "📝 Observações Adicionais",
    height=120
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "💾 Salvar",
        use_container_width=True
    ):

        if modelo == "" or cliente == "":

            st.warning(
                "Preencha pelo menos o modelo e o nome do cliente."
            )

        else:

            try:

                numero = salvar_os(
                    modelo=modelo,
                    defeito=defeito,
                    valor=valor,
                    cliente=cliente,
                    contato=contato,
                    retirada=data_retirada,
                    observacoes=observacoes
                )

                st.session_state.numero_os = numero
                st.session_state.os_salva = True

                st.rerun()

            except Exception as erro:

                st.error(
                    f"Erro ao salvar:\n\n{erro}"
                )


with col2:

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("app.py")