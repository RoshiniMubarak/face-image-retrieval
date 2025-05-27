import streamlit as st
from PIL import Image
from utils import search_images
import time
import base64
import io

# Page config
st.set_page_config(page_title="✨ Face Finder AI ✨", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #fff0f6;
        font-family: 'Segoe UI', sans-serif;
    }
    .title-typing {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #ff6ec4, #7873f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: fadeIn 2s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .sidebar-style {
        padding: 0;
        box-shadow: none;
        margin-bottom: 0;
        color: #333;
    }
    .search-card {
        border-radius: 0;
        padding: 0;
        margin: auto;
        text-align: center;
        margin-bottom: 1rem;
    }

    .image-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin-top: 1.5rem;
        padding: 0 1rem 1rem 1rem;
    }
    .image-card {
        background-color: #1c1c24;
        padding: 0.75rem;
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        transition: transform 0.3s ease-in-out;
        text-align: center;
    }
    .image-card:hover {
        transform: scale(1.05);
    }
    .image-card img {
        width: 100%;
        max-height: 600px;
        border-radius: 8px;
        object-fit: cover;
    }
    .image-score {
        color: #ccc;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title-typing">✨ Face Finder AI ✨</div>', unsafe_allow_html=True)
st.markdown("#### Describe a face, and we’ll retrieve images that match your vision using the power of CLIP!", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-style">', unsafe_allow_html=True)
    st.header("🎨 Customize")
    st.markdown("Describe any facial features you want to find visually.")
    st.markdown("**Examples:**")
    st.markdown("- A close-up face with blue eyes")
    st.markdown("- A person with curly hair")
    st.markdown("- An old man with a white beard")
    st.markdown("- A confident woman with short hair and glasses")

    num_results = st.slider("Number of images to retrieve:", min_value=2, max_value=20, value=6, step=1)
    layout_cols = st.radio("Images per row:", [1, 2, 3, 4], index=1, horizontal=True)
    st.info("💡 Be as creative as you like!")
    st.markdown('</div>', unsafe_allow_html=True)

# Search box
st.markdown('<div class="search-card">', unsafe_allow_html=True)
prompt = st.text_input("📝 Describe the face:", "a confident woman with short hair and glasses")
search_clicked = st.button("🔍 Search Images")
st.markdown('</div>', unsafe_allow_html=True)

results = []

if search_clicked:
    with st.spinner("✨ Searching for matching faces..."):
        time.sleep(1.2)
        results = search_images(prompt, top_k=num_results)

if results:
    st.markdown("## 🖼️ Top Retrieved Faces", unsafe_allow_html=True)

    for i in range(0, len(results[:num_results]), layout_cols):
        cols = st.columns(layout_cols)
        for j in range(layout_cols):
            if i + j < len(results):
                res = results[i + j]
                image = Image.open(res['path'])

                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                with cols[j]:
                    st.markdown(f"""
                        <div class="image-card">
                            <img src="data:image/jpeg;base64,{img_str}" />
                            <div class="image-score">🏅 Rank {i + j + 1}<br>Score: <b>{res['score']:.4f}</b></div>
                        </div>
                    """, unsafe_allow_html=True)


    # Scores
    st.markdown("## 📊 Similarity Scores")
    metric_cols = st.columns(4)
    for i, res in enumerate(results[:num_results]):
        with metric_cols[i % 4]:
            st.metric(label=f"Rank {i+1}", value=f"{res['score']:.4f}")

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit & CLIP | © 2025</div>', unsafe_allow_html=True)
