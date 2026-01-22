# app/services/image_input.py
from abc import ABC, abstractmethod
import numpy as np
import cv2
import io
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()


class ImageInput(ABC):
    @abstractmethod
    def to_ndarray(self) -> np.ndarray:
        """Convert image input to numpy ndarray in BGR format."""
        pass


class FileImageInput(ImageInput):
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

    def to_ndarray(self) -> np.ndarray:
        if not self.image_bytes:
            raise ValueError("Empty image bytes")

        # Try OpenCV first (JPEG/PNG)
        nparr = np.frombuffer(self.image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is not None:
            return img

        # Fallback: HEIC via Pillow
        try:
            pil_img = Image.open(io.BytesIO(self.image_bytes)).convert("RGB")
        except Exception as e:
            raise ValueError(f"Failed to decode image (HEIC fallback failed): {e}")

        # Convert RGB → BGR for OpenCV / dlib
        img = np.array(pil_img)[:, :, ::-1]
        return img
