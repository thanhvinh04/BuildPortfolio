# pages/home.py
import streamlit as st
from pathlib import Path
from utils.helpers import load_settings
import html
import typing

def _is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")

def _render_html_carousel(image_urls: typing.List[str], height: int = 420, autoplay: bool = True, interval: int = 3000):
    """
    Render a simple CSS/JS carousel that auto-plays in the browser.
    Requires image URLs (public).
    interval in ms.
    """
    # build slides HTML
    slides_html = ""
    for i, url in enumerate(image_urls):
        # escape url for safety
        safe = html.escape(url, quote=True)
        slides_html += f'<div class="slide"><img src="{safe}" alt="slide-{i}" /></div>\n'

    autoplay_attr = "true" if autoplay else "false"
    # Simple carousel CSS + JS (no external libs). Will show images centered + arrows + dots.
    html_code = f"""
        <style>
        .carousel{{
            position:relative;
            overflow:hidden;
            max-width:100%;   /* tăng từ 100% lên 120% */
            width:100%;       /* thêm để chắc chắn */
            height:{height}px;
            border-radius:10px;
            box-shadow:0 8px 24px rgba(0,0,0,0.12);
        }}
        .carousel .slides{{display:flex;transition:transform .6s ease; height:100%;}}
        .carousel .slide{{min-width:100%; display:flex;align-items:center;justify-content:center;background:#fffde7;}}
        .carousel img{{max-width:110%; max-height:100%; object-fit:contain;}}  /* tăng max-width */
        .carousel .nav{{position:absolute;top:50%;transform:translateY(-50%);width:100%;display:flex;justify-content:space-between;padding:0 8px;box-sizing:border-box;}}
        .carousel button.arrow{{background:rgba(0,0,0,0.4);border:none;color:white;padding:8px 10px;border-radius:6px;cursor:pointer;}}
        .carousel .dots{{position:absolute;left:50%;transform:translateX(-50%);bottom:8px;display:flex;gap:6px}}
        .carousel .dot{{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,0.5);cursor:pointer}}
        .carousel .dot.active{{background:white}}
        </style>

    <div class="carousel" id="streamlit-carousel">
      <div class="slides" id="slides">
        {slides_html}
      </div>
      <div class="nav">
        <button class="arrow" id="prev">&#10094;</button>
        <button class="arrow" id="next">&#10095;</button>
      </div>
      <div class="dots" id="dots"></div>
    </div>

    <script>
    (()=>{{
      const slidesEl = document.getElementById("slides");
      const dotsEl = document.getElementById("dots");
      const slidesCount = {len(image_urls)};
      let idx = 0;
      const interval = {interval};
      let timer = null;

      function renderDots() {{
        dotsEl.innerHTML = "";
        for(let i=0;i<slidesCount;i++) {{
          const d = document.createElement("div");
          d.className = "dot" + (i===0?" active":"");
          d.dataset.i = i;
          d.onclick = (e)=>{{ goTo(parseInt(e.target.dataset.i)); }};
          dotsEl.appendChild(d);
        }}
      }}

      function update() {{
        slidesEl.style.transform = `translateX(${{-idx * 100}}%)`;
        const ds = dotsEl.querySelectorAll(".dot");
        ds.forEach((d,i)=> d.classList.toggle("active", i===idx));
      }}

      function next() {{ idx = (idx+1) % slidesCount; update(); }}
      function prev() {{ idx = (idx-1+slidesCount) % slidesCount; update(); }}
      function goTo(i) {{ idx = i % slidesCount; update(); }}

      document.getElementById("next").addEventListener("click", ()=>{{ stopTimer(); next(); startTimer(); }});
      document.getElementById("prev").addEventListener("click", ()=>{{ stopTimer(); prev(); startTimer(); }});

      function startTimer() {{
        if ({'true' if autoplay else 'false'}) {{
          stopTimer();
          timer = setInterval(next, interval);
        }}
      }}
      function stopTimer() {{ if (timer) {{ clearInterval(timer); timer = null; }} }}

      renderDots();
      update();
      startTimer();

      // pause on hover
      const carousel = document.getElementById("streamlit-carousel");
      carousel.addEventListener("mouseenter", stopTimer);
      carousel.addEventListener("mouseleave", startTimer);
    }})();
    </script>
    """

    st.components.v1.html(html_code, height=height + 80, scrolling=False)


def app():
    settings = load_settings().get("home", {})

    title = settings.get("title", "Nguyễn Thành Vinh")
    subtitle = settings.get("subtitle", "Data Analyst / Analytics Engineering")
    description = settings.get("description", "Xin chào! Mình xây dựng các pipeline OCR, mô hình ML, dashboards và các sản phẩm analytics.")
    image = settings.get("image", None)  # main hero (optional)
    how_to = settings.get("how_to_browse", [
        "Vào **Projects** để lướt nhanh.",
        "Bấm **Xem chi tiết** để mở trang project riêng.",
        "Tải CV ở tab **Resume**."
    ])

    # slides: list of urls or local paths
    slides = settings.get("slides", [])  # e.g. ["assets/images/1.jpg", "https://.../2.jpg"]

    st.title(title)
    st.subheader(subtitle)
    st.write(description)

    # If slides provided, choose rendering strategy:
    if slides:
        # check types
        all_urls = all(_is_url(s) for s in slides)
        st.markdown("---")
        st.markdown("### My Journey")
        if all_urls:
            # HTML carousel with autoplay (best UX) for public URLs
            autoplay = settings.get("slides_autoplay", True)
            interval = int(settings.get("slides_interval_ms", 3000))
            height = int(settings.get("slides_height", 420))
            _render_html_carousel(slides, height=height, autoplay=autoplay, interval=interval)
        else:
            # Streamlit native slideshow for local images (no external JS)
            if "slide_idx" not in st.session_state:
                st.session_state.slide_idx = 0

            cols = st.columns([1, 3, 1])
            with cols[0]:
                if st.button("⟨ Prev", key="prev_btn"):
                    st.session_state.slide_idx = max(0, st.session_state.slide_idx - 1)
            with cols[2]:
                if st.button("Next ⟩", key="next_btn"):
                    st.session_state.slide_idx = min(len(slides) - 1, st.session_state.slide_idx + 1)

            idx = st.session_state.slide_idx
            img = slides[idx]
            p = Path(img)
            if p.exists():
                st.image(str(p), use_column_width=True)
            else:
                # try as URL
                try:
                    st.image(img, use_column_width=True)
                except Exception:
                    st.error(f"Không tìm thấy ảnh: {img}")

            # thumbnails
            thumbs = st.columns(len(slides))
            for i, s in enumerate(slides):
                with thumbs[i]:
                    label = f"{i+1}"
                    if st.button(label, key=f"thumb_{i}"):
                        st.session_state.slide_idx = i

    else:
        # if no slides, show single hero image or description
        st.markdown("---")
        if image:
            p = Path(image)
            if p.exists():
                st.image(str(p), width=720)
            else:
                try:
                    st.image(image, width=720)
                except Exception:
                    st.info("Ảnh hero không tìm thấy.")
        st.markdown("---")
        st.markdown("### How to browse")
        for i, line in enumerate(how_to, start=1):
            st.markdown(f"{i}) {line}")
