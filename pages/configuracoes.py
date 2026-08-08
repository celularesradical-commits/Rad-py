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

st.markdown(
    """
    <a href="radicalsystem://configurar-impressora"
       style="
       display:block;
       text-align:center;
       padding:0.65rem;
       margin-bottom:0.6rem;
       border:1px solid rgba(128,128,128,0.4);
       border-radius:0.5rem;
       text-decoration:none;
       font-weight:600;
       ">
       🔵 Configurar impressora Bluetooth
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <a href="radicalsystem://testar-impressao"
       style="
       display:block;
       text-align:center;
       padding:0.65rem;
       border:1px solid rgba(128,128,128,0.4);
       border-radius:0.5rem;
       text-decoration:none;
       font-weight:600;
       ">
       🧾 Testar impressão
    </a>
    """,
    unsafe_allow_html=True
)

st.caption(
    "A impressora é configurada individualmente "
    "em cada aparelho Android."
)

st.divider()

# ============================================
# Conta
# ============================================

st.subheader("👤 Conta")

st.caption(
    f"{perfil_nome} • {perfil_loja}"
)

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