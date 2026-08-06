import streamlit as st

from panic_parser import extrair_resumo

st.set_page_config(
    page_title="Analisador de Panic Full",
    page_icon="📱",
    layout="centered"
)

st.title("📱 Analisador de Panic Full")

st.write(
    "Selecione um arquivo Panic Full (.ips)."
)

arquivo = st.file_uploader(
    "Selecione o arquivo Panic Full"
)

if arquivo is not None:

    st.success(f"Arquivo selecionado: {arquivo.name}")

    if st.button(
        "🔍 Analisar",
        use_container_width=True
    ):

        with st.spinner("Extraindo informações do arquivo..."):

            try:

                conteudo = arquivo.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                resumo = extrair_resumo(
                    conteudo
                )

                if not resumo.strip():

                    st.error(
                        "Não foi possível extrair informações do Panic Full."
                    )

                    st.stop()

                st.success("Resumo técnico gerado com sucesso!")

                st.text_area(
                    "Resumo Técnico",
                    resumo,
                    height=600
                )

            except Exception as erro:

                st.error(
                    f"Erro ao analisar o arquivo:\n\n{erro}"
                )