import streamlit as st
from datetime import date
from database import supabase

# ============================================
# Configuração da página
# ============================================

st.set_page_config(
    page_title="RadicalSystem",
    page_icon="📱",
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
# Contador da Agenda
# ============================================

hoje = date.today().isoformat()

try:

    resposta = (
        supabase.table("ordens_servico")
        .select("numero_os")
        .eq("status", "Em andamento")
        .eq("data_retirada", hoje)
        .execute()
    )

    agenda_hoje = len(resposta.data)

except Exception:

    agenda_hoje = 0

# ============================================
# Cabeçalho
# ============================================

st.title("📱 RadicalSystem")
st.subheader("Sistema de Gestão para Assistência Técnica")

st.markdown("---")

# ============================================
# Perfil Logado
# ============================================

st.write(
    f"👤 **{perfil_nome}** • 🏪 **{perfil_loja}**"
)

st.markdown("---")

st.write("Selecione um módulo abaixo:")

# ============================================
# Botões
# ============================================

if st.button(
    "📋 Ordem de Serviço",
    use_container_width=True
):
    st.switch_page("pages/novo_reparo.py")

if st.button(
    "🔎 Pesquisar Reparo",
    use_container_width=True
):
    st.switch_page("pages/pesquisar_os.py")

if st.button(
    "🛠️ Reparos em Andamento",
    use_container_width=True
):
    st.switch_page("pages/reparos_andamento.py")

if st.button(
    "✅ Entregues",
    use_container_width=True
):
    st.switch_page("pages/entregues.py")

if st.button(
    "🔍 Pesquisar Películas",
    use_container_width=True
):
    st.switch_page("pages/peliculas.py")

if st.button(
    f"📅 Agenda ({agenda_hoje})",
    use_container_width=True
):
    st.switch_page("pages/agenda.py")

if st.button(
    "💬 Chat Geral",
    use_container_width=True
):
    st.switch_page("pages/chat.py")

if st.button(
    "📱 Analisar Panic Full",
    use_container_width=True
):
    st.switch_page("pages/panic_full.py")

if st.button(
    "📦 Estoque",
    use_container_width=True
):
    st.switch_page("pages/estoque.py")

if st.button(
    "💰 PDV",
    use_container_width=True
):
    st.switch_page("pages/pdv.py")

if st.button(
    "📊 Relatórios",
    use_container_width=True
):
    st.switch_page("pages/relatorios.py")

if st.button(
    "⚙️ Configurações",
    use_container_width=True
):
    st.switch_page("pages/configuracoes.py")

# ============================================
# Rodapé
# ============================================

st.markdown("---")

st.caption(
    f"Radical Celulares • RadicalSystem • "
    f"{perfil_nome} • {perfil_loja}"
)