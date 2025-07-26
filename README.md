# PlantDoc

🌱 **PlantDoc** is a deep learning-powered web app for plant disease detection and guidance. Upload a plant leaf image, and PlantDoc will classify the disease (or health) and provide detailed information, including symptoms, causes, prevention, treatment, and recommendations.

## Features
- Upload plant leaf images for instant disease detection
- Uses a trained CNN model (`.h5` weights)
- Retrieves expert information from a CSV knowledge base
- Clean, modern Streamlit interface
- Detects diseases such as:
  - Apple Black Rot
  - Apple Healthy
  - Apple Scab
  - Cedar Apple Rust
  - Bell Pepper Bacterial Spot
  - Bell Pepper Healthy
  - Cherry Healthy
  - Cherry Powdery Mildew
  - Corn Healthy
  - Corn Common Rust
  - Potato Healthy
  - Potato Early Blight

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PlantDoc.git
   cd PlantDoc
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Structure
```
PlantDoc/
├── app.py
├── requirements.txt
├── README.md
├── plant_disease_expert_reports_english.csv
└── model/
    └── plant_disease_classification_advanced_model.h5
```

## Notes
- The model expects images of size 128x128x3.
- The CSV file must be present in the root directory.
- The model weights (`.h5`) should be in the `model/` folder.

## License
MIT
