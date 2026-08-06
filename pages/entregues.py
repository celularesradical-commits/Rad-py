import streamlit as st
from database import supabase

st.set_page_config(
    page_title="Entregues",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Aparelhos Entregues")

resposta = (
    supabase.table("ordens_servico")
    .select("*")
    .eq("status", "Entregue")
    .order("numero_os", desc=True)
    .execute()
)

lista = resposta.data

if len(lista) == 0:

    st.info("Nenhum aparelho entregue.")

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

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):
    st.switch_page("pages/ordem_servico.py")