# app.py
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import torch
from pathlib import Path

# Function to perform object detection with YOLOv5
def detect_objects(image, model):
    # Perform object detection using YOLOv5
    results = model(image)

    # Return predictions
    return results.pandas().xyxy[0]

def main():
    st.title('Real-time Object Detection with YOLOv5')

    # Load YOLOv5 model
    @st.cache(allow_output_mutation=True)
    def load_model():
        model_path = Path("yolov5s.pt")  # Path to the YOLOv5 model file
        model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path, force_reload=True)
        return model
    model = load_model()

    # Create a video capture object
    video_capture = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not video_capture.isOpened():
        st.error('Error: Unable to access camera')
        return

    # Loop to capture frames and perform object detection
    while True:
        # Read frame from camera
        ret, frame = video_capture.read()
        if not ret:
            st.error('Error: Unable to capture frame')
            break

        # Convert the frame to PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection and get predictions
        predictions = detect_objects(image, model)

        # Display predictions
        st.write(predictions)

        # Wait for 2 seconds
        st.experimental_rerun_every(2 * 1000)  # Rerun every 2 seconds

if __name__ == "__main__":
    main()
