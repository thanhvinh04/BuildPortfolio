# pages/contact.py
import streamlit as st
from urllib.parse import quote_plus
from utils.helpers import load_settings

def app():
    settings = load_settings().get("contact", {})

    email = settings.get("email", "")
    linkedin = settings.get("linkedin", "")
    github = settings.get("github", "")

    st.title("✉️ Contact")
    st.write("Kết nối với mình qua email hoặc LinkedIn")

    # show contact links neatly
    st.markdown(f"- **Email:** [{email}](mailto:{email})")
    st.markdown(f"- **LinkedIn:** [{linkedin}]({linkedin})")
    if github:
        st.markdown(f"- **GitHub:** [{github}]({github})")

    st.markdown("---")
    st.subheader("Gửi tin nhắn")

    with st.form("contact_form"):
        name = st.text_input("Tên")
        sender = st.text_input("Email của bạn (để mình trả lời)", value="")
        msg = st.text_area("Nội dung tin nhắn")
        submit = st.form_submit_button("Gửi")

        if submit:
            if not sender or not msg:
                st.warning("Vui lòng nhập email và tin nhắn")
            else:
                # Build mailto link (subject + body encoded)
                subject = f"Portfolio Contact from {name or 'Visitor'}"
                body = f"From: {name or 'Visitor'} <{sender}>\n\n{msg}"
                mailto = f"mailto:{email}?subject={quote_plus(subject)}&body={quote_plus(body)}"

                st.success("Chuẩn bị gửi email — bấm link bên dưới để mở trình email của bạn:")
                # show clickable mailto link
                st.markdown(f"[📧 Gửi email tới {email}]({mailto})")
                # Also display the raw message for user's confirmation
                st.markdown("**Nội dung bạn sẽ gửi:**")
                st.code(body)
