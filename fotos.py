import json
import urllib.error
import urllib.parse
import urllib.request

import streamlit as st


# ======================================
# CONFIGURAÇÃO
# ======================================

SUPABASE_URL = str(
    st.secrets["SUPABASE_URL"]
).strip().rstrip("/")

SUPABASE_SERVICE_KEY = str(
    st.secrets["SUPABASE_SERVICE_KEY"]
).strip()

BUCKET = "os-fotos"


# ======================================
# ENVIAR FOTO
# ======================================

def enviar_foto(numero_os, foto):

    if foto is None:
        raise ValueError("Nenhuma foto foi recebida.")

    conteudo = foto.getvalue()

    if not conteudo:
        raise ValueError("A foto capturada está vazia.")

    nome_arquivo = f"{int(numero_os)}.jpg"

    caminho = urllib.parse.quote(
        f"{BUCKET}/{nome_arquivo}",
        safe="/"
    )

    url = (
        f"{SUPABASE_URL}/storage/v1/object/"
        f"{caminho}"
    )

    cabecalhos = {
        "Authorization": str(
            f"Bearer {SUPABASE_SERVICE_KEY}"
        ),
        "apikey": str(
            SUPABASE_SERVICE_KEY
        ),
        "Content-Type": str(
            "image/jpeg"
        )
    }

    requisicao = urllib.request.Request(
        url=str(url),
        data=conteudo,
        headers=cabecalhos,
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            requisicao,
            timeout=60
        ) as resposta:

            codigo = resposta.getcode()

            if codigo not in (200, 201):
                raise RuntimeError(
                    f"Falha no upload. Código HTTP: {codigo}"
                )

            return True

    except urllib.error.HTTPError as erro:

        detalhe = erro.read().decode(
            "utf-8",
            errors="replace"
        )

        try:

            dados_erro = json.loads(detalhe)

            mensagem = (
                dados_erro.get("message")
                or dados_erro.get("error")
                or detalhe
            )

        except Exception:

            mensagem = detalhe

        raise RuntimeError(
            f"Erro do Supabase Storage: {mensagem}"
        ) from erro

    except urllib.error.URLError as erro:

        raise RuntimeError(
            f"Não foi possível conectar ao Supabase: "
            f"{erro.reason}"
        ) from erro


# ======================================
# OBTER URL PÚBLICA
# ======================================

def obter_url_foto(numero_os):

    nome_arquivo = f"{int(numero_os)}.jpg"

    caminho = urllib.parse.quote(
        f"{BUCKET}/{nome_arquivo}",
        safe="/"
    )

    return (
        f"{SUPABASE_URL}/storage/v1/object/public/"
        f"{caminho}"
    )