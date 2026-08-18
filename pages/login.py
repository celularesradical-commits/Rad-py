import hmac
import streamlit as st

from database import supabase
from auth import recuperar_login, salvar_login


st.set_page_config(
    page_title="Entrar",
    page_icon="👤",
    layout="centered"
)


# ============================================
# RECUPERAR LOGIN AUTOMATICAMENTE
# ============================================

if recuperar_login():

    st.switch_page(
        "app.py"
    )

    st.stop()


# ============================================
# TELA
# ============================================

st.title("👤 RadicalSystem")
st.subheader("Entrar no perfil")


# ============================================
# CÓDIGO DE CONVITE
# ============================================

CODIGO_CONVITE = str(
    st.secrets.get(
        "CODIGO_CONVITE",
        ""
    )
)


# ============================================
# BUSCAR PERFIS
# ============================================

try:

    resposta = (
        supabase
        .table("perfis")
        .select("*")
        .eq(
            "ativo",
            True
        )
        .order(
            "nome"
        )
        .execute()
    )

    perfis = resposta.data or []

except Exception as erro:

    st.error(
        f"Erro ao carregar os perfis:\n\n{erro}"
    )

    st.stop()


# ============================================
# LOGIN
# ============================================

if perfis:

    nomes = [
        perfil["nome"]
        for perfil in perfis
    ]

    nome_escolhido = st.selectbox(
        "👤 Usuário",
        nomes
    )

    pin_digitado = st.text_input(
        "🔑 PIN",
        type="password",
        max_chars=4
    )

    if st.button(
        "Entrar",
        use_container_width=True
    ):

        perfil = next(
            (
                item
                for item in perfis
                if item["nome"]
                == nome_escolhido
            ),
            None
        )

        if perfil is None:

            st.error(
                "Perfil não encontrado."
            )

        elif (
            str(perfil["pin"])
            != pin_digitado
        ):

            st.error(
                "PIN incorreto."
            )

        else:

            # =================================
            # SALVA SESSÃO + COOKIE
            # =================================

            salvar_login(
                perfil
            )

            st.switch_page(
                "app.py"
            )

            st.stop()

else:

    st.info(
        "Nenhum perfil cadastrado."
    )


# ============================================
# CRIAR NOVO PERFIL
# ============================================

st.divider()

if (
    "mostrar_cadastro"
    not in st.session_state
):

    st.session_state[
        "mostrar_cadastro"
    ] = False


if not st.session_state[
    "mostrar_cadastro"
]:

    if st.button(
        "➕ Criar novo perfil",
        use_container_width=True
    ):

        st.session_state[
            "mostrar_cadastro"
        ] = True

        st.rerun()

else:

    st.subheader(
        "➕ Criar novo perfil"
    )

    codigo_digitado = st.text_input(
        "🔐 Código de convite",
        type="password"
    )

    nome = st.text_input(
        "👤 Nome do usuário"
    )

    loja = st.selectbox(
        "🏪 Loja",
        [
            "Loja 1",
            "Loja 2"
        ]
    )

    pin = st.text_input(
        "🔑 PIN de 4 dígitos",
        type="password",
        max_chars=4
    )

    confirmar_pin = st.text_input(
        "🔑 Confirmar PIN",
        type="password",
        max_chars=4
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Criar perfil",
            use_container_width=True
        ):

            if not CODIGO_CONVITE:

                st.error(
                    "O código de convite ainda não foi "
                    "configurado nos Secrets."
                )

            elif not hmac.compare_digest(
                codigo_digitado,
                CODIGO_CONVITE
            ):

                st.error(
                    "Código de convite incorreto."
                )

            elif not nome.strip():

                st.warning(
                    "Digite o nome do usuário."
                )

            elif (
                len(pin) != 4
                or not pin.isdigit()
            ):

                st.warning(
                    "O PIN deve ter exatamente 4 números."
                )

            elif pin != confirmar_pin:

                st.warning(
                    "Os PINs não conferem."
                )

            elif any(
                perfil["nome"]
                .strip()
                .lower()
                ==
                nome.strip().lower()
                for perfil in perfis
            ):

                st.warning(
                    "Já existe um perfil com esse nome."
                )

            else:

                try:

                    supabase.table(
                        "perfis"
                    ).insert(
                        {
                            "nome":
                                nome.strip(),

                            "pin":
                                pin,

                            "loja":
                                loja,

                            "ativo":
                                True
                        }
                    ).execute()

                    st.session_state[
                        "mostrar_cadastro"
                    ] = False

                    st.success(
                        "✅ Perfil criado com sucesso."
                    )

                    st.rerun()

                except Exception as erro:

                    st.error(
                        f"Erro ao criar perfil:\n\n{erro}"
                    )

    with col2:

        if st.button(
            "❌ Cancelar",
            use_container_width=True
        ):

            st.session_state[
                "mostrar_cadastro"
            ] = False

            st.rerun()