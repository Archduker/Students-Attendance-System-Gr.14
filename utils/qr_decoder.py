import cv2
from PIL import Image
import numpy as np
import os

# Try to import pyzbar, but don't hard fail if system lib is missing
try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    HAS_PYZBAR = True
except ImportError:
    HAS_PYZBAR = False

class QRDecoder:
    """
    Utility class for decoding QR codes.
    Uses pyzbar if available (faster/robust), falls back to OpenCV.
    """
    
    @staticmethod
    def decode_image(image_path: str) -> str:
        """
        Decodes a QR code from an image file.
        Returns the data string if found, else None.
        """
        try:
            # Method 1: Pyzbar (if available)
            if HAS_PYZBAR:
                img = Image.open(image_path)
                decoded_objects = pyzbar_decode(img)
                if decoded_objects:
                    for obj in decoded_objects:
                        return obj.data.decode("utf-8")
            
            # Method 2: OpenCV Fallback
            img_cv = cv2.imread(image_path)
            if img_cv is not None:
                 detector = cv2.QRCodeDetector()
                 data, points, _ = detector.detectAndDecode(img_cv)
                 if data:
                     return data
                     
            return None
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None

    @staticmethod
    def decode_frame(frame) -> str:
        """
        Decodes a QR code from a cv2 frame (numpy array).
        Returns the data string if found, else None.
        """
        try:
            # Method 1: Pyzbar
            if HAS_PYZBAR:
                decoded_objects = pyzbar_decode(frame)
                if decoded_objects:
                    for obj in decoded_objects:
                        return obj.data.decode("utf-8")
            
            # Method 2: OpenCV Fallback
            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(frame)
            if data:
                return data
                
            return None
        except Exception as e:
            # print(f"Error decoding frame: {e}")
            return None
