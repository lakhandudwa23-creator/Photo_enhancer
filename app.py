import streamlit as st
import replicate
from PIL import Image

# App Heading
st.set_page_config(page_title="AI HD Photo Enhancer", page_icon="✨", layout="centered")

st.title("✨ AI Photo Enhancer (2K / 4K)")
st.write("Apni blur ya low-quality photo upload karein aur use ekdum sharp HD banayein!")

# API Key Input (Ya app ke andar secure rakhne ke liye)
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Apni Replicate API Key daalein", type="password")

# Photo Upload Section
uploaded_file = st.file_uploader("Apni Photo Chuniye (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Original Photo Show karein
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Photo", use_column_width=True)
    
    if st.button("🚀 Enhance Photo to HD"):
        if not api_key:
            st.error("Pehle sidebar me apni Replicate API Key daalein!")
        else:
            with st.spinner("AI photo ko 2K/4K HD me badal raha hai, thoda intezaar karein..."):
                try:
                    # Replicate API ko call karenge (Real-ESRGAN model ke liye)
                    import os
                    os.environ["REPLICATE_API_TOKEN"] = api_key
                    
                    # Model run kar rahe hain
                    output = replicate.run(
                        "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
                        input={"image": uploaded_file}
                    )
                    
                    # Enhanced image show karein
                    st.success("Photo successfully enhance ho gayi!")
                    st.image(output, caption="Enhanced HD Photo", use_column_width=True)
                    st.markdown(f"[📥 Photo Download Karein]({output})")
                    
                except Exception as e:
                    st.error(f"Kuch error aa gaya: {e}")
