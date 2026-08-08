import streamlit as st

st.set_page_config(
    page_title="Configurações",
    page_icon="⚙️",
    layout="centered"
)

# ============================================
# Verificar Login
# ============================================

if not st.session_state.get("logado", False):
    st.switch_page("pages/login.py")
    st.stop()

# ============================================
# Dados do Perfil
# ============================================

perfil_nome = st.session_state.get(
    "perfil_nome",
    "Usuário"
)

perfil_loja = st.session_state.get(
    "perfil_loja",
    ""
)

# ============================================
# Cabeçalho
# ============================================

st.title("⚙️ Configurações")

st.write(
    f"👤 **Perfil:** {perfil_nome}"
)

st.write(
    f"🏪 **Loja:** {perfil_loja}"
)

st.divider()

# ============================================
# Conta
# ============================================

st.subheader("👤 Conta")

if st.button(
    "🚪 Sair do perfil",
    use_container_width=True
):

    st.session_state.clear()

    st.switch_page(
        "pages/login.py"
    )

# ============================================
# Voltar
# ============================================

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):

    st.switch_page(
        "app.py"
    )