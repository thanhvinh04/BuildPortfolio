# streamlit_portfolio.py
import streamlit as st
from pathlib import Path
from utils.helpers import load_projects
from views.home import app as home_app


st.set_page_config(page_title="Portfolio - Nguyễn Thành Vinh", layout="wide")

# Load projects (from projects.json)
projects = load_projects()

# Initialize session state defaults
if "page" not in st.session_state:
    st.session_state.page = "home"
if "project_id" not in st.session_state:
    st.session_state.project_id = None
if "query" not in st.session_state:
    st.session_state.query = ""

# Sidebar navigation
with st.sidebar:
    avatar_path = Path("assets/images/avatar.jpg")
    if avatar_path.exists():
        st.image(str(avatar_path), width=360)
    else:
        st.warning("Avatar image not found.")

    st.title("Menu")

    btn_style = """
    <style>
    .sidebar-btn {
        width: 100%;
        display: block;
        padding: 0.7em 0;
        margin-bottom: 0.5em;
        background: #f0f2f6;
        border: none;
        border-radius: 8px;
        font-size: 1.1em;
        text-align: left;
        cursor: pointer;
        transition: background 0.2s;
    }
    .sidebar-btn:hover {
        background: #e0e4ea;
    }
    </style>
    """
    st.markdown(btn_style, unsafe_allow_html=True)

    # Streamlit buttons với style CSS
    if st.button("🏠 Home", key="home"):
        st.session_state.page = "home"
        st.session_state.project_id = None
    if st.button("ℹ️ About", key="about"):
        st.session_state.page = "about"
        st.session_state.project_id = None
    if st.button("📂 Projects", key="projects"):
        st.session_state.page = "projects"
        st.session_state.project_id = None
    if st.button("📄 Resume", key="resume"):
        st.session_state.page = "resume"
        st.session_state.project_id = None
    if st.button("✉️ Contact", key="contact"):
        st.session_state.page = "contact"
        st.session_state.project_id = None

    st.markdown("---")
    q_input = st.text_input("🔎 Tìm kiếm project", value=st.session_state.get("query", ""))
    if st.button("Tìm"):
        st.session_state.query = q_input or ""
        st.session_state.page = "projects"
        st.session_state.project_id = None

# Routing
page = st.session_state.page

# If projects is empty, show a friendly note in Projects page later.
# But keep imports lazy (import page module only when needed)
if page == "home":
    from views.home import app as home_app
    home_app()

elif page == "about":
    from views.about import app as about_app
    about_app()

elif page == "projects":
    # show projects list; pages/projects.py should set session_state.project_id and page to "project_detail" when selecting
    from views.projects import app as projects_app
    projects_app(projects)

elif page == "project_detail":
    pid = st.session_state.get("project_id")
    if pid is None:
        st.error("Không tìm thấy project. Quay về Projects.")
        if st.button("Quay về Projects"):
            st.session_state.page = "projects"
            st.session_state.project_id = None
    else:
        from views.projects_detail import app as project_detail_app
        project_detail_app(projects, pid)

elif page == "resume":
    from views.resume import app as resume_app
    resume_app()

elif page == "contact":
    from views.contact import app as contact_app
    contact_app()

else:
    st.write("Trang không xác định. Quay về Home.")
    st.session_state.page = "home"
