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

# ============================================
# BOTÃO CONFIGURAR IMPRESSORA
# ============================================

st.components.v1.html(
    """
    <button
        onclick="configurarImpressora()"
        style="
            width:100%;
            padding:12px;
            font-size:16px;
            font-weight:600;
            border-radius:8px;
            border:1px solid #777;
            background:white;
            cursor:pointer;
        "
    >
        🔵 Configurar impressora Bluetooth
    </button>

    <script>
        function configurarImpressora() {
            window.top.location.href =
                "radicalsystem://configurar-impressora";
        }
    </script>
    """,
    height=60
)

# ============================================
# BOTÃO TESTAR IMPRESSÃO
# ============================================

st.components.v1.html(
    """
    <button
        onclick="testarImpressao()"
        style="
            width:100%;
            padding:12px;
            font-size:16px;
            font-weight:600;
            border-radius:8px;
            border:1px solid #777;
            background:white;
            cursor:pointer;
        "
    >
        🧾 Testar impressão
    </button>

    <script>
        function testarImpressao() {
            window.top.location.href =
                "radicalsystem://testar-impressao";
        }
    </script>
    """,
    height=60
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