import streamlit as st

from ai_client import AIOnlineClient
from panic_parser import extrair_resumo

st.set_page_config(
    page_title="Analisador de Panic Full",
    page_icon="📱",
    layout="centered"
)

st.title("📱 Analisador de Panic Full")

st.write(
    "Selecione um arquivo Panic Full (.ips) para identificar o hardware responsável pela reinicialização."
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

                ia = AIOnlineClient()

                with st.spinner("Consultando Gemini..."):

                    resposta = ia.analisar_panic(
                        resumo
                    )

                st.success("Análise concluída!")

                st.markdown(resposta)

            except Exception as erro:

                st.error(
                    f"Erro ao analisar o arquivo:\n\n{erro}"
                )