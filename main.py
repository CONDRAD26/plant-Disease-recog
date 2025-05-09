import streamlit as st
import mysql.connector
import tensorflow as tf
import numpy as np
from PIL import Image

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Default XAMPP MySQL username
        password="", 
        database="plant_app"
    )

# Function to check login credentials
def check_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == password:
        return True
    return False

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        conn.close()
        return False

# Login Page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Registration Page
def registration_page():
    st.title("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_password == confirm_password:
            if register_user(new_username, new_password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists or registration failed.")
        else:
            st.error("Passwords do not match.")

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras')
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return result_index

# Main Application
def main_app():
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
                    class_name = ['Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy']
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
                    class_name = ['Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy']
                    st.success(f"Model is predicting it's a {class_name[result_index]}")
            else:
                st.warning("Please capture an image first.")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Check if user is logged in
if st.session_state.logged_in:
    main_app()
else:
    st.sidebar.title("Authentication")
    auth_mode = st.sidebar.radio("Choose Mode", ["Login", "Register"])
    if auth_mode == "Login":
        login_page()
    else:
        registration_page()