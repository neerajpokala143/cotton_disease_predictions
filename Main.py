import streamlit as st
import numpy as np
from PIL import Image
import pickle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_image_class(model, img_array):
    preds = model.predict(img_array)
    preds = np.argmax(preds, axis=1)
    class_labels = ['diseased cotton leaf', 'diseased cotton plant', 'fresh cotton leaf', 'fresh cotton plant']
    return class_labels[preds[0]]

def main():
    #st.title('Cotton Disease Detection')
    st.markdown("<h1 style='text-align: center; color: skyblue; font-size: 40px; '>CNN FOR COTTON DISEASE DETECTION </h1>", unsafe_allow_html=True)
    page = st.sidebar.selectbox("Choose a page", ["CNN Explanation", "Image Inference"])

    if page == "CNN Explanation":
        st.markdown("<h1 style='text-align: left; color: white; font-size: 20px;'>Introduction to CNNs for Image Analysis:</h1>", unsafe_allow_html=True)
        st.markdown("Convolutional Neural Networks (CNNs) are a class of deep neural networks that are particularly effective for image analysis tasks. They are inspired by the organization of the animal visual cortex, where individual neurons respond to specific features of the visual field.")
        st.markdown("CNNs consist of multiple layers, including convolutional layers, pooling layers, and fully connected layers. Each layer performs a specific operation on the input data, and the network learns to extract hierarchical representations of features from the input image.")
        st.markdown("<h1 style='text-align: left; color: white; font-size: 20px;'>Architecture of a Typical CNN for Image Classification:</h1>", unsafe_allow_html=True)
        st.image(os.path.join(.'CNN.jpg'),use_column_width=True )
    
    elif page == "Image Inference":
        st.header("Image Inference")
        st.write("Upload an image of a cotton leaf or plant to detect if it's diseased or fresh.")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Make prediction
            model_path = 'model.pkl'  # Provide the path to your pickle file
            model = load_model(model_path)
            img_array = preprocess_image(uploaded_file)
            prediction = predict_image_class(model, img_array)
            st.success(f"Prediction: {prediction}")

if __name__ == "__main__":
    main()
