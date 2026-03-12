import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. BRANDING & UI ---
st.set_page_config(page_title="Ultra AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #21262d; color: white; border: 1px solid #30363d; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Ultra AI Pro")
st.caption("Multimodal intelligence powered by Groq LPU™")

# --- 2. SETUP ---
# In production, use st.secrets for the API Key
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
if not api_key:
    st.info("Please enter your Groq API key in the sidebar to begin.")
    st.stop()

client = Groq(api_key=api_key)

# --- 3. THE "+" MULTI-INPUT SECTION ---
with st.expander("➕ Add Image (Camera or Upload)", expanded=True):
    source = st.radio("Select Source:", ["Upload from Device", "Take a Photo"])
    
    uploaded_file = None
    if source == "Upload from Device":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Snap a photo")

# --- 4. THE COMMAND & LOGIC ---
if uploaded_file:
    # Preview the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Selected Image", use_container_width=True)
    
    # Custom Command
    user_command = st.text_input("What should Ultra AI do with this image?", placeholder="e.g. 'Solve this math problem' or 'Describe the style'")
    
    if st.button("🚀 Process with Ultra AI"):
        # Convert to Base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        base64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        with st.spinner("Analyzing with Llama 3.2 Vision..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_command if user_command else "Describe this image."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                        ]
                    }]
                )
                
                st.subheader("Results:")
                st.write(response.choices[0].message.content)
                
                # Auto-Speech (Optional)
                # (You can re-add your speak_text function here)
                
            except Exception as e:
                st.error(f"Error: {e}")