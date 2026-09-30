import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AI Photo Enhancer", page_icon="✨", layout="centered")

st.markdown("""
    <div style='text-align: center;'>
        <h1>✨ AI Photo Enhancer (2K / 4K)</h1>
        <p>Apni blur ya low-quality photo upload karein aur use ekdum sharp HD banayein!</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for API Token
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("Apni Replicate API Key daalein", type="password")
    st.markdown("---")
    st.markdown("### Guide")
    st.markdown("1. Replicate account se apni API key banayein.\n2. Use yahan paste karein.\n3. Photo upload karke enhance karein!")

# Main content
uploaded_file = st.file_uploader("Apni Photo Chuniye (JPG/png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display original image safely using PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Photo", use_container_width=True)
    
    if st.button("✨ Photo Enhance Karein", type="primary"):
        if not api_key_input:
            st.error("Kripya pehle sidebar me apni Replicate API Key daalein!")
        else:
            with st.spinner("AI photo ko 2K/4K HD me enhance kar raha hai, kripya intezaar karein..."):
                try:
                    # Initialize Replicate client
                    client = replicate.Client(api_token=api_key_input)
                    
                    # Prepare image for Replicate input
                    uploaded_file.seek(0)
                    
                    # Run CodeFormer with full correct version hash to avoid 404
                    output = client.run(
                        "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ef9a525c65f72f8ba66835ff93f85f5aff",
                        input={
                            "image": uploaded_file,
                            "codeformer_fidelity": 0.7,
                            "upscale": 2,
                            "face_upsample": True
                        }
                    )
                    
                    if output:
                        # Download and display enhanced image
                        response = requests.get(output)
                        enhanced_image = Image.open(BytesIO(response.content))
                        
                        st.success("Photo safalta-purvak enhance ho gayi hai!")
                        st.image(enhanced_image, caption="Enhanced HD Photo", use_container_width=True)
                        
                        # Download button
                        buffered = BytesIO()
                        enhanced_image.save(buffered, format="JPEG")
                        st.download_button(
                            label="📥 Enhanced Photo Download Karein",
                            data=buffered.getvalue(),
                            file_name="enhanced_photo_hd.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        st.error("Model se output nahi mila. Kripya dobara koshish karein.")
                        
                except Exception as e:
                    st.error(f"Ek error aa gayi hai: {e}")
