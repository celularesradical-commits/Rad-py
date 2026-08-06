import streamlit as st
from supabase import create_client

# ======================================
# SUPABASE
# ======================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

BUCKET = "os-fotos"


# ======================================
# ENVIAR FOTO
# ======================================

def enviar_foto(numero_os, foto):

    try:

        if foto is None:
            st.error("Nenhuma foto foi recebida.")
            return False

        nome = f"{numero_os}.jpg"

        st.write(f"📤 Enviando foto: {nome}")

        resposta = supabase.storage.from_(BUCKET).upload(
            path=nome,
            file=foto.getvalue(),
            file_options={
                "content-type": "image/jpeg",
                "upsert": "true"
            }
        )

        st.success("✅ Foto enviada com sucesso!")

        return resposta

    except Exception as erro:

        st.error(f"❌ Erro ao enviar foto:\n\n{erro}")

        return False


# ======================================
# OBTER URL
# ======================================

def obter_url_foto(numero_os):

    nome = f"{numero_os}.jpg"

    return supabase.storage.from_(BUCKET).get_public_url(nome)