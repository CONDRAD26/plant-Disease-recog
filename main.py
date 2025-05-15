import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2

def is_maize_leaf(image):
    try:
        if hasattr(image, 'read'):
            img = Image.open(image)
        else:
            img = Image.fromarray(image)

        img = img.convert('RGB')
        width, height = img.size
        aspect_ratio = width / height
        if aspect_ratio < 1.2:
            return False

        img_array = np.array(img)
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([95, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        green_percentage = np.sum(mask > 0) / (width * height)
        return green_percentage > 0.4
    except Exception as e:
        st.error(f"Error analyzing leaf: {str(e)}")
        return True

def model_prediction(test_image):
    maize_check = is_maize_leaf(test_image)
    if not maize_check:
        st.warning("""
        ⚠️ Note: This image doesn't fully match typical maize leaf characteristics.
        Processing anyway, but results may be less accurate.
        """)

    model = tf.keras.models.load_model('trained_model.keras')

    if hasattr(test_image, 'read'):
        image = Image.open(test_image)
    else:
        image = Image.fromarray(test_image)

    image = image.resize((128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    return np.argmax(prediction)

def show_management_page():
    st.header("Common Rust Disease Management in Maize")
    st.subheader("Disease Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://www.apsnet.org/publications/imageresources/PublishingImages/CommonRustFigure1.jpg", 
                caption="Common Rust symptoms on maize leaves", width=300)
    with col2:
        st.markdown("""
        **Scientific Name**: Puccinia sorghi  
        **Primary Host**: Maize (Zea mays)  
        **Season**: Favors cool, moist conditions (60-70°F)  
        **Severity**: Can cause 10-20% yield loss in susceptible varieties
        """)

    st.subheader("Integrated Management Strategies")
    st.markdown("""### Cultural Control Methods""")
    with st.expander("Show Cultural Control Methods"):
        st.markdown("""
        - **Resistant Varieties**: Plant rust-resistant maize hybrids
        - **Crop Rotation**: Rotate with non-host crops (soybeans, wheat)
        - **Field Sanitation**: Remove crop debris and volunteer plants
        - **Planting Time**: Adjust planting dates to avoid cool, moist periods
        - **Plant Spacing**: Ensure proper spacing for good air circulation
        """)

    st.markdown("""### Chemical Control Methods""")
    with st.expander("Show Chemical Control Methods"):
        st.markdown("""
        - **Fungicide Types**:
          - Triazoles (e.g., propiconazole, tebuconazole)
          - Strobilurins (e.g., azoxystrobin, pyraclostrobin)
          - Mixed formulations (e.g., propiconazole + azoxystrobin)

        - **Application Timing**:
          - First spray at disease detection
          - Follow-up sprays at 10-14 day intervals if weather favors disease
          - Critical period: from knee-high to tasseling stages

        - **Application Tips**:
          - Use sufficient water volume (20-30 gallons/acre)
          - Ensure good coverage of all leaves
          - Follow label instructions and pre-harvest intervals
        """)

    st.subheader("Monitoring and Action Thresholds")
    st.markdown("""
    - **Scouting Frequency**: Weekly during vegetative stages
    - **Threshold for Action**:
      - 5-10% leaf area affected on lower leaves
      - Disease present during cool, moist weather
      - Susceptible variety planted
    - **High Risk Conditions**:
      - Temperatures 60-70°F (16-21°C)
      - High humidity (>90%) or leaf wetness
      - Dense crop canopy
    """)

    st.subheader("Seasonal Prevention Calendar")
    st.table({
        "Growth Stage": ["Pre-planting", "Early Vegetative", "Late Vegetative", "Reproductive"],
        "Actions": [
            "Select resistant varieties, clean field",
            "Begin scouting, remove volunteers",
            "Apply first fungicide if needed",
            "Monitor upper leaves, apply fungicide if needed"
        ]
    })

    st.subheader("Additional Resources")
    st.markdown("""
    - [APSnet: Common Rust of Corn](https://www.apsnet.org/edcenter/disandpath/fungalbasidio/pdlessons/Pages/CornRust.aspx)
    - [Purdue Extension: Corn Disease Guide](https://www.extension.purdue.edu/extmedia/BP/BP-56-W.pdf)
    - [FAO: Maize Disease Management](http://www.fao.org/3/y4011e/y4011e00.htm)
    """)

def main_app():
    st.sidebar.markdown("""
        <div style="text-align: center; color: #ff6347;">
            <h1>GREEN GUARDIAN</h1>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.title('Dashboard')
    app_mode = st.sidebar.selectbox("Select page", 
                                    ["Home", "About", "Disease Recognition", 
                                     "Disease Recognition (Take a Photo)", "Rust Management"],
                                    index=0)

    if app_mode == "Home":
        st.header("Common Rust Disease in Maize")
        st.image("plant.jpg", width=450, caption="Welcome to the Common Rust Disease Recognition System")
        st.title("Your Smart Assistant for Plant Health")
        st.subheader("Identify Common Rust Disease with Ease")
        st.write("""
        Explore the cutting-edge technology designed to help you diagnose plant issues and receive instant solutions to keep your farm or garden thriving.
        """)
        st.header("How It Works:")
        st.write("""
        1. **Capture a Clear Image**: Take a photo of your maize plant showing symptoms
        2. **Upload the Image**: Use our interface to upload the picture
        3. **AI-Driven Analysis**: Our technology analyzes for Common Rust disease
        4. **Get Management Advice**: Receive tailored recommendations
        """)

    elif app_mode == "About":
        st.header("About")
        st.markdown("""
        ### About Our System
        Our Common Rust recognition system uses advanced AI technology trained on thousands of maize disease images to provide accurate identification and management recommendations for farmers and agronomists.
        """)

    elif app_mode == "Disease Recognition":
        st.header("Disease Recognition")
        test_image = st.file_uploader("Choose an Image", type=['jpg', 'png', 'jpeg'])

        if test_image is not None and st.button("Show Image"):
            st.image(test_image, use_column_width=True, caption="Uploaded Image")

        if st.button("Predict"):
            if test_image is not None:
                with st.spinner("Analyzing..."):
                    result_index = model_prediction(test_image)
                    class_names = [
                        'Corn (maize) - Common rust',
                        'Corn (maize) - Healthy'
                    ]
                    st.success(f"🔍 Model Prediction: {class_names[result_index]}")
                    st.image(test_image, caption="Analyzed Leaf", use_column_width=True)
                    if result_index == 0:
                        st.warning("""
                        🚨 Common Rust Detected!
                        Visit the 'Rust Management' page for control recommendations.
                        """)
                    else:
                        st.balloons()
                        st.success("""
                        🌱 Healthy Maize Leaf Detected!
                        Continue good farming practices.
                        """)
            else:
                st.warning("Please upload an image first.")

    elif app_mode == "Disease Recognition (Take a Photo)":
        st.header("Disease Recognition (Take a Photo)")
        test_image = st.camera_input("Take an Image")

        if test_image is not None and st.button("Show Image"):
            st.image(test_image, use_column_width=True, caption="Captured Image")

        if st.button("Predict"):
            if test_image is not None:
                with st.spinner("Analyzing..."):
                    result_index = model_prediction(test_image)
                    class_names = [
                        'Corn (maize) - Common rust',
                        'Corn (maize) - Healthy'
                    ]
                    st.success(f"🔍 Model Prediction: {class_names[result_index]}")
                    st.image(test_image, caption="Analyzed Leaf", use_column_width=True)
                    if result_index == 0:
                        st.warning("""
                        🚨 Common Rust Detected!
                        Visit the 'Rust Management' page for control recommendations.
                        """)
                    else:
                        st.balloons()
                        st.success("""
                        🌱 Healthy Maize Leaf Detected!
                        Continue good farming practices.
                        """)
            else:
                st.warning("Please capture an image first.")

    elif app_mode == "Rust Management":
        show_management_page()

if __name__ == '__main__':
    main_app()