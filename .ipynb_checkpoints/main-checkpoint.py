import streamlit as st

# Sidebar 
st.sidebar.markdown(
        """
        <div style="text-align: ;">
            <h1 style="color: #ff6347;">GREEN GUARDIAN</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.title('Dashboard')
app_mode = st.sidebar.selectbox("Select page", ["Home", "About", "Disease Recognition", "Disease Recognition (Take a Photo)"])

# Home page
if app_mode == "Home":
    st.header("Plant Disease Recognition System")
    image_path = "plant.jpg"
    st.image(image_path, width=450)
    
    # Welcome Section
    st.title(" Welcome to the Plant Recognition System")
    st.subheader("Your Smart Assistant for Plant Health ")

    st.write("""
    We're thrilled to have you here! This web app is your personal plant expert, helping you quickly identify plant diseases, pests, and nutrient deficiencies with ease. With just a single click, you can diagnose plant issues and get instant solutions to keep your farm or garden thriving.
    """)

    # How It Works Section
    st.header(" How It Works:")
    st.write("""
    1. **Snap a Picture** : Simply take a clear photo of your plant or crop showing any issues.
    2. **Upload the Image** : Use our easy-to-use interface to upload the picture.
    3. **AI-Powered Analysis** : Our cutting-edge AI instantly analyzes the plant for diseases, pests, or deficiencies.
    4. **Get Actionable Solutions** : Receive personalized recommendations.
    

    Ready to get started? Let’s keep your plants healthy and growing strong. 
    """)

# About Us Page
elif app_mode == "About":
    st.header("About")
    st.markdown("""
    ### About Dataset
    This section provides information about the dataset used for training the plant recognition model.
    """)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image")
    if st.button("Show Image"):
        if test_image is not None:
            st.image(test_image, use_column_width=True)
        else:
            st.warning("Please upload an image first.")
    
    # Predict Button
    if st.button("Predict"):
        if test_image is not None:
            with st.spinner("Please Wait....."):
                st.write("Our prediction")
                result_index = model_prediction(test_image)  # You need to implement this function
                # Define Classname
                class_name = ['Egg_Class B', 'Egg_Fresh Class A', 'Egg_Fresh Class AA', 'Egg_stale']
                st.success(f"Model is predicting it's a {class_name[result_index]}")
        else:
            st.warning("Please upload an image first.")

# Disease Recognition (Take a Photo) Page
elif app_mode == "Disease Recognition (Take a Photo)":
    st.header("Disease Recognition (Take a Photo)")
    test_image = st.camera_input("Take an Image")
    if test_image is not None:
        st.image(test_image)
    