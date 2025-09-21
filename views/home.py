# pages/home.py
import streamlit as st

def app():
    st.title("Nguyễn Thành Vinh — Portfolio")
    st.subheader("Data Analyst / Analytics Engineering")
    st.write("Xin chào! Mình xây dựng các pipeline OCR, mô hình ML, dashboards và các sản phẩm analytics.")
    st.image("assets/images/background.jpg", width=360)
    st.markdown("---")
    st.markdown("### How to browse")
    st.write(
        "1) Vào **Projects** để lướt nhanh.\n"
        "2) Bấm **Xem chi tiết** để mở trang project riêng.\n"
        "3) Tải CV ở tab **Resume**."
    )
