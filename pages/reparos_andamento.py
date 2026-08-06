import streamlit as st
from database import reparos_em_andamento, entregar_os

st.set_page_config(
    page_title="Reparos em Andamento",
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 Reparos em Andamento")

lista = reparos_em_andamento()

if len(lista) == 0:

    st.success("Nenhum reparo em andamento.")

else:

    for os in lista:

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

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✏️ Editar",
                    key=f"editar_{os['numero_os']}",
                    use_container_width=True
                ):

                    st.session_state["os_editar"] = os["numero_os"]

                    st.switch_page("pages/editar_reparo.py")

            with col2:

                if st.button(
                    "✅ Entregar",
                    key=f"entregar_{os['numero_os']}",
                    use_container_width=True
                ):

                    entregar_os(os["numero_os"])

                    st.success("Aparelho entregue com sucesso.")

                    st.rerun()

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):
    st.switch_page("pages/ordem_servico.py")