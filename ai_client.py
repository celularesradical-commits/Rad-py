import streamlit as st
from google import genai

from prompts import PROMPT
 


class AIOnlineClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

    def pesquisar(self, modelo_aparelho: str) -> str:

        prompt_final = PROMPT.replace(
            "[INSERIR O NOME DO APARELHO AQUI]",
            modelo_aparelho
        )

        resposta = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_final
        )

        return resposta.text

    def analisar_panic(self, conteudo_arquivo: str) -> str:

        prompt_final = (
            PROMPT_PANIC
            + "\n\n"
            + conteudo_arquivo
        )

        resposta = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_final
        )

        return resposta.text