# pages/about.py
import streamlit as st
from utils.helpers import load_settings
from pathlib import Path

def app():
    settings = load_settings().get("about", {})

    title = settings.get("title", "ℹ️ About me")
    name = settings.get("name", "Your Name")
    role = settings.get("role", "")
    details = settings.get("details", [])
    tips_title = settings.get("tips_title", "Portfolio tips")
    tips = settings.get("tips", [])

    st.title(title)
    st.markdown(f"**{name}** — {role}")

    st.markdown("---")
    if details:
        for line in details:
            # details may contain Markdown formatting
            st.markdown(f"- {line}")
    else:
        st.write("Chưa có thông tin chi tiết. Cập nhật `settings.json` để thay đổi nội dung.")

    st.markdown("---")
    st.subheader(tips_title)
    if tips:
        for t in tips:
            st.markdown(f"- {t}")
    else:
        st.write("No tips provided.")
