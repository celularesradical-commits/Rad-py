import json
import urllib.error
import urllib.parse
import urllib.request

import streamlit as st


# ======================================
# CONFIGURAÇÃO
# ======================================

SUPABASE_URL = st.secrets["SUPABASE_URL"].rstrip("/")
SUPABASE_SERVICE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

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

    requisicao = urllib.request.Request(
        url=url,
        data=conteudo,
        method="POST",
        headers={
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "apikey": SUPABASE_SERVICE_KEY,
            "Content-Type": "image/jpeg",
            "x-upsert": "false"
        }
    )

    try:

        with urllib.request.urlopen(
            requisicao,
            timeout=60
        ) as resposta:

            if resposta.status not in (200, 201):
                raise RuntimeError(
                    f"Falha no upload. Código: {resposta.status}"
                )

        return True

    except urllib.error.HTTPError as erro:

        detalhe = erro.read().decode(
            "utf-8",
            errors="replace"
        )

        try:
            detalhe_json = json.loads(detalhe)
            mensagem = (
                detalhe_json.get("message")
                or detalhe_json.get("error")
                or detalhe
            )
        except json.JSONDecodeError:
            mensagem = detalhe

        raise RuntimeError(
            f"Erro ao enviar a foto: {mensagem}"
        ) from erro

    except urllib.error.URLError as erro:

        raise RuntimeError(
            f"Não foi possível conectar ao Storage: {erro.reason}"
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