# pages/contact.py
import streamlit as st
from urllib.parse import quote_plus

def app():
    st.title("✉️ Contact")
    st.write("Kết nối với mình qua email hoặc LinkedIn")
    st.write("- Email: nguyenthanhvinh1234qn@gmail.com")
    st.write("- LinkedIn: https://www.linkedin.com/in/thanhvinh04/")
    st.markdown("---")
    st.subheader("Gửi tin nhắn")
    with st.form("contact_form"):
        name = st.text_input("Tên")
        email = st.text_input("Email")
        msg = st.text_area("Tin nhắn")
        submit = st.form_submit_button("Gửi")
        if submit:
            if not email or not msg:
                st.warning("Vui lòng nhập email và tin nhắn")
            else:
                mailto = f"mailto:nguyenthanhvinh1234qn@gmail.com?subject=Portfolio%20Contact%20from%20{quote_plus(name or 'Visitor')}&body={quote_plus(msg)}"
                st.markdown(f"Gửi email bằng cách bấm đây: [{mailto}]({mailto})")
