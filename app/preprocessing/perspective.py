import cv2
import numpy as np

from app.config import NORMALIZED_W, NORMALIZED_H, FIDUCIAL_MM


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


def _find_fiducial_in_region(
    gray: np.ndarray,
    x1: int, y1: int, x2: int, y2: int,
    corner_xy: tuple[int, int],
) -> tuple[float, float] | None:
    """
    Detect the fiducial mark center within the ROI [x1:x2, y1:y2].
    When multiple circles are found, returns the one closest to corner_xy
    (expressed in ROI-local coordinates), so we always pick the mark that
    is deepest into the corner rather than a form bubble.
    """
    roi = gray[y1:y2, x1:x2]
    h_roi, w_roi = roi.shape

    blurred = cv2.GaussianBlur(roi, (7, 7), 2)
    min_r = max(8, min(w_roi, h_roi) // 15)
    max_r = min(w_roi, h_roi) // 4

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=min_r * 2,
        param1=50,
        param2=18,
        minRadius=min_r,
        maxRadius=max_r,
    )
    if circles is None:
        return None

    cx_ref, cy_ref = corner_xy
    best = min(
        circles[0],
        key=lambda c: (c[0] - cx_ref) ** 2 + (c[1] - cy_ref) ** 2,
    )
    return float(int(np.round(best[0])) + x1), float(int(np.round(best[1])) + y1)


def find_fiducials(gray: np.ndarray) -> list[tuple[float, float]] | None:
    """
    Detect all 4 fiducial marks in the scan.
    Returns [(TL), (TR), (BL), (BR)] pixel centers, or None if any are missing.

    For each mark, estimates its expected pixel position from FIDUCIAL_MM assuming
    the scan is approximately A4 (210×297 mm), then searches in a ±12% window and
    picks the circle closest to that estimated center.  This avoids confusing the
    fiducial with other circles (e.g. logos) that happen to be near the corner.
    """
    h, w = gray.shape
    margin_x = int(w * 0.12)
    margin_y = int(h * 0.12)

    centers: list[tuple[float, float]] = []
    for fx_mm, fy_mm in FIDUCIAL_MM:
        ex = int(fx_mm / 210.0 * w)
        ey = int(fy_mm / 297.0 * h)

        x1 = max(0, ex - margin_x)
        x2 = min(w, ex + margin_x)
        y1 = max(0, ey - margin_y)
        y2 = min(h, ey + margin_y)

        # Reference = expected center expressed in ROI-local coordinates
        ref_in_roi = (ex - x1, ey - y1)

        pt = _find_fiducial_in_region(gray, x1, y1, x2, y2, ref_in_roi)
        if pt is None:
            return None
        centers.append(pt)

    return centers  # [TL, TR, BL, BR]


def correct_perspective(gray: np.ndarray) -> tuple[np.ndarray, list[str]]:
    """
    Warp the scan to a fixed NORMALIZED_W × NORMALIZED_H canvas.

    Priority:
      1. Fiducial-based warp  – most accurate, requires ⊕ marks on the form.
      2. Page-contour warp    – fallback when no fiducials found.
      3. Plain resize         – last resort.

    Returns (warped_gray, warnings).
    """
    warnings: list[str] = []
    h, w = gray.shape[:2]

    # ── 1. Fiducial-based warp ────────────────────────────────────────────────
    fiducials = find_fiducials(gray)
    if fiducials is not None:
        src = np.array(fiducials, dtype=np.float32)
        dst = np.array(
            [[fx / 210 * NORMALIZED_W, fy / 297 * NORMALIZED_H] for fx, fy in FIDUCIAL_MM],
            dtype=np.float32,
        )
        M = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(gray, M, (NORMALIZED_W, NORMALIZED_H))
        return warped, warnings

    warnings.append("fiducials_not_found: falling back to page-contour detection")

    # ── 2. Page-contour warp ──────────────────────────────────────────────────
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, page_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(page_mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 0.80 * h * w:
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

    # ── 3. Plain resize ───────────────────────────────────────────────────────
    warnings.append("perspective_correction_skipped: resizing to normalized canvas")
    resized = cv2.resize(gray, (NORMALIZED_W, NORMALIZED_H))
    return resized, warnings
