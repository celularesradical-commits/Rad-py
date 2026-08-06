import streamlit as st
from database import pesquisar_os

st.set_page_config(
    page_title="Pesquisar Reparo",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Pesquisar Reparo")

pesquisa = st.text_input(
    "Digite o número da OS, cliente, modelo ou contato"
)

st.divider()

if st.button("🔍 Pesquisar", use_container_width=True):

    if pesquisa.strip() == "":
        st.warning("Digite algo para pesquisar.")

    else:

        resultados = pesquisar_os(pesquisa)

        if len(resultados) == 0:

            st.error("Nenhum reparo encontrado.")

        else:

            for os in resultados:

                st.container(border=True)

                st.markdown(f"### 📄 Ordem de Serviço {os['numero_os']}")

                st.write(f"**Cliente:** {os['cliente']}")
                st.write(f"**Modelo:** {os['modelo']}")
                st.write(f"**Defeito:** {os['defeito']}")
                st.write(f"**Contato:** {os['contato']}")
                st.write(f"**Valor:** R$ {os['valor']}")
                st.write(f"**Entrada:** {os['data_entrada']}")
                st.write(f"**Retirada:** {os['data_retirada']}")
                st.write(f"**Status:** {os['status']}")

                if os["observacoes"]:
                    st.write(f"**Observações:** {os['observacoes']}")

                st.divider()

st.divider()

if st.button("⬅️ Voltar", use_container_width=True):
    st.switch_page("app.py")