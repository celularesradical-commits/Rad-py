import hmac
import json
import base64
import hashlib
import time

from datetime import datetime, timedelta

import streamlit as st

from database import supabase
from streamlit_cookies_controller import CookieController


# ============================================
# CONFIGURAÇÃO
# ============================================

COOKIE_LOGIN = "radicalsystem_login"

# O navegador/aparelho ficará autorizado
# por 90 dias.
DIAS_LOGIN = 90

SESSION_SECRET = str(
    st.secrets.get(
        "SESSION_SECRET",
        "radicalsystem-chave-temporaria"
    )
)


# ============================================
# COOKIE CONTROLLER
# ============================================

def obter_controller():

    return CookieController(
        key="radicalsystem_auth_cookies"
    )


# ============================================
# CRIAR TOKEN
# ============================================

def criar_token(perfil):

    expiracao = int(
        time.time()
    ) + (
        DIAS_LOGIN
        * 24
        * 60
        * 60
    )

    dados = {
        "id": perfil["id"],
        "exp": expiracao
    }

    dados_json = json.dumps(
        dados,
        separators=(",", ":"),
        ensure_ascii=False
    )

    dados_base64 = base64.urlsafe_b64encode(
        dados_json.encode("utf-8")
    ).decode("utf-8")

    assinatura = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        dados_base64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return (
        f"{dados_base64}."
        f"{assinatura}"
    )


# ============================================
# LER E VALIDAR TOKEN
# ============================================

def ler_token(token):

    try:

        if not token:
            return None

        partes = token.split(".")

        if len(partes) != 2:
            return None

        dados_base64 = partes[0]
        assinatura_recebida = partes[1]

        assinatura_correta = hmac.new(
            SESSION_SECRET.encode("utf-8"),
            dados_base64.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(
            assinatura_recebida,
            assinatura_correta
        ):
            return None

        dados_json = base64.urlsafe_b64decode(
            dados_base64.encode("utf-8")
        ).decode("utf-8")

        dados = json.loads(
            dados_json
        )

        expiracao = dados.get(
            "exp"
        )

        if not expiracao:
            return None

        if int(time.time()) > int(expiracao):
            return None

        if not dados.get("id"):
            return None

        return dados

    except Exception:

        return None


# ============================================
# APLICAR PERFIL NA SESSÃO
# ============================================

def aplicar_login(perfil):

    st.session_state[
        "perfil_id"
    ] = perfil["id"]

    st.session_state[
        "perfil_nome"
    ] = perfil["nome"]

    st.session_state[
        "perfil_loja"
    ] = perfil["loja"]

    st.session_state[
        "logado"
    ] = True


# ============================================
# SALVAR LOGIN NO NAVEGADOR
# ============================================

def salvar_login(perfil):

    aplicar_login(
        perfil
    )

    token = criar_token(
        perfil
    )

    expiracao = (
        datetime.now()
        + timedelta(
            days=DIAS_LOGIN
        )
    )

    try:

        controller = obter_controller()

        controller.set(
            COOKIE_LOGIN,
            token,
            path="/",
            expires=expiracao,
            secure=True,
            same_site="lax"
        )

    except Exception:

        pass


# ============================================
# LER COOKIE
# ============================================

def obter_cookie_login():

    # ----------------------------------------
    # PRIMEIRA OPÇÃO
    # Cookie recebido junto com a sessão
    # do navegador.
    # ----------------------------------------

    try:

        token = st.context.cookies.get(
            COOKIE_LOGIN
        )

        if token:
            return token

    except Exception:

        pass

    # ----------------------------------------
    # SEGUNDA OPÇÃO
    # CookieController como alternativa.
    # ----------------------------------------

    try:

        controller = obter_controller()

        token = controller.get(
            COOKIE_LOGIN
        )

        if token:
            return token

    except Exception:

        pass

    return None


# ============================================
# RECUPERAR LOGIN AUTOMATICAMENTE
# ============================================

def recuperar_login():

    # Já está logado nesta sessão.
    if st.session_state.get(
        "logado",
        False
    ):

        return True

    # Sessão foi perdida.
    # Vamos procurar o cookie.
    token = obter_cookie_login()

    dados = ler_token(
        token
    )

    if not dados:

        return False

    perfil_id = dados.get(
        "id"
    )

    if not perfil_id:

        return False

    # ----------------------------------------
    # Confirmar que o perfil ainda existe
    # e continua ativo.
    # ----------------------------------------

    try:

        resposta = (
            supabase
            .table("perfis")
            .select("*")
            .eq(
                "id",
                perfil_id
            )
            .eq(
                "ativo",
                True
            )
            .limit(1)
            .execute()
        )

    except Exception:

        # Se o Supabase tiver uma falha
        # temporária, não destruímos o cookie.
        return False

    if not resposta.data:

        apagar_login()

        return False

    perfil = resposta.data[0]

    # Reconstrói toda a sessão.
    aplicar_login(
        perfil
    )

    return True


# ============================================
# EXIGIR LOGIN
# ============================================

def exigir_login():

    if recuperar_login():
        return True

    st.switch_page(
        "pages/login.py"
    )

    st.stop()


# ============================================
# LOGOUT
# ============================================

def apagar_login():

    chaves = [
        "perfil_id",
        "perfil_nome",
        "perfil_loja",
        "logado"
    ]

    for chave in chaves:

        st.session_state.pop(
            chave,
            None
        )

    try:

        controller = obter_controller()

        controller.remove(
            COOKIE_LOGIN,
            path="/",
            secure=True,
            same_site="lax"
        )

    except Exception:

        pass