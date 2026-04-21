import cv2
import numpy as np

from app.config import NORMALIZED_W, NORMALIZED_H


def _order_corners(pts: np.ndarray) -> np.ndarray:
    """Return 4 points ordered: top-left, top-right, bottom-right, bottom-left."""
    pts = pts.reshape(4, 2).astype(np.float32)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    return np.array(
        [
            pts[np.argmin(s)],   # top-left:     min x+y
            pts[np.argmin(d)],   # top-right:    min x-y
            pts[np.argmax(s)],   # bottom-right: max x+y
            pts[np.argmax(d)],   # bottom-left:  max x-y
        ],
        dtype=np.float32,
    )


def correct_perspective(gray: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """
    Attempt to detect the document boundary and warp it to a fixed
    NORMALIZED_W × NORMALIZED_H canvas.  Falls back to a plain resize
    when detection fails (e.g. CamScanner output that is already flat).
    Returns (warped_gray, warnings).
    """
    warnings: list[str] = []
    h, w = gray.shape[:2]

    # Otsu threshold – bright page on a slightly darker scanner background
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, page_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Close small gaps so the page outline is a solid shape
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(page_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        img_area = h * w

        # Only attempt warp when the detected region covers most of the image
        if cv2.contourArea(largest) > 0.80 * img_area:
            peri = cv2.arcLength(largest, True)
            approx = cv2.approxPolyDP(largest, 0.02 * peri, True)

            if len(approx) == 4:
                corners = _order_corners(approx)
                dst = np.array(
                    [
                        [0, 0],
                        [NORMALIZED_W - 1, 0],
                        [NORMALIZED_W - 1, NORMALIZED_H - 1],
                        [0, NORMALIZED_H - 1],
                    ],
                    dtype=np.float32,
                )
                M = cv2.getPerspectiveTransform(corners, dst)
                warped = cv2.warpPerspective(gray, M, (NORMALIZED_W, NORMALIZED_H))
                return warped, warnings

    warnings.append("perspective_correction_skipped: resizing to normalized canvas")
    resized = cv2.resize(gray, (NORMALIZED_W, NORMALIZED_H))
    return resized, warnings
