import streamlit as st
import json
from pathlib import Path
import base64
from urllib.parse import quote_plus
import textwrap

st.set_page_config(page_title="Portfolio - Nguyễn Thành Vinh", layout="wide")

DATA_FILE = Path(__file__).parent / "projects.json"
if DATA_FILE.exists():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        projects = json.load(f)
else:
    projects = []

# ---------- Utility helpers ----------

def set_page(page: str, **params):
    """
    Cập nhật st.query_params hợp lệ để điều hướng (simulate multipage).
    Gán st.query_params = dict với values là list-of-strings.
    Không gọi st.rerun() ở đây (tránh cảnh báo 'calling rerun in callback is a no-op').
    Streamlit sẽ tự rerun khi query params thay đổi.
    """
    # Xây dict mới (value là list of strings)
    q = {}
    q["page"] = [str(page)]
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            q[k] = [str(x) for x in v]
        else:
            q[k] = [str(v)]

    # Gán query params (Streamlit sẽ cập nhật URL và rerun script tự động)
    st.query_params = q
    # Không gọi st.rerun() ở đây để tránh warning 'Calling st.rerun() within a callback is a no-op.'

def get_query():
    # Trả về đối tượng query params (dict-like)
    return st.query_params


def download_link_bytes(content_bytes: bytes, filename: str, label: str):
    b64 = base64.b64encode(content_bytes).decode()
    href = f"data:application/octet-stream;base64,{b64}"
    st.markdown(f"[{label}]({href})")


def render_project_card(p):
    st.image(p["thumbnail"], width=320)
    st.subheader(p["title"])
    st.write(p["short_desc"])
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("Xem chi tiết", key=f"view_{p['id']}"):
            # trực tiếp set query params (chuyển page)
            set_page("project", id=p["id"])
    with cols[1]:
        if st.button("GitHub", key=f"gh_{p['id']}"):
            st.write(f"Open: {p.get('notebook_github','-')}")
    with cols[2]:
        if st.button("Tải báo cáo", key=f"rep_{p['id']}"):
            st.info("Báo cáo chưa có. Bạn có thể upload file pdf và chỉnh link report_pdf trong projects list.")


# ---------- Top navigation (simple) ----------
query = get_query()
# Lấy page (nếu không có -> "home")
page = query.get("page", ["home"])[0]

with st.sidebar:
    st.title("Menu")
    # Khi dùng as on_click callback, truyền kwargs {"page":"home"} — set_page sẽ thay query params và Streamlit sẽ rerun
    st.button("Home", on_click=set_page, kwargs={"page": "home"})
    st.button("About", on_click=set_page, kwargs={"page": "about"})
    st.button("Projects", on_click=set_page, kwargs={"page": "projects"})
    st.button("Resume", on_click=set_page, kwargs={"page": "resume"})
    st.button("Contact", on_click=set_page, kwargs={"page": "contact"})
    st.markdown("---")
    st.write("🔎 Tìm nhanh")
    q = st.text_input("Tìm kiếm projects", value=query.get('q', [''])[0])
    if st.button("Tìm", key="search_btn"):
        set_page("projects", q=q)

# ---------- PAGES ----------
if page == "home":
    st.header("Hello — My name is Nguyen Thanh Vinh")
    st.subheader("Data Analyst / Analytics Engineering")
    st.write("Mình xây dựng các pipeline OCR, mô hình ML, và dashboards. Dưới đây là một số project tiêu biểu — lướt nhanh và bấm vào để xem chi tiết.")
    st.image("https://picsum.photos/seed/profile/1000/400")
    st.markdown("---")
    st.subheader("How to browse")
    st.write("1) Vào Projects để lướt nhanh. 2) Bấm 'Xem chi tiết' để mở trang project riêng. 3) Tải CV ở tab Resume.")

elif page == "about":
    st.header("About — Thông tin cá nhân")
    st.markdown("**Background học tập:** Cử nhân Khoa học máy tính ...")
    st.markdown("**Kỹ năng:** Python, SQL, Machine Learning, BI (Power BI/Looker Studio).")
    st.markdown("**Mục tiêu nghề nghiệp:** Trở thành Data Scientist chuyên sâu về giải pháp computer vision và analytics cho ngành bán lẻ.")
    st.markdown("---")
    st.subheader("Tips for portfolio")
    st.write("- 3-5 project chất lượng > 10 project sơ sài.\n- Storytelling: Dataset -> Tools -> Process -> Result.\n- Thêm hình ảnh dashboard, chart, screenshot code.")

elif page == "projects":
    st.header("Projects")
    q = query.get('q', [''])[0]
    tag_filter = query.get('tag', [''])[0]

    # Quick filter UI
    cols = st.columns([3, 1])
    with cols[0]:
        search_box = st.text_input("Tìm trong projects", value=q, key="projects_search")
    with cols[1]:
        all_tags = sorted({t for p in projects for t in p.get('tools', [])})
        tag_choice = st.selectbox("Lọc tag", options=[""] + all_tags, index=0)

    # Render quick cards
    st.write("Lướt nhanh các project — click 'Xem chi tiết' để mở trang riêng")
    for p in projects:
        # simple text match filter
        txt = (p.get('title','') + ' ' + p.get('short_desc','') + ' ' + p.get('long_desc','')).lower()
        if search_box and search_box.lower() not in txt:
            continue
        if tag_choice and tag_choice not in p.get('tools', []):
            continue
        with st.container():
            cols = st.columns([1, 2])
            with cols[0]:
                st.image(p['thumbnail'], width=220)
            with cols[1]:
                st.subheader(p['title'])
                st.write(p['short_desc'])
                # badges
                st.markdown(' '.join([f'`{t}`' for t in p.get('tools', [])]))
                if st.button("Xem chi tiết", key=f"detail_{p['id']}"):
                    set_page("project", id=p['id'])
        st.divider()

elif page == "project":
    # Show single project detail page
    pid = query.get('id', [None])[0]
    p = next((x for x in projects if x['id'] == pid), None)
    if not p:
        st.error("Project không tìm thấy. Vui lòng quay lại Projects.")
    else:
        st.header(p['title'])
        st.write(p['long_desc'])
        st.markdown("**Tóm tắt nhanh**")
        st.write(f"- Dataset: {p.get('dataset','-')}")
        st.write(f"- Tools: {', '.join(p.get('tools',[]))}")
        st.write(f"- Quy trình: {p.get('process','-')}")
        st.write(f"- Kết quả chính: {p.get('results','-')}")

        st.markdown("---")
        # images / dashboards
        st.subheader("Ảnh / Dashboard")
        for img in p.get('image_assets', []):
            st.image(img, use_column_width=True)

        st.markdown("---")
        # Code example (show only)
        st.subheader("Đoạn code minh họa (chỉ hiển thị)")
        example = """
# Example: load model and predict (pseudo)
from PIL import Image
import clip
import torch

model, preprocess = clip.load('ViT-B/32')
img = preprocess(Image.open('sample.jpg')).unsqueeze(0)
text = clip.tokenize(['sarcasm','not sarcasm'])
with torch.no_grad():
    image_features = model.encode_image(img)
    text_features = model.encode_text(text)
    # cos sim -> predict
"""
        st.code(textwrap.dedent(example), language='python')

        st.markdown("---")
        # Links
        st.subheader("Tài nguyên & Download")
        if p.get('notebook_github'):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Mở Notebook (GitHub)", key="nb_{}".format(p["id"])):
                    st.write(p.get('notebook_github'))
            with col2:
                if p.get('code_example_raw') and st.button("Xem code (raw)", key=f"raw_{p['id']}"):
                    st.write(p.get('code_example_raw'))
            with col3:
                if p.get('report_pdf') and st.button("Tải báo cáo PDF", key=f"repdown_{p['id']}"):
                    st.write("Report link: ", p.get('report_pdf'))

        st.markdown("---")
        if st.button("Quay về Projects"):
            set_page('projects')

elif page == "resume":
    st.header("Resume / CV")
    st.write("Bạn có thể tải CV ở đây")
    # fake CV bytes (replace with open file)
    dummy = b"PDF_BYTES_REPLACE_WITH_YOUR_CV"
    download_link_bytes(dummy, "CV_Nguyen_Thanh_Vinh.pdf", "📥 Tải CV (thay bằng file thật)")

elif page == "contact":
    st.header("Contact")
    st.write("Gửi tin nhắn cho mình — mình sẽ trả lời qua email.")
    with st.form('contact_form'):
        name = st.text_input('Tên')
        email = st.text_input('Email')
        msg = st.text_area('Tin nhắn')
        submit = st.form_submit_button('Gửi')
        if submit:
            if not email or not msg:
                st.warning('Vui lòng nhập email và tin nhắn')
            else:
                mailto = f"mailto:vinh@example.com?subject=Portfolio%20Contact%20from%20{quote_plus(name or 'Visitor')}&body={quote_plus(msg)}"
                st.markdown(f"Gửi email bằng cách bấm đây: [{mailto}]({mailto})")

else:
    st.write("Trang không xác định — quay về Home")
    set_page('home')

# ---------- Footer ----------
st.markdown("---")
st.write("© 2025 Nguyễn Thành Vinh — Portfolio")

# End of file
