import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) 
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index


# Sidebar 
st.sidebar.markdown(
        """
        <div style="text-align: center; color: #ff6347;">
            <h1>GREEN GUARDIAN</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.title('Dashboard')
app_mode = st.sidebar.selectbox("Select page", ["Home", "About", "Disease Recognition", "Disease Recognition (Take a Photo)"], index=0)

# Home page
if app_mode == "Home":
    st.header("Plant Disease Recognition System")
    image_path = "plant.jpg"
    st.image(image_path, width=450, caption="Welcome to the Plant Recognition System")
    
    # Welcome Section
    st.title("Your Smart Assistant for Plant Health")
    st.subheader("Identify Plant Diseases, Pests, and Nutrient Deficiencies with Ease")
    st.write("""
    Explore the cutting-edge technology designed to help you diagnose plant issues and receive instant solutions to keep your farm or garden thriving.
    """, unsafe_allow_html=True)

    # How It Works Section
    st.header("How It Works:")
    st.write("""
    1. **Capture a Clear Image** : Take a photo of your plant or crop showing any issues.
    2. **Upload the Image** : Use our user-friendly interface to upload the picture.
    3. **AI-Driven Analysis** : Our advanced AI technology instantly analyzes the plant for diseases, pests, or deficiencies.
    4. **Get Personalized Recommendations** : Receive tailored advice for optimal plant care.
    """, unsafe_allow_html=True)

    st.write("""
    Ready to get started? Let’s ensure your plants are healthy and flourishing. 
    """, unsafe_allow_html=True)
# About Us Page
elif app_mode == "About":
    st.header("About")
    st.markdown("""
    ### About Our Dataset
    Our plant disease recognition system leverages a comprehensive dataset of images, carefully curated to represent a wide range of plant species and diseases. This dataset includes over 10,000 images of plants, each labeled with the specific disease or condition affecting the plant. The images were sourced from various agricultural research institutions, universities, and online repositories, ensuring a diverse and representative sample of plant diseases. This extensive dataset allows our system to learn patterns and characteristics of different plant diseases, enabling it to make accurate predictions and provide valuable insights for plant health management.
    """, unsafe_allow_html=True)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image", type=['jpg', 'png', 'jpeg'])
    if st.button("Show Image"):
        if test_image is not None:
            st.image(test_image, use_column_width=True, caption="Uploaded Image")
        else:
            st.warning("Please upload an image first.")
    
    # Predict Button
    if st.button("Predict"):
        if test_image is not None:
            with st.spinner("Please Wait....."):
                st.write("Our prediction")
                result_index = model_prediction(test_image)  # You need to implement this function
                # Define Classname
                class_name = ['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight','Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___healthy','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot','Tomato___Tomato_mosaic_virus','Tomato___Tomato_Yellow_Leaf_Curl_Virus']
                st.success(f"Model is predicting it's a {class_name[result_index]}")
        else:
            st.warning("Please upload an image first.")

# Disease Recognition (Take a Photo) Page
elif app_mode == "Disease Recognition (Take a Photo)":
    st.header("Disease Recognition (Take a Photo)")
    test_image = st.camera_input("Take an Image")
    if st.button("Show Image"):
        if test_image is not None:
            st.image(test_image, use_column_width=True, caption="Captured Image")
        else:
            st.warning("Please capture an image first.")
    
    # Predict Button
    if st.button("Predict"):
        if test_image is not None:
            with st.spinner("Please Wait....."):
                st.write("Our prediction")
                result_index = model_prediction(test_image)  # You need to implement this function
                # Define Classname
                class_name = ['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight','Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___healthy','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot','Tomato___Tomato_mosaic_virus','Tomato___Tomato_Yellow_Leaf_Curl_Virus']
                st.success(f"Model is predicting it's a {class_name[result_index]}")
        else:
            st.warning("Please capture an image first.")