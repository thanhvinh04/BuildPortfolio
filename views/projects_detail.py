# pages/project_detail.py
import streamlit as st
from pathlib import Path
import textwrap
from urllib.parse import urlparse, unquote

def short_github_repo(url: str) -> str:
    """
    Trả về 'user/repo' nếu có, hoặc hostname nếu không parse được.
    """
    if not url:
        return ""
    try:
        u = urlparse(url)
        parts = [p for p in u.path.split("/") if p]
        if len(parts) >= 2:
            return "/".join(parts[:2])
        return u.netloc or url
    except Exception:
        return url

def last_path_name(url: str) -> str:
    """Lấy tên file cuối cùng trong path (giải mã percent-encoding)."""
    if not url:
        return ""
    try:
        u = urlparse(url)
        parts = [p for p in u.path.split("/") if p]
        if parts:
            return unquote(parts[-1])
        return ""
    except Exception:
        return ""

def to_colab_url(github_blob_url: str) -> str:
    """
    Convert a GitHub blob URL to Colab open URL.
    e.g. https://github.com/user/repo/blob/main/path/notebook.ipynb ->
          https://colab.research.google.com/github/user/repo/blob/main/path/notebook.ipynb
    """
    if not github_blob_url:
        return ""
    return github_blob_url.replace("https://github.com/", "https://colab.research.google.com/github/")

def github_button_html(url: str, label: str = "Open on GitHub", small_label: str = "") -> str:
    """
    Trả về HTML cho 1 nút mở GitHub + nhãn nhỏ bên cạnh.
    """
    small_html = f'<div style="font-size:0.9rem; color:#6b7280; margin-left:8px">{small_label}</div>' if small_label else ""
    html = f'''
    <div style="display:flex; align-items:center; gap:8px;">
      <a href="{url}" target="_blank" rel="noopener noreferrer" style="text-decoration:none;">
        <button style="padding:7px 12px; border-radius:8px; border:1px solid #e5e7eb; background:#111827; color:#ffffff;">
          {label}
        </button>
      </a>
      {small_html}
    </div>
    '''
    return html

def app(projects, pid: str):
    p = next((x for x in projects if str(x.get("id")) == str(pid)), None)
    if p is None:
        st.error("Không tìm thấy project.")
        if st.button("Quay lại", key="back_from_missing"):
            st.session_state.page = "projects"
            st.session_state.project_id = None
        return

    # callback to go back to projects using query params (works with router that reads st.query_params)
    def go_back():
        st.session_state.page = "projects"
        st.session_state.project_id = None

    # Nút quay lại ở đầu trang (dùng on_click để chắc chắn)
    st.button("⬅ Quay lại", key=f"back_btn_top_{pid}", on_click=go_back)

    st.title(p.get("title", "Untitled"))
    st.write(p.get("long_desc", ""))
    st.markdown("**Tóm tắt nhanh**")
    st.write(f"- Dataset: {p.get('dataset', '-')}")
    st.write(f"- Tools: {', '.join(p.get('tools', []))}")
    st.write(f"- Process: {p.get('process', '-')}")
    st.write(f"- Results: {p.get('results', '-')}")

    st.markdown("---")
    st.subheader("Ảnh / Dashboard")
    for img in p.get("image_assets", []):
        try:
            st.image(img, use_column_width=True)
        except Exception:
            st.write(img)

    st.markdown("---")
    st.subheader("Code")
    code_local = p.get("code_example_local", "")
    code_raw = p.get("code_example_raw", "")

    if code_local:
        pth = Path(code_local)
        if pth.exists():
            st.code(pth.read_text(encoding="utf-8"), language="python")
        else:
            st.warning(f"Code local không tìm thấy: {code_local}")
            if code_raw:
                repo_label = short_github_repo(code_raw)
                file_label = last_path_name(code_raw)
                st.markdown(f'- Remote: [{repo_label}/.../{file_label}]({code_raw})')
    elif code_raw:
        st.write("Code / Notebook:")
        repo_label = short_github_repo(code_raw)
        file_label = last_path_name(code_raw)
        st.markdown(github_button_html(code_raw, label="Open on GitHub", small_label=f"{repo_label}/.../{file_label}"), unsafe_allow_html=True)
        if "github.com" in code_raw and ("blob" in code_raw or code_raw.endswith(".ipynb")):
            colab = to_colab_url(code_raw)
            st.markdown(f'<a href="{colab}" target="_blank" rel="noopener noreferrer">🐙 Open in Colab</a>', unsafe_allow_html=True)
    else:
        example = """
# pseudo example
print("Replace with your code snippet or set 'code_example_local' in projects.json")
"""
        st.code(textwrap.dedent(example), language="python")

    st.markdown("---")
    st.subheader("Tài nguyên")

    nb_url = p.get("notebook_github", "").strip()
    if nb_url:
        repo_label = short_github_repo(nb_url)
        file_label = last_path_name(nb_url)
        st.markdown(
            github_button_html(nb_url, label="Open on GitHub", small_label=f"{repo_label}/.../{file_label}"),
            unsafe_allow_html=True
        )
        if "github.com" in nb_url and ("blob" in nb_url or nb_url.endswith(".ipynb")):
            st.markdown(f'<a href="{to_colab_url(nb_url)}" target="_blank" rel="noopener noreferrer">🐙 Open in Colab</a>', unsafe_allow_html=True)

    if p.get("report_pdf"):
        rp = Path(p.get("report_pdf"))
        if rp.exists():
            with open(rp, "rb") as f:
                st.download_button("📥 Tải báo cáo PDF", data=f, file_name=rp.name, key=f"report_{pid}")
        else:
            st.markdown(f'**Báo cáo:** <a href="{p.get("report_pdf")}" target="_blank" rel="noopener noreferrer">Mở báo cáo</a>', unsafe_allow_html=True)

    st.markdown("---")
    # Nút quay lại ở cuối trang (dùng on_click)
    st.button("⬅ Quay lại", key=f"back_btn_{pid}", on_click=go_back)
