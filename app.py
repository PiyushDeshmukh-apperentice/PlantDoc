import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

# --- CONFIG ---
MODEL_PATH = os.path.join("model", "plant_disease_classification_advanced_model.h5")
CSV_PATH = "/home/piyush/Desktop/Projects/Plant_Disease/plant_disease_expert_reports_english.csv"
IMG_SIZE = (128, 128)

# --- LOAD MODEL & CSV ---
@st.cache_resource
def load_cnn_model():
    return load_model(MODEL_PATH)

@st.cache_data
def load_disease_info():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    return df

model = load_cnn_model()
disease_info = load_disease_info()
CLASSES = disease_info["Disease Name (English)"].tolist()

# --- STREAMLIT UI ---

# --- CUSTOM CSS ---
st.set_page_config(page_title="PlantDoc", layout="centered")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, .stApp {
        background: #14532d !important; /* solid dark green */
        font-family: 'Montserrat', Arial, sans-serif !important;
        color: #f1f8e9 !important;
    }
    .main-header {
        background: #1b5e20;
        color: #e8f5e9;
        padding: 2rem 1rem 1rem 1rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 2px 16px 0 rgba(67,160,71,0.08);
        font-family: 'Montserrat', Arial, sans-serif !important;
    }
    .stFileUploader label {
        color: #e8f5e9 !important;
        font-weight: 600;
        font-size: 1.1rem;
        background: #256029;
        padding: 0.7em 1.2em;
        border-radius: 0.7em;
        box-shadow: 0 2px 8px 0 rgba(67,160,71,0.10);
        margin-bottom: 1em;
        display: inline-block;
    }
    .stFileUploader .css-1cpxqw2 {
        color: #388e3c !important;
    }
    .stButton>button {
        background: #388e3c;
        color: #e8f5e9;
        border-radius: 0.5em;
        font-weight: 600;
        border: none;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #66bb6a;
        color: #14532d;
    }
    .stMarkdown, .stSubheader, .stInfo, .stImage, .stAlert, .stTextInput, .stSelectbox, .stFileUploader, .stDataFrame, .stTable {
        color: #f1f8e9 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- HEADER ---
st.markdown(
    '<div class="main-header"><h1>🌱 PlantDoc: Plant Disease Diagnosis & Guidance</h1></div>',
    unsafe_allow_html=True
)

# --- DISEASE LIST ---
st.markdown(
    '<div style="background:#256029;padding:1.2em 1em 1em 1em;border-radius:0.7em;margin-bottom:1.5em;box-shadow:0 2px 8px 0 rgba(67,160,71,0.10);color:#e8f5e9;">'
    '<b>Detectable Diseases:</b>'
    '<ul style="margin-top:0.7em;">'
    + ''.join([f'<li style="margin-bottom:0.2em;">{d}</li>' for d in CLASSES]) +
    '</ul>'
    '</div>',
    unsafe_allow_html=True
)

st.write("Upload a photo of a plant leaf. The app will detect the disease (if any) and provide expert information.")

uploaded_file = st.file_uploader("Choose a plant leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    st.image(uploaded_file, caption="Uploaded Leaf Image", use_column_width=True)
    
    # Preprocess image
    img = load_img(uploaded_file, target_size=IMG_SIZE)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    preds = model.predict(img_array)
    pred_idx = np.argmax(preds)
    pred_class = CLASSES[pred_idx]
    st.subheader(f"🩺 Prediction: **{pred_class}**")
    
    # Get info from CSV
    info_row = disease_info[disease_info["Disease Name (English)"] == pred_class].iloc[0]
    st.markdown("### Disease Information")
    st.markdown(f"**Symptoms:** {info_row['Symptoms']}")
    st.markdown(f"**Causes:** {info_row['Causes']}")
    st.markdown(f"**Prevention:** {info_row['Prevention']}")
    if 'Treatment' in info_row and not pd.isna(info_row['Treatment']):
        st.markdown(f"**Treatment:** {info_row['Treatment']}")
    if 'Recommendations' in info_row and not pd.isna(info_row['Recommendations']):
        st.markdown(f"**Recommendations:** {info_row['Recommendations']}")
else:
    st.info("Please upload a plant leaf image to get started.")