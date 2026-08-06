import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)

BUCKET = "os-fotos"


def enviar_foto(numero_os, foto):

    st.error(">>> ENTROU EM enviar_foto() <<<")

    if foto is None:
        st.error("Foto é None.")
        return False

    nome = f"{numero_os}.jpg"

    st.write(f"Arquivo: {nome}")

    try:

        resposta = supabase.storage.from_(BUCKET).upload(
            nome,
            foto.getvalue()
        )

        st.success("UPLOAD OK")

        st.write(resposta)

        return True

    except Exception as erro:

        st.error(erro)

        return False


def obter_url_foto(numero_os):

    nome = f"{numero_os}.jpg"

    return supabase.storage.from_(BUCKET).get_public_url(nome)