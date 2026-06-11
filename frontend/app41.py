import streamlit as st 

st.set_page_config(page_title="AI Customer Support", layout="wide", page_icon="🤖")

chat_page = st.Page(
    "pages/chat.py",
    title="Chat"
)

admin_page = st.Page(
    "pages/admin.py",
    title="Admin"
)

pg = st.navigation({"Main":[chat_page],"Manage":[ admin_page]})
pg.run()