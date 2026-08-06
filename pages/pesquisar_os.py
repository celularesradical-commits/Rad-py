import streamlit as st
from database import pesquisar_os, entregar_os

st.set_page_config(
    page_title="Pesquisar Ordem de Serviço",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Pesquisar Ordem de Serviço")

# ===========================
# ESTADO
# ===========================

if "resultado_pesquisa" not in st.session_state:
    st.session_state.resultado_pesquisa = []

# ===========================
# PESQUISA
# ===========================

pesquisa = st.text_input(
    "Digite o número da OS, cliente, modelo ou contato"
)

if st.button(
    "🔍 Pesquisar",
    use_container_width=True
):

    if pesquisa.strip() == "":
        st.warning("Digite algo para pesquisar.")
    else:
        st.session_state.resultado_pesquisa = pesquisar_os(pesquisa)

st.divider()

# ===========================
# RESULTADOS
# ===========================

if st.session_state.resultado_pesquisa:

    for os in st.session_state.resultado_pesquisa:

        with st.container(border=True):

            st.markdown("## 📄 Ordem de Serviço")

            st.write(f"**🆔 Número da OS:** {os['numero_os']}")
            st.write(f"**👤 Cliente:** {os['cliente']}")
            st.write(f"**📱 Modelo:** {os['modelo']}")
            st.write(f"**🔧 Defeito:** {os['defeito']}")
            st.write(f"**📞 Contato:** {os['contato']}")
            st.write(f"**💰 Valor:** R$ {float(os['valor']):.2f}")
            st.write(f"**📅 Entrada:** {os['data_entrada']}")
            st.write(f"**📅 Retirada:** {os['data_retirada']}")
            st.write(f"**📌 Status:** {os['status']}")

            if os["observacoes"]:
                st.write(f"**📝 Observações:** {os['observacoes']}")

            st.divider()

            col1, col2, col3 = st.columns(3)

            # ===========================
            # EDITAR
            # ===========================

            with col1:

                if st.button(
                    "✏️ Editar",
                    key=f"editar_{os['numero_os']}",
                    use_container_width=True
                ):

                    st.session_state["os_editar"] = os["numero_os"]

                    st.switch_page("pages/editar_reparo.py")

            # ===========================
            # ENTREGAR
            # ===========================

            with col2:

                if st.button(
                    "✅ Entregar",
                    key=f"entregar_{os['numero_os']}",
                    use_container_width=True
                ):

                    entregar_os(os["numero_os"])

                    st.success("Aparelho entregue com sucesso!")

                    st.session_state.resultado_pesquisa = pesquisar_os(pesquisa)

                    st.rerun()

            # ===========================
            # IMPRIMIR
            # ===========================

            with col3:

                if st.button(
                    "🖨️ Imprimir",
                    key=f"imprimir_{os['numero_os']}",
                    use_container_width=True
                ):

                    st.info("Função disponível em breve.")

elif pesquisa != "":
    st.error("Nenhuma Ordem de Serviço encontrada.")

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):
    st.session_state.pop("resultado_pesquisa", None)
    st.switch_page("app.py")