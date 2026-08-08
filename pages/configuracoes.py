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

st.caption(
    f"👤 {perfil_nome} • 🏪 {perfil_loja}"
)

st.divider()

# ============================================
# Impressora
# ============================================

st.subheader("🖨️ Impressora")

st.write(
    "Configure a impressora térmica Bluetooth "
    "utilizada neste aparelho."
)

if st.button(
    "🔵 Configurar impressora Bluetooth",
    use_container_width=True
):
    st.query_params["configurar_impressora"] = "1"

    st.info(
        "Abrindo configuração da impressora..."
    )

st.caption(
    "A impressora será configurada individualmente "
    "em cada celular Android."
)

st.divider()

# ============================================
# Conta
# ============================================

st.subheader("👤 Conta")

st.write(f"**Perfil:** {perfil_nome}")
st.write(f"**Loja atual:** {perfil_loja}")

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