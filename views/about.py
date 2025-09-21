# pages/about.py
import streamlit as st

def app():
    st.title("ℹ️ About me")
    st.markdown("**Nguyễn Thành Vinh** — Data Analyst / Machine Learning Engineer")
    st.write("""
    - **Học vấn:** Cử nhân Khoa học máy tính (viết chi tiết)
    - **Kinh nghiệm:** Analytics, Computer Vision, OCR pipeline
    - **Kỹ năng:** Python, SQL, TensorFlow, PyTorch, CLIP, EasyOCR, Power BI
    - **Mục tiêu:** Trở thành Data Scientist chuyên sâu về computer vision và analytics cho ngành bán lẻ
    """)
    st.markdown("---")
    st.subheader("Portfolio tips")
    st.write("- 3–5 project chất lượng > 10 project sơ sài.\n- Storytelling: Dataset -> Tools -> Process -> Result.\n- Thêm ảnh dashboard, chart, screenshot code.")
