import streamlit as st
from pathlib import Path

# ── MUST be first Streamlit call ──────────────────────────────────────────────
st.set_page_config(
    page_title="Spotware",
    page_icon="🔍",
    layout="centered"      
)

# ── Fonts + Title Styling ─────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;600;700;800;900&display=swap');

        html, body, p, div, span, label, button, input {
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Hero title ─────────────────────────────────────────────────── */
        .hero-title {
            font-family: 'DM Sans', sans-serif;
            font-size: clamp(5rem, 10vw, 9rem);  /* scales with screen width */
            font-weight: 900;
            text-align: center;
            letter-spacing: -0.03em;
            line-height: 1;
            width: 100%;
            padding: 2rem 0 0.5rem 0;
            color: inherit;
        }

        /* ── Subtitle under title ────────────────────────────────────────── */
        .hero-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            font-weight: 400;
            text-align: center;
            opacity: 0.6;
            margin-bottom: 2.5rem;
        }

        /* ── Divider line under hero ─────────────────────────────────────── */
        .hero-divider {
            border: none;
            border-top: 1px solid rgba(128,128,128,0.2);
            margin: 0 auto 2rem auto;
            width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

# ── Logo ──────────────────────────────────────────────────────────────────────


col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image(str("logo1.png"), width=1000)

# ── Hero Title ────────────────────────────────────────────────────────────────
st.markdown("<h1 class='hero-title'>Spotware</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Upload or capture a photo of damaged hardware for analysis.</p>", unsafe_allow_html=True)
st.markdown("<hr class='hero-divider'>", unsafe_allow_html=True)

# ── Method 1: Upload ──────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

# ── Method 2: Camera ──────────────────────────────────────────────────────────
picture = st.camera_input("Take a picture")
if picture:
    st.image(picture)