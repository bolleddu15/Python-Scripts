import os
import pydicom
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Function to preprocess the DICOM images
def preprocess_dicom_image(dicom_file_path):
    if os.path.exists(dicom_file_path):
        ds = pydicom.dcmread(dicom_file_path)
        img_array = ds.pixel_array
        img_array = cv2.resize(img_array, (128, 128))  # Resize to 128x128 for simplicity
        img_array = img_array / np.max(img_array)  # Normalize to [0,1]
        return img_array
    else:
        print("File not found:", dicom_file_path)
        return None

# Load and preprocess the initial DICOM file
dicom_file_path = r'C:\vscode folders\Chest_cancer deployment\0007d316f756b3fa0baea2ff514ce945.dicom'
label = 1  # Assuming 1 indicates cancer, modify accordingly

image = preprocess_dicom_image(dicom_file_path)

if image is not None:
    images = np.array([image]).reshape(-1, 128, 128, 1)
    labels = np.array([label])

    # Model creation
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')  # Assuming binary classification
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Fit the model without validation split since we have only one data point
    model.fit(images, labels, epochs=10, batch_size=1)

    # Load and preprocess a new DICOM image for prediction
    new_image_path = r'path_to_new_image.dicom'  # Update with the correct path
    new_image = preprocess_dicom_image(new_image_path)

    if new_image is not None:
        new_image = new_image.reshape(1, 128, 128, 1)  # Reshape for prediction

        # Predict whether the new image indicates cancer
        prediction = model.predict(new_image)
        print(f'Cancer Detected: {prediction[0][0] > 0.5}')
    else:
        print("New image could not be loaded.")
else:
    print("Initial image could not be loaded.")
import streamlit as st

# Function to display the image and prediction result
def display_prediction(image_path):
    image = preprocess_dicom_image(image_path)
    st.image(image, caption='DICOM Image', use_column_width=True)
    prediction = model.predict(image.reshape(1, 128, 128, 1))
    st.write(f'Cancer Detected: {prediction[0][0] > 0.5}')

# Streamlit app
def main():
    st.title("DICOM Image Cancer Detection")
    dicom_file_path = st.text_input("Enter DICOM file path:")
    if st.button("Predict"):
        display_prediction(dicom_file_path)

if __name__ == "__main__":
    main()
