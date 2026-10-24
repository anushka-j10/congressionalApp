"""OpenCV preprocessing adapter; the original Tesseract reader stays intact."""

import math

import cv2
import numpy as np

from backend.readers import ReaderError, Reading, TesseractReader

PREPROCESSING = {
    "version": "opencv-v1", "median_kernel": 3, "adaptive_block": 51,
    "adaptive_constant": 15, "upscale": 2, "max_long_edge": 3200,
    "deskew_max_degrees": 10,
}


def estimate_skew(gray):
    """Estimate modest page tilt from many long, nearly horizontal text edges."""
    scale = min(1, 1000 / max(gray.shape))
    small = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    binary = cv2.adaptiveThreshold(small, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 31, 15)
    edges = cv2.Canny(binary, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 1800, threshold=45,
                            minLineLength=45, maxLineGap=10)
    angles = []
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            angle = math.degrees(math.atan2(int(y2) - int(y1), int(x2) - int(x1)))
            if abs(angle) <= PREPROCESSING["deskew_max_degrees"]:
                angles.append(angle)
    # Too little evidence means no automatic rotation, rather than a guess.
    return float(np.median(angles)) if len(angles) >= 5 else 0.0


def preprocess(image_bytes):
    """Return a clean grayscale PNG and estimated tilt, entirely in memory."""
    gray = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise ReaderError("Image preprocessing failed. Try another photo.")
    gray = cv2.medianBlur(gray, PREPROCESSING["median_kernel"])
    angle = estimate_skew(gray)
    if abs(angle) >= 0.15:
        height, width = gray.shape
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        gray = cv2.warpAffine(gray, matrix, (width, height),
                              flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT,
                              borderValue=255)
    scale = min(PREPROCESSING["upscale"], PREPROCESSING["max_long_edge"] / max(gray.shape))
    if scale > 1:
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, PREPROCESSING["adaptive_block"],
                                   PREPROCESSING["adaptive_constant"])
    # A small white margin helps page segmentation without adding source text.
    binary = cv2.copyMakeBorder(binary, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    ok, encoded = cv2.imencode(".png", binary)
    if not ok:
        raise ReaderError("Image preprocessing failed. Try another photo.")
    return encoded.tobytes(), angle


class PreprocessedReader:
    name = "preprocessed"

    def __init__(self, command="tesseract"):
        self.engine = TesseractReader(command)

    def read(self, jpeg):
        png, _ = preprocess(jpeg)
        reading = self.engine.read(png)
        return Reading(reading.text, reading.warnings + [
            "Image was preprocessed. Check dates, amounts, and IDs against the photo."
        ])
