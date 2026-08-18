import hmac
import json
import base64
import hashlib
import time

from datetime import datetime, timedelta, timezone

import streamlit as st

from database import supabase
from streamlit_cookies_controller import CookieController


# ============================================
# CONFIGURAÇÃO
# ============================================

COOKIE_LOGIN = "radicalsystem_login"

DIAS_LOGIN = 90

MAX_AGE_LOGIN = (
    DIAS_LOGIN
    * 24
    * 60
    * 60
)

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

    expiracao = (
        int(time.time())
        + MAX_AGE_LOGIN
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
# LER TOKEN
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
# APLICAR LOGIN
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
# GRAVAR COOKIE PERSISTENTE
# ============================================

def gravar_cookie(perfil):

    token = criar_token(
        perfil
    )

    expiracao = (
        datetime.now(
            timezone.utc
        )
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
            max_age=MAX_AGE_LOGIN,
            secure=True,
            same_site="lax"
        )

        st.session_state[
            "_cookie_login_gravado"
        ] = True

    except Exception:

        pass


# ============================================
# SALVAR LOGIN
# ============================================

def salvar_login(perfil):

    aplicar_login(
        perfil
    )

    gravar_cookie(
        perfil
    )


# ============================================
# BUSCAR COOKIE
# ============================================

def obter_cookie_login():

    # ----------------------------------------
    # COOKIE ENVIADO NO INÍCIO DA SESSÃO
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
    # COOKIE CONTROLLER
    # ----------------------------------------

    try:

        controller = obter_controller()

        controller.refresh()

        token = controller.get(
            COOKIE_LOGIN
        )

        if token:
            return token

    except Exception:

        pass

    return None


# ============================================
# RECUPERAR LOGIN
# ============================================

def recuperar_login():

    # ========================================
    # JÁ ESTÁ LOGADO
    # ========================================

    if st.session_state.get(
        "logado",
        False
    ):

        # Reforça o cookie uma vez por sessão.
        if not st.session_state.get(
            "_cookie_login_gravado",
            False
        ):

            perfil = {
                "id":
                    st.session_state.get(
                        "perfil_id"
                    ),

                "nome":
                    st.session_state.get(
                        "perfil_nome"
                    ),

                "loja":
                    st.session_state.get(
                        "perfil_loja"
                    )
            }

            if perfil["id"]:

                gravar_cookie(
                    perfil
                )

        return True


    # ========================================
    # PROCURAR COOKIE
    # ========================================

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


    # ========================================
    # VALIDAR PERFIL NO SUPABASE
    # ========================================

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

        return False


    if not resposta.data:

        apagar_login()

        return False


    perfil = resposta.data[0]


    # ========================================
    # RECONSTRUIR SESSÃO
    # ========================================

    aplicar_login(
        perfil
    )


    # ========================================
    # RENOVAR COOKIE
    # ========================================

    gravar_cookie(
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
# SAIR
# ============================================

def apagar_login():

    chaves = [
        "perfil_id",
        "perfil_nome",
        "perfil_loja",
        "logado",
        "_cookie_login_gravado"
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