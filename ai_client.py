import streamlit as st
import google.generativeai as genai

from prompts import PROMPT


class AIOnlineClient:
    def __init__(self):
        api_key = st.secrets["GEMINI_API_KEY"]

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def pesquisar(self, modelo_aparelho: str) -> str:
        prompt_final = PROMPT.replace(
            "[INSERIR O NOME DO APARELHO AQUI]",
            modelo_aparelho
        )

        resposta = self.model.generate_content(prompt_final)

        return resposta.text