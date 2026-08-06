import streamlit as st
from supabase import create_client

cliente = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SERVICE_KEY"]
)

st.write(cliente.storage)