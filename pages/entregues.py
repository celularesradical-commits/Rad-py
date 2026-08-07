import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from database import supabase


st.set_page_config(
    page_title="Entregues",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Aparelhos Entregues")


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

        data = data.astimezone(
            ZoneInfo("America/Sao_Paulo")
        )

        return data.strftime(
            "%d/%m/%Y às %Hh"
        )

    except Exception:

        return str(data_entrega)


# ===========================
# BUSCAR APARELHOS ENTREGUES
# ===========================

try:

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .eq("status", "Entregue")
        .order("numero_os", desc=True)
        .execute()
    )

    lista = resposta.data or []

except Exception as erro:

    st.error(
        f"Erro ao carregar aparelhos entregues: {erro}"
    )

    lista = []


# ===========================
# EXIBIR RESULTADOS
# ===========================

if len(lista) == 0:

    st.info(
        "Nenhum aparelho entregue."
    )

else:

    for os in lista:

        with st.container(border=True):

            st.markdown(
                "## 📄 Ordem de Serviço"
            )

            st.write(
                f"**🆔 Número da OS:** "
                f"{os.get('numero_os', '')}"
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
                f"**💰 Valor:** "
                f"R$ {valor:.2f}"
            )

            st.write(
                f"**📅 Entrada:** "
                f"{os.get('data_entrada', '')}"
            )

            st.write(
                f"**📅 Retirada prevista:** "
                f"{os.get('data_retirada', '')}"
            )

            st.write(
                f"**📌 Status:** "
                f"{os.get('status', '')}"
            )

            # ===========================
            # DATA REAL DA ENTREGA
            # ===========================

            data_entrega = formatar_data_entrega(
                os.get("data_entrega")
            )

            if data_entrega:

                st.write(
                    f"**🕒 Entregue em:** "
                    f"{data_entrega}"
                )

            else:

                st.write(
                    "**🕒 Entregue em:** "
                    "Data não registrada"
                )

            # ===========================
            # OBSERVAÇÕES
            # ===========================

            observacoes = os.get(
                "observacoes"
            )

            if observacoes:

                st.write(
                    f"**📝 Observações:** "
                    f"{observacoes}"
                )


# ===========================
# VOLTAR
# ===========================

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):

    st.switch_page(
        "pages/ordem_servico.py"
    )