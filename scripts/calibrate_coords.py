#!/usr/bin/env python3
"""
Overlay the expected bubble grid on a real scan so you can visually verify
and tune the coordinate values in app/config.py.

Usage:
    python scripts/calibrate_coords.py <image_path> [output_path]

Output:
    - An annotated PNG where green circles = fill > threshold (marked),
      red circles = unmarked.
    - Fill ratios printed to stdout for every bubble so you can confirm the
      threshold value is appropriate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from app.config import (
    ANSWER_OPTIONS,
    BUBBLE_RADIUS_FRAC,
    CURSO_CONFIG,
    CURSO_TYPES,
    FECHA_CONFIG,
    DNI_CONFIG,
    FILL_THRESHOLD,
    MAX_BUBBLE_RADIUS,
    MONTHS,
    NORMALIZED_W,
    NORMALIZED_H,
    RESPUESTAS_CONFIG,
)
from app.preprocessing.loader import load_image
from app.preprocessing.normalizer import adaptive_threshold, to_grayscale
from app.preprocessing.perspective import correct_perspective
from app.extractors.bubble import sample_bubble


def _col_radius(cols: list[float]) -> float:
    if len(cols) < 2:
        return 10.0
    spacing = (cols[1] - cols[0]) * NORMALIZED_W
    return min(MAX_BUBBLE_RADIUS, max(5.0, spacing * BUBBLE_RADIUS_FRAC))


def _to_px(fx: float, fy: float) -> tuple[int, int]:
    return int(fx * NORMALIZED_W), int(fy * NORMALIZED_H)


def _draw(overlay, thresh, label, cx_frac, cy_frac, radius):
    cx, cy = _to_px(cx_frac, cy_frac)
    fill = sample_bubble(thresh, cx, cy, radius)
    color = (0, 200, 0) if fill > FILL_THRESHOLD else (0, 0, 200)
    cv2.circle(overlay, (cx, cy), int(radius), color, 2)
    print(f"  {label:<35s} fill={fill:.3f}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "calibration_overlay.png"

    with open(image_path, "rb") as fh:
        raw = fh.read()

    img = load_image(raw)
    gray = to_grayscale(img)
    warped_gray, warnings = correct_perspective(gray)
    thresh = adaptive_threshold(warped_gray)

    if warnings:
        print("Pipeline warnings:", warnings)

    overlay = cv2.cvtColor(warped_gray, cv2.COLOR_GRAY2BGR)

    # ── DNI ──────────────────────────────────────────────────────────────────
    print("\n=== DNI ===")
    r = _col_radius(DNI_CONFIG["cols"])
    for i, row_y in enumerate(DNI_CONFIG["rows"]):
        for j, col_x in enumerate(DNI_CONFIG["cols"]):
            _draw(overlay, thresh, f"D{i+1} digit={j}", col_x, row_y, r)

    # ── Fecha – Day ───────────────────────────────────────────────────────────
    print("\n=== FECHA DÍA ===")
    r = _col_radius(FECHA_CONFIG["dia_cols"])
    for i, row_y in enumerate(FECHA_CONFIG["dia_rows"]):
        for j, col_x in enumerate(FECHA_CONFIG["dia_cols"]):
            _draw(overlay, thresh, f"Día D{i+1} digit={j}", col_x, row_y, r)

    # ── Fecha – Month ─────────────────────────────────────────────────────────
    print("\n=== FECHA MES ===")
    r = _col_radius(FECHA_CONFIG["mes_cols_row1"])
    for month, col_x in zip(MONTHS[:6], FECHA_CONFIG["mes_cols_row1"]):
        _draw(overlay, thresh, f"Mes {month}", col_x, FECHA_CONFIG["mes_row1"], r)
    for month, col_x in zip(MONTHS[6:], FECHA_CONFIG["mes_cols_row2"]):
        _draw(overlay, thresh, f"Mes {month}", col_x, FECHA_CONFIG["mes_row2"], r)

    # ── Fecha – Year ──────────────────────────────────────────────────────────
    print("\n=== FECHA AÑO ===")
    r = _col_radius(FECHA_CONFIG["anio_cols"])
    for i, row_y in enumerate(FECHA_CONFIG["anio_rows"]):
        for j, col_x in enumerate(FECHA_CONFIG["anio_cols"]):
            _draw(overlay, thresh, f"Año A{i+1} digit={j}", col_x, row_y, r)

    # ── Curso – Type ──────────────────────────────────────────────────────────
    print("\n=== CURSO TIPO ===")
    r = _col_radius(CURSO_CONFIG["tipo_cols"])
    for tipo, col_x in zip(CURSO_TYPES, CURSO_CONFIG["tipo_cols"]):
        _draw(overlay, thresh, f"Tipo {tipo}", col_x, CURSO_CONFIG["tipo_row"], r)

    # ── Curso – Digits ────────────────────────────────────────────────────────
    print("\n=== CURSO DÍGITOS ===")
    r = _col_radius(CURSO_CONFIG["digit_cols"])
    for i, row_y in enumerate(CURSO_CONFIG["digit_rows"]):
        for j, col_x in enumerate(CURSO_CONFIG["digit_cols"]):
            _draw(overlay, thresh, f"C{i+1} digit={j}", col_x, row_y, r)

    # ── Respuestas ────────────────────────────────────────────────────────────
    print("\n=== RESPUESTAS ===")
    for block_name in ("left", "right"):
        block = RESPUESTAS_CONFIG[block_name]
        r = _col_radius(block["cols"])
        for i, row_y in enumerate(block["rows"]):
            q = block["q_start"] + i
            for opt, col_x in zip(ANSWER_OPTIONS, block["cols"]):
                _draw(overlay, thresh, f"Q{q:2d} {opt}", col_x, row_y, r)

    cv2.imwrite(output_path, overlay)
    print(f"\nOverlay saved → {output_path}")
    print("Green = marked (fill > threshold), Red = unmarked")


if __name__ == "__main__":
    main()
