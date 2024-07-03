import cv2
import numpy as np
import cloudinary
import cloudinary.uploader
from django.conf import settings

def extract_frame_from_video(video_url):
    cap = cv2.VideoCapture(video_url)
    success, frame = cap.read()
    cap.release()
    if success:
        # Convert frame to image
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(img_bytes, folder="extracted_frames/")
        return result['url']
    return None
