# pages/resume.py
import streamlit as st
from pathlib import Path
import base64
from utils.helpers import load_settings

def app():
    settings = load_settings()
    resume_cfg = settings.get("resume", {})

    resume_path = Path(resume_cfg.get("path", "assets/resume/Data Analyst_Analytics Engineering.pdf"))
    resume_title = resume_cfg.get("title", "Resume / CV")

    st.title(f"📄 {resume_title}")

    if resume_path.exists():
        # Hiển thị nút tải về
        with open(resume_path, "rb") as f:
            pdf_bytes = f.read()
            st.download_button(
                "📥 Tải CV",
                data=pdf_bytes,
                file_name=resume_path.name,
                mime="application/pdf"
            )

        # Hiển thị trực tiếp file PDF trong giao diện
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" height="800" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

    else:
        st.warning(f"⚠️ CV chưa có. Hãy đặt file vào `{resume_path}`")
