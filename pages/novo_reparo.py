import streamlit as st
from database import salvar_os, gerar_numero_os
from fotos import enviar_foto

st.set_page_config(
    page_title="Novo Reparo",
    page_icon="🔧",
    layout="centered"
)

# -------------------------
# Número da próxima OS
# -------------------------

if "proxima_os" not in st.session_state:
    st.session_state.proxima_os = gerar_numero_os()

# -------------------------
# Após salvar
# -------------------------

if st.session_state.get("os_salva", False):

    if st.session_state.get("foto_salva", False):
        st.success(
            f"✅ Nota e foto salvas com sucesso!\n\n"
            f"Ordem de Serviço Nº {st.session_state.numero_os}"
        )
    else:
        st.success(
            f"✅ Nota salva com sucesso!\n\n"
            f"Ordem de Serviço Nº {st.session_state.numero_os}"
        )

    if st.button(
        "OK",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")

    st.stop()

# -------------------------
# Tela
# -------------------------

st.title("🔧 Novo Reparo")

st.text_input(
    "📄 Número da Ordem de Serviço",
    value=str(st.session_state.proxima_os),
    disabled=True
)

modelo = st.text_input(
    "📱 Modelo do Celular"
)

defeito = st.text_area(
    "🔧 Defeito Identificado",
    height=100
)

valor = st.number_input(
    "💰 Valor do Reparo",
    min_value=1.0,
    step=1.0,
    format="%.0f"
)

cliente = st.text_input(
    "👤 Nome do Cliente"
)

contato = st.text_input(
    "📞 Contato"
)

data_retirada = st.date_input(
    "📅 Data Prevista de Retirada"
)

observacoes = st.text_area(
    "📝 Observações",
    height=120
)

# -------------------------
# Foto
# -------------------------

st.divider()

st.subheader("📸 Foto do Aparelho")

foto = st.camera_input(
    "Fotografar aparelho"
)

if foto is not None:
    st.image(
        foto,
        caption="Foto capturada",
        use_container_width=True
    )

# -------------------------
# Botões
# -------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "💾 Salvar",
        use_container_width=True
    ):

        if modelo.strip() == "" or cliente.strip() == "":
            st.warning(
                "Preencha o modelo e o nome do cliente."
            )

        elif foto is None:
            st.warning(
                "Tire uma foto do aparelho antes de salvar."
            )

        else:

            try:

                numero = salvar_os(
                    modelo,
                    defeito,
                    valor,
                    cliente,
                    contato,
                    data_retirada,
                    observacoes
                )

                try:

                    resultado_foto = enviar_foto(
                        numero,
                        foto
                    )

                    if resultado_foto is not True:
                        raise RuntimeError(
                            f"Resposta inesperada do envio: {resultado_foto}"
                        )

                    st.session_state.numero_os = numero
                    st.session_state.foto_salva = True
                    st.session_state.os_salva = True

                    st.rerun()

                except Exception as erro_foto:

                    st.error(
                        f"A OS Nº {numero} foi salva, "
                        f"mas a foto não foi enviada.\n\n"
                        f"Erro: {erro_foto}"
                    )

            except Exception as erro:

                st.error(
                    f"Erro ao salvar a ordem de serviço:\n\n{erro}"
                )

with col2:

    if st.button(
        "⬅️ Voltar",
        use_container_width=True
    ):
        st.switch_page("app.py")