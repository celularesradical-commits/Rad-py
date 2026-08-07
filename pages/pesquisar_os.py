import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from database import pesquisar_os, supabase


st.set_page_config(
    page_title="Pesquisar Ordem de Serviço",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Pesquisar Ordem de Serviço")


# ===========================
# FORMATAR DATA DA ENTREGA
# ===========================

def formatar_data_entrega(data_entrega):

    if not data_entrega:
        return None

    try:

        data = datetime.fromisoformat(
            str(data_entrega).replace(
                "Z",
                "+00:00"
            )
        )

        if data.tzinfo is None:

            data = data.replace(
                tzinfo=ZoneInfo("America/Sao_Paulo")
            )

        data_brasil = data.astimezone(
            ZoneInfo("America/Sao_Paulo")
        )

        return data_brasil.strftime(
            "%d/%m/%Y às %Hh"
        )

    except (ValueError, TypeError):

        return str(data_entrega)


# ===========================
# REGISTRAR ENTREGA
# ===========================

def registrar_entrega(numero_os):

    momento_entrega = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).isoformat()

    (
        supabase.table("ordens_servico")
        .update({
            "status": "Entregue",
            "data_entrega": momento_entrega
        })
        .eq("numero_os", numero_os)
        .execute()
    )


# ===========================
# ESTADO
# ===========================

if "resultado_pesquisa" not in st.session_state:

    st.session_state.resultado_pesquisa = []


# ===========================
# MENSAGEM
# ===========================

if "mensagem_pesquisa_os" in st.session_state:

    st.success(
        st.session_state.pop(
            "mensagem_pesquisa_os"
        )
    )


# ===========================
# PESQUISA
# ===========================

pesquisa = st.text_input(
    "Digite o número da OS, cliente, modelo ou contato"
)

if st.button(
    "🔍 Pesquisar",
    use_container_width=True
):

    if pesquisa.strip() == "":

        st.warning(
            "Digite algo para pesquisar."
        )

    else:

        try:

            st.session_state.resultado_pesquisa = (
                pesquisar_os(
                    pesquisa.strip()
                )
            )

        except Exception as erro:

            st.error(
                f"Erro ao pesquisar: {erro}"
            )


st.divider()


# ===========================
# RESULTADOS
# ===========================

if st.session_state.resultado_pesquisa:

    for os in st.session_state.resultado_pesquisa:

        numero_os = os.get(
            "numero_os"
        )

        status = os.get(
            "status",
            ""
        )

        with st.container(border=True):

            st.markdown(
                "## 📄 Ordem de Serviço"
            )

            st.write(
                f"**🆔 Número da OS:** "
                f"{numero_os}"
            )

            st.write(
                f"**👤 Cliente:** "
                f"{os.get('cliente', '')}"
            )

            st.write(
                f"**📱 Modelo:** "
                f"{os.get('modelo', '')}"
            )

            st.write(
                f"**🔧 Defeito:** "
                f"{os.get('defeito', '')}"
            )

            st.write(
                f"**📞 Contato:** "
                f"{os.get('contato', '')}"
            )

            valor = float(
                os.get("valor") or 0
            )

            st.write(
                f"**💰 Valor:** R$ {valor:.2f}"
            )

            st.write(
                f"**📅 Entrada:** "
                f"{os.get('data_entrada', '')}"
            )

            st.write(
                f"**📅 Retirada:** "
                f"{os.get('data_retirada', '')}"
            )

            # ===========================
            # STATUS E DATA DA ENTREGA
            # ===========================

            data_entrega = formatar_data_entrega(
                os.get("data_entrega")
            )

            if (
                status == "Entregue"
                and data_entrega
            ):

                st.write(
                    f"**📌 Status:** Entregue — "
                    f"{data_entrega}"
                )

            else:

                st.write(
                    f"**📌 Status:** {status}"
                )

            observacoes = os.get(
                "observacoes"
            )

            if observacoes:

                st.write(
                    f"**📝 Observações:** "
                    f"{observacoes}"
                )

            st.divider()

            col1, col2, col3 = st.columns(3)


            # ===========================
            # EDITAR
            # ===========================

            with col1:

                if st.button(
                    "✏️ Editar",
                    key=f"editar_{numero_os}",
                    use_container_width=True
                ):

                    st.session_state[
                        "os_editar"
                    ] = numero_os

                    st.switch_page(
                        "pages/editar_reparo.py"
                    )


            # ===========================
            # ENTREGAR
            # ===========================

            with col2:

                if status == "Entregue":

                    st.button(
                        "✅ Entregue",
                        key=f"ja_entregue_{numero_os}",
                        use_container_width=True,
                        disabled=True
                    )

                else:

                    if st.button(
                        "✅ Entregar",
                        key=f"entregar_{numero_os}",
                        use_container_width=True
                    ):

                        try:

                            registrar_entrega(
                                numero_os
                            )

                            st.session_state[
                                "mensagem_pesquisa_os"
                            ] = (
                                "Aparelho entregue "
                                "com sucesso!"
                            )

                            st.session_state[
                                "resultado_pesquisa"
                            ] = pesquisar_os(
                                pesquisa.strip()
                            )

                            st.rerun()

                        except Exception as erro:

                            st.error(
                                f"Erro ao entregar "
                                f"o aparelho: {erro}"
                            )


            # ===========================
            # IMPRIMIR
            # ===========================

            with col3:

                if st.button(
                    "🖨️ Imprimir",
                    key=f"imprimir_{numero_os}",
                    use_container_width=True
                ):

                    st.info(
                        "Função disponível em breve."
                    )


elif pesquisa.strip() != "":

    st.error(
        "Nenhuma Ordem de Serviço encontrada."
    )


# ===========================
# VOLTAR
# ===========================

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):

    st.session_state.pop(
        "resultado_pesquisa",
        None
    )

    st.switch_page("app.py")