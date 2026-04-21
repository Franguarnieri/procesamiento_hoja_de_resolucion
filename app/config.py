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
FILL_THRESHOLD = 0.55
BUBBLE_RADIUS_FRAC = 0.35
MAX_BUBBLE_RADIUS = 18.0

# ---------------------------------------------------------------------------
# DNI
# 8 rows (D1–D8), each row has 10 bubbles for digits 0–9.
# NOTE: these are estimated values – calibrate with calibrate_coords.py.
# ---------------------------------------------------------------------------
DNI_CONFIG = {
    "rows": [0.160, 0.190, 0.220, 0.250, 0.280, 0.310, 0.340, 0.370],
    "cols": [0.080, 0.117, 0.154, 0.191, 0.228, 0.265, 0.302, 0.339, 0.376, 0.413],
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
    "dia_rows": [0.160, 0.190],
    "dia_cols": [0.550, 0.587, 0.624, 0.661, 0.698,
                 0.735, 0.772, 0.809, 0.846, 0.883],
    "mes_row1": 0.265,
    "mes_row2": 0.295,
    "mes_cols_row1": [0.555, 0.627, 0.699, 0.771, 0.843, 0.915],
    "mes_cols_row2": [0.555, 0.627, 0.699, 0.771, 0.843, 0.915],
    "anio_rows": [0.345, 0.375],
    "anio_cols": [0.550, 0.587, 0.624, 0.661, 0.698,
                  0.735, 0.772, 0.809, 0.846, 0.883],
}

# ---------------------------------------------------------------------------
# Curso
# Type: one row with 7 options (RP, RC, CM, CC, CPD, CAD, C)
# Digits: C1, C2, C3 rows × digits 0–9
# ---------------------------------------------------------------------------
CURSO_TYPES = ["RP", "RC", "CM", "CC", "CPD", "CAD", "C"]

CURSO_CONFIG = {
    "tipo_row": 0.470,
    "tipo_cols": [0.080, 0.132, 0.184, 0.236, 0.300, 0.362, 0.422],
    "digit_rows": [0.520, 0.550, 0.580],
    "digit_cols": [0.080, 0.117, 0.154, 0.191, 0.228,
                   0.265, 0.302, 0.339, 0.376, 0.413],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Respuestas
# 50 questions × 5 options (A–E).
# Questions 1–25 in the left block, 26–50 in the right block.
# ---------------------------------------------------------------------------
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]

_LEFT_Q1_Y = 0.660
_RIGHT_Q26_Y = 0.660
_ROW_SPACING = 0.0125

RESPUESTAS_CONFIG = {
    "left": {
        "q_start": 1,
        "rows": [_LEFT_Q1_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [0.080, 0.122, 0.164, 0.206, 0.248],
    },
    "right": {
        "q_start": 26,
        "rows": [_RIGHT_Q26_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [0.550, 0.592, 0.634, 0.676, 0.718],
    },
}
