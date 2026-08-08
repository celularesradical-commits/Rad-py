import streamlit as st
from database import supabase
from datetime import datetime

st.set_page_config(
    page_title="Chat Geral",
    page_icon="💬",
    layout="centered"
)

# ============================================
# Verificar Login
# ============================================

if not st.session_state.get("logado", False):
    st.switch_page("pages/login.py")
    st.stop()

perfil_id = st.session_state.get("perfil_id")
perfil_nome = st.session_state.get("perfil_nome")
perfil_loja = st.session_state.get("perfil_loja")

# ============================================
# Cabeçalho
# ============================================

st.title("💬 Chat Geral")

st.caption(
    f"Conectado como {perfil_nome} • {perfil_loja}"
)

# ============================================
# Botões superiores
# ============================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔄 Atualizar",
        use_container_width=True
    ):
        st.rerun()

with col2:

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("app.py")

st.divider()

# ============================================
# Buscar mensagens
# ============================================

try:

    resposta = (
        supabase.table("mensagens")
        .select("*")
        .order("data_hora", desc=True)
        .limit(100)
        .execute()
    )

    mensagens = resposta.data or []

    # Mostrar da mais antiga para a mais nova
    mensagens.reverse()

except Exception as erro:

    st.error(
        f"Erro ao carregar mensagens:\n\n{erro}"
    )

    mensagens = []

# ============================================
# Mostrar mensagens
# ============================================

if not mensagens:

    st.info(
        "Ainda não existem mensagens no chat."
    )

else:

    for mensagem in mensagens:

        nome = mensagem.get(
            "nome",
            "Usuário"
        )

        loja = mensagem.get(
            "loja",
            ""
        )

        texto = mensagem.get(
            "mensagem",
            ""
        )

        data_hora = mensagem.get(
            "data_hora"
        )

        horario = ""

        if data_hora:

            try:

                data_convertida = datetime.fromisoformat(
                    data_hora.replace(
                        "Z",
                        "+00:00"
                    )
                )

                horario = data_convertida.strftime(
                    "%d/%m %H:%M"
                )

            except Exception:
                horario = ""

        # ------------------------------------
        # Minha mensagem
        # ------------------------------------

        if mensagem.get("perfil_id") == perfil_id:

            with st.chat_message("user"):

                st.caption(
                    f"Você • {loja}"
                )

                st.write(texto)

                if horario:
                    st.caption(horario)

        # ------------------------------------
        # Mensagem de outro usuário
        # ------------------------------------

        else:

            with st.chat_message("assistant"):

                st.caption(
                    f"{nome} • {loja}"
                )

                st.write(texto)

                if horario:
                    st.caption(horario)

# ============================================
# Enviar mensagem
# ============================================

mensagem_nova = st.chat_input(
    "Digite uma mensagem..."
)

if mensagem_nova:

    mensagem_nova = mensagem_nova.strip()

    if mensagem_nova:

        try:

            supabase.table(
                "mensagens"
            ).insert(
                {
                    "perfil_id": perfil_id,
                    "nome": perfil_nome,
                    "loja": perfil_loja,
                    "mensagem": mensagem_nova
                }
            ).execute()

            st.rerun()

        except Exception as erro:

            st.error(
                f"Erro ao enviar mensagem:\n\n{erro}"
            )