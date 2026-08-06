import streamlit as st
from supabase import create_client

# =====================================
# SUPABASE STORAGE
# =====================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SERVICE_KEY"]
)

BUCKET = "os-fotos"


# =====================================
# ENVIAR FOTO
# =====================================

def enviar_foto(numero_os, foto):

    if foto is None:
        return False

    nome = f"{numero_os}.jpg"

    supabase.storage.from_(BUCKET).upload(
        nome,
        foto.getvalue(),
        file_options={
            "content-type": "image/jpeg",
            "upsert": True
        }
    )

    return True


# =====================================
# URL DA FOTO
# =====================================

def obter_url_foto(numero_os):

    nome = f"{numero_os}.jpg"

    return supabase.storage.from_(BUCKET).get_public_url(nome)