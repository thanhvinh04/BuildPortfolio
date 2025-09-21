# pages/projects.py
import streamlit as st
from pathlib import Path

def go_to_detail(pid: str):
    """Callback để chuyển sang trang detail cho project pid."""
    st.session_state.project_id = pid
    st.session_state.page = "project_detail"
    # Streamlit sẽ tự rerun sau callback

def app(projects):
    st.title("📂 Projects")
    q = st.session_state.get("query", "")
    if q:
        st.info(f"Filter: {q}")

    cols = st.columns([3, 1])
    with cols[0]:
        search_box = st.text_input("Tìm kiếm Project", value=q, key="projects_search")
    with cols[1]:
        all_tags = sorted({t for p in projects for t in p.get("tools", [])})
        tag_choice = st.selectbox("Lọc tools", options=[""] + all_tags, index=0)

    # Build filtered list
    filtered = []
    for p in projects:
        txt = (p.get("title", "") + " " + p.get("short_desc", "") + " " + p.get("long_desc", "")).lower()
        if search_box and search_box.lower() not in txt:
            continue
        if tag_choice and tag_choice not in p.get("tools", []):
            continue
        filtered.append(p)

    if not filtered:
        st.write("Không tìm thấy project nào phù hợp")
        return

    for p in filtered:
        # ensure p['id'] is string (for unique keys)
        pid = str(p.get("id"))
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                thumb = p.get("thumbnail", "")
                if thumb:
                    thumb_path = Path(thumb)
                    if thumb_path.exists():
                        st.image(str(thumb_path), width=220)
                    else:
                        # allow URL thumbnails
                        try:
                            st.image(thumb, width=220)
                        except Exception:
                            st.warning(f"Không tìm thấy ảnh: {thumb}")

            with c2:
                st.subheader(p.get("title", "Untitled"))
                st.write(p.get("short_desc", ""))
                st.markdown(" ".join([f'`{t}`' for t in p.get("tools", [])]))

                # action buttons with unique keys and stable callbacks
                bcol1, bcol2, bcol3 = st.columns([1,1,1])
                with bcol1:
                    # Use on_click with kwargs (more reliable than args in loops)
                    st.button(
                        "Xem chi tiết",
                        key=f"detail_btn_{pid}",
                        on_click=go_to_detail,
                        kwargs={"pid": pid}
                    )
                with bcol2:
                    notebook_url = p.get("notebook_github", "").strip()
                    if notebook_url:
                        # anchor-button that opens in new tab
                        st.markdown(
                            f"""<a href="{notebook_url}" target="_blank" rel="noopener noreferrer"
                            style="text-decoration:none;">
                                <button style="width:100%; padding:8px; border-radius:6px; border:1px solid #ddd; background:#f7fbff;">
                                    Notebook
                                </button>
                            </a>""",
                            unsafe_allow_html=True
                        )
                    else:
                        st.write("")  # keep column height
                with bcol3:
                    report = p.get("report_pdf", "")
                    if report:
                        rp = Path(report)
                        if rp.exists():
                            # unique key for each download_button
                            with open(rp, "rb") as f:
                                st.download_button(
                                    "📥 Tải PDF",
                                    data=f,
                                    file_name=rp.name,
                                    key=f"download_{pid}"
                                )
                        else:
                            # external link
                            st.markdown(f"[Báo cáo]({report})")
        st.divider()
