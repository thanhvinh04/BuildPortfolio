# pages/home.py
import streamlit as st
from pathlib import Path
from utils.helpers import load_settings

def app():
    settings = load_settings().get("home", {})

    title = settings.get("title", "Nguyễn Thành Vinh — Portfolio")
    subtitle = settings.get("subtitle", "Data Analyst / Analytics Engineering")
    description = settings.get("description", "Xin chào! Mình xây dựng các pipeline OCR, mô hình ML, dashboards và các sản phẩm analytics.")
    image = settings.get("image", "assets/images/background.jpg")
    how_to = settings.get("how_to_browse", [
        "Vào **Projects** để lướt nhanh.",
        "Bấm **Xem chi tiết** để mở trang project riêng.",
        "Tải CV ở tab **Resume**."
    ])

    st.title(title)
    st.subheader(subtitle)
    st.write(description)

    # Render image if exists (support local path or URL)
    if image:
        p = Path(image)
        if p.exists():
            st.image(str(p), width=360)
        else:
            # assume it's a URL or invalid path -> try show (Streamlit will error if it's broken)
            try:
                st.image(image, width=360)
            except Exception:
                st.warning("Image not found: " + str(image))

    st.markdown("---")
    st.markdown("### How to browse")
    for i, line in enumerate(how_to, start=1):
        # support markdown in each line
        st.markdown(f"{i}) {line}")
