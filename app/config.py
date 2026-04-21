# ---------------------------------------------------------------------------
# Canvas dimensions for the normalised (perspective-corrected) image.
# All coordinate fractions below are relative to this canvas.
# ---------------------------------------------------------------------------
NORMALIZED_W = 1200
NORMALIZED_H = 1700

# ---------------------------------------------------------------------------
# Bubble detection thresholds.
# FILL_THRESHOLD  – fill ratio above which a bubble is considered "marked".
#                   Tune with scripts/calibrate_coords.py on real scans.
# BUBBLE_RADIUS_FRAC – fraction of the inter-column spacing used as the
#                      sampling circle radius.
# MAX_BUBBLE_RADIUS  – hard cap in pixels to prevent oversized samples in
#                      sections where column labels are far apart (e.g. Mes).
# ---------------------------------------------------------------------------
FILL_THRESHOLD = 0.40
BUBBLE_RADIUS_FRAC = 0.30
MAX_BUBBLE_RADIUS = 15.0

# ---------------------------------------------------------------------------
# DNI
# 8 rows (D1–D8), each row has 10 bubbles for digits 0–9.
# NOTE: these are estimated values – calibrate with calibrate_coords.py.
# ---------------------------------------------------------------------------
DNI_CONFIG = {
    "rows": [0.125, 0.147, 0.169, 0.191, 0.213, 0.235, 0.257, 0.279],
    "cols": [0.042, 0.066, 0.090, 0.114, 0.138, 0.162, 0.186, 0.210, 0.234, 0.258],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Fecha
# Day : D1, D2 rows × digits 0–9
# Mes : two rows of 6 months each (Ene–Jun / Jul–Dic)
# Year: A1, A2 rows × digits 0–9
# ---------------------------------------------------------------------------
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

FECHA_CONFIG = {
    "dia_rows": [0.125, 0.147],
    "dia_cols": [0.516, 0.541, 0.567, 0.592, 0.617,
                 0.642, 0.667, 0.692, 0.717, 0.742],
    "mes_row1": 0.178,
    "mes_row2": 0.201,
    "mes_cols_row1": [0.516, 0.561, 0.607, 0.652, 0.697, 0.742],
    "mes_cols_row2": [0.516, 0.561, 0.607, 0.652, 0.697, 0.742],
    "anio_rows": [0.246, 0.267],
    "anio_cols": [0.516, 0.541, 0.567, 0.592, 0.617,
                  0.642, 0.667, 0.692, 0.717, 0.742],
}

# ---------------------------------------------------------------------------
# Curso
# Type: one row with 7 options (RP, RC, CM, CC, CPD, CAD, C)
# Digits: C1, C2, C3 rows × digits 0–9
# ---------------------------------------------------------------------------
CURSO_TYPES = ["RP", "RC", "CM", "CC", "CPD", "CAD", "C"]

CURSO_CONFIG = {
    "tipo_row": 0.320,
    "tipo_cols": [0.042, 0.118, 0.188, 0.256, 0.329, 0.396, 0.456],
    "digit_rows": [0.358, 0.379, 0.401],
    "digit_cols": [0.042, 0.066, 0.090, 0.114, 0.138,
                   0.162, 0.186, 0.210, 0.234, 0.258],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Respuestas
# 50 questions × 5 options (A–E).
# Questions 1–25 in the left block, 26–50 in the right block.
# ---------------------------------------------------------------------------
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]

_LEFT_Q1_Y = 0.425
_RIGHT_Q26_Y = 0.425
_ROW_SPACING = 0.023

RESPUESTAS_CONFIG = {
    "left": {
        "q_start": 1,
        "rows": [_LEFT_Q1_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [0.069, 0.101, 0.134, 0.167, 0.199],
    },
    "right": {
        "q_start": 26,
        "rows": [_RIGHT_Q26_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [0.530, 0.562, 0.594, 0.626, 0.658],
    },
}
