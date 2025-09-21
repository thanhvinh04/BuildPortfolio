# pages/resume.py
import streamlit as st
from utils.helpers import load_settings
import base64
import requests
from pathlib import Path

def st_pdf(pdf_path_or_url, width="100%", height=800):
    """
    Hiển thị PDF trong Streamlit với iframe + download button.
    pdf_path_or_url: đường dẫn local hoặc URL (raw link)
    """
    # Load file
    if str(pdf_path_or_url).startswith("http"):
        # từ URL
        try:
            pdf_bytes = requests.get(pdf_path_or_url).content
        except Exception as e:
            st.error(f"Không thể tải PDF từ URL: {e}")
            return
        file_name = pdf_path_or_url.split("/")[-1]
    else:
        # từ local
        p = Path(pdf_path_or_url)
        if not p.exists():
            st.error(f"File PDF không tồn tại: {pdf_path_or_url}")
            return
        pdf_bytes = p.read_bytes()
        file_name = p.name

    # Embed PDF trực tiếp bằng Base64
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{b64_pdf}" 
                width="{width}" height="{height}" type="application/pdf" 
                style="border-radius:10px; border:1px solid #ddd;"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="📥 Tải CV",
        data=pdf_bytes,
        file_name=file_name,
        mime="application/pdf"
    )

def app():
    settings = load_settings()
    resume_cfg = settings.get("resume", {})

    resume_path = resume_cfg.get("path")
    resume_title = resume_cfg.get("title", "Resume / CV")

    st.title(f"📄 {resume_title}")

    if resume_path:
        st_pdf(resume_path, width="100%", height=800)
    else:
        st.warning("⚠️ CV chưa có đường dẫn trong settings.json")
