import streamlit as st
from supabase import create_client

# ======================================
# CONFIGURAÇÃO DO SUPABASE STORAGE
# ======================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase_fotos = create_client(
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

    nome_arquivo = f"{int(numero_os)}.jpg"
    conteudo = foto.getvalue()

    if not conteudo:
        raise ValueError("A foto capturada está vazia.")

    resposta = (
        supabase_fotos.storage
        .from_(BUCKET)
        .upload(
            path=nome_arquivo,
            file=conteudo,
            file_options={
                "content-type": "image/jpeg"
            }
        )
    )

    return resposta


# ======================================
# OBTER URL PÚBLICA DA FOTO
# ======================================

def obter_url_foto(numero_os):

    nome_arquivo = f"{int(numero_os)}.jpg"

    return (
        supabase_fotos.storage
        .from_(BUCKET)
        .get_public_url(nome_arquivo)
    )