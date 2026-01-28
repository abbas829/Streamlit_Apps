import streamlit as st, pandas as pd, io, zipfile
from PIL import Image
from caption_engine import CaptionEngine
from seo_tools import inject_keywords

st.set_page_config(page_title="CaptionPro", page_icon="🖼️")
st.title("🖼️ CaptionPro – AI Product Caption Generator")
st.markdown("*Upwork 🟢 Certified | 24-h delivery | SEO-optimized*")

@st.cache_resource
def load_engine():
    return CaptionEngine()

engine = load_engine()

# Pricing
if st.button("Basic – 50 captions – $50"): st.session_state["tier"] = "basic"
if st.button("Pro – 150 captions – $150"): st.session_state["tier"] = "pro"
if st.button("Enterprise – API – $300"): st.session_state["tier"] = "api"

uploaded = st.file_uploader("Drop images", accept_multiple_files=True)
keywords = st.text_input("SEO keywords", "stylish, comfortable, premium")

if st.button("Generate Captions") and uploaded:
    captions = []
    for img_file in uploaded:
        image = Image.open(img_file).convert("RGB")
        raw = engine.generate(image)
        final = inject_keywords(raw, keywords.split(","))
        captions.append({"file": img_file.name, "caption": final})
    df_out = pd.DataFrame(captions)
    st.dataframe(df_out)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for _, row in df_out.iterrows():
            zf.writestr(row['file'] + ".txt", row['caption'])
    st.download_button("💾 Download ZIP", data=zip_buffer.getvalue(), file_name="captions.zip")