import streamlit as st
from supabase import create_client

# ======================================
# CONFIGURAÇÃO DO SUPABASE STORAGE
# ======================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)

BUCKET = "os-fotos"


# ======================================
# ENVIAR FOTO
# ======================================

def enviar_foto(numero_os, foto):

    if foto is None:
        raise ValueError("Nenhuma foto foi recebida.")

    nome_arquivo = f"{numero_os}.jpg"

    resposta = supabase.storage.from_(BUCKET).upload(
        path=nome_arquivo,
        file=foto.getvalue(),
        file_options={
            "content-type": "image/jpeg",
            "upsert": "true"
        }
    )

    return resposta


# ======================================
# OBTER URL PÚBLICA DA FOTO
# ======================================

def obter_url_foto(numero_os):

    nome_arquivo = f"{numero_os}.jpg"

    return supabase.storage.from_(BUCKET).get_public_url(
        nome_arquivo
    )