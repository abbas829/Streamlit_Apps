import streamlit as st
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import io
import os

# Set matmul precision (important for performance on some systems)
torch.set_float32_matmul_precision(["high", "highest"][0])

# Load the model (outside the function for efficiency)
@st.cache_resource  # Cache the model to avoid reloading on every run
def load_model():
    model = AutoModelForImageSegmentation.from_pretrained("ZhengPeng7/BiRefNet", trust_remote_code=True)
    model.to("cuda" if torch.cuda.is_available() else "cpu") # Use CUDA if available
    return model

birefnet = load_model()

# Image transformation
transform_image = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

@st.cache_data # Cache the processed images.
def process(image):
    image_size = image.size
    input_images = transform_image(image).unsqueeze(0).to("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        preds = birefnet(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image_size)
    image.putalpha(mask)
    return image

def process_file(uploaded_file):
    try:
        image = Image.open(uploaded_file).convert("RGB")
        transparent = process(image)

        # Convert to bytes for download
        img_bytes = io.BytesIO()
        transparent.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        return img_bytes, transparent # Return bytes for download and PIL image for display

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None


st.title("Background Removal Tool")

# Tabs for different input methods
tabs = ["Image Upload", "URL Input", "File Output"]
selected_tab = st.sidebar.radio("Select Input Method", tabs)

if selected_tab == "Image Upload":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        processed_image = process(image)
        st.image(processed_image, caption="Processed Image")

elif selected_tab == "URL Input":
    image_url = st.text_input("Paste an image URL")
    if image_url:
        try:
            import requests
            from io import BytesIO
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            image = Image.open(BytesIO(response.content)).convert("RGB")
            processed_image = process(image)
            st.image(processed_image, caption="Processed Image from URL")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching image from URL: {e}")
        except Exception as e:
            st.error(f"Error processing image: {e}")


elif selected_tab == "File Output":
    uploaded_file = st.file_uploader("Upload an image for file output", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes, processed_image = process_file(uploaded_file)
        if file_bytes:
            st.image(processed_image, caption="Processed Image") # Display the image
            st.download_button(
                label="Download PNG",
                data=file_bytes,
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.png",
                mime="image/png",
            )