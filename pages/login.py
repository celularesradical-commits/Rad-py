import streamlit as st
from database import supabase

st.set_page_config(
    page_title="Entrar",
    page_icon="👤",
    layout="centered"
)

st.title("👤 RadicalSystem")
st.subheader("Entrar no perfil")

# ===========================
# BUSCAR PERFIS ATIVOS
# ===========================

try:

    resposta = (
        supabase.table("perfis")
        .select("*")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )

    perfis = resposta.data or []

except Exception as erro:

    st.error(
        f"Erro ao carregar os perfis:\n\n{erro}"
    )

    st.stop()


# ===========================
# PRIMEIRO PERFIL
# ===========================

if not perfis:

    st.info(
        "Nenhum perfil cadastrado. "
        "Crie o primeiro perfil."
    )

    nome = st.text_input(
        "👤 Nome"
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

    if st.button(
        "➕ Criar primeiro perfil",
        use_container_width=True
    ):

        if not nome.strip():

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

        else:

            try:

                supabase.table(
                    "perfis"
                ).insert(
                    {
                        "nome": nome.strip(),
                        "pin": pin,
                        "loja": loja,
                        "ativo": True
                    }
                ).execute()

                st.success(
                    "✅ Perfil criado com sucesso."
                )

                st.rerun()

            except Exception as erro:

                st.error(
                    f"Erro ao criar perfil:\n\n{erro}"
                )

    st.stop()


# ===========================
# LOGIN
# ===========================

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
            if item["nome"] == nome_escolhido
        ),
        None
    )

    if perfil is None:

        st.error(
            "Perfil não encontrado."
        )

    elif str(perfil["pin"]) != pin_digitado:

        st.error(
            "PIN incorreto."
        )

    else:

        st.session_state["perfil_id"] = perfil["id"]
        st.session_state["perfil_nome"] = perfil["nome"]
        st.session_state["perfil_loja"] = perfil["loja"]
        st.session_state["logado"] = True

        st.switch_page("app.py")