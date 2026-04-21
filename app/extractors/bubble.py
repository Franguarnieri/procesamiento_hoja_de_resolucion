import cv2
import numpy as np


def sample_bubble(thresh_img: np.ndarray, cx: float, cy: float, radius: float) -> float:
    """
    Return the fill ratio (0.0–1.0) of the circular region centred at (cx, cy)
    with the given radius, on a THRESH_BINARY_INV image (marked pixels = white).
    """
    mask = np.zeros(thresh_img.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (int(cx), int(cy)), max(1, int(radius)), 255, -1)
    area = cv2.countNonZero(mask)
    if area == 0:
        return 0.0
    marked = cv2.countNonZero(cv2.bitwise_and(thresh_img, thresh_img, mask=mask))
    return marked / area
