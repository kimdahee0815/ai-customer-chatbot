import streamlit as st

st.set_page_config(page_title="AI Customer Support", layout="wide")

def build_navigation()->None:
    pages = [
        st.Page("pages/chat.py", title="Chat"),
        st.Page("pages/admin.py", title="Admin"),
        st.Page("pages/documents.py", title="문서 분석"),
        st.Page("pages/settings.py", title="Settings"),
        st.Page("pages/dashboard.py", title="DashBoard")
    ]

    navigation = st.navigation(pages)
    navigation.run()
    
build_navigation()

