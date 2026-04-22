# ---------------------------------------------------------------------------
# Canvas dimensions for the normalised (perspective-corrected) image.
# All coordinate fractions below are relative to this canvas.
# ---------------------------------------------------------------------------
NORMALIZED_W = 1200
NORMALIZED_H = 1700

# ---------------------------------------------------------------------------
# Bubble detection thresholds.
# Coordinates are derived from the jsPDF source (A4 = 210×297 mm):
#   x_frac = x_mm / 210,  y_frac = y_mm / 297
#
# FILL_THRESHOLD  – fill ratio above which a bubble is considered "marked".
# BUBBLE_RADIUS_FRAC – fraction of inter-column spacing → sampling radius.
# MAX_BUBBLE_RADIUS  – hard cap so every section uses the same radius.
#   Physical bubble radius = 2.5 mm → ~14.3 px on canvas.
#   Tightest column gap (fecha/curso digits, 7.5 mm) → 42.9 px * 0.30 = 12.9 px.
#   Setting cap to 12 px gives uniform 12 px across all sections.
# ---------------------------------------------------------------------------
FILL_THRESHOLD = 0.40
BUBBLE_RADIUS_FRAC = 0.30
MAX_BUBBLE_RADIUS = 12.0

# ---------------------------------------------------------------------------
# ID type selector – which identification method is used on this sheet.
# ID_TIPO_DNI: x=40 mm, y=39 mm  →  (40/210, 39/297)
# ID_TIPO_NRO_CONTROL: x=56 mm, y=39 mm
# ---------------------------------------------------------------------------
ID_SELECTOR_CONFIG = {
    "row": 39 / 297,
    "cols": [40 / 210, 56 / 210],
    "labels": ["DNI", "NRO_CONTROL"],
}

# ---------------------------------------------------------------------------
# DNI / Nro de Control digits
# Exact coordinates not yet provided — these are placeholder estimates.
# Calibrate with scripts/calibrate_coords.py once the digit layout is known.
# ---------------------------------------------------------------------------
DNI_CONFIG = {
    "rows": [0.125, 0.147, 0.169, 0.191, 0.213, 0.235, 0.257, 0.279],
    "cols": [0.042, 0.066, 0.090, 0.114, 0.138, 0.162, 0.186, 0.210, 0.234, 0.258],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Fecha
# Source (mm): D1 y=51.5, D2 y=57.5; col0 x=110.5, gap=7.5 mm
#              Mes row1 y=71.5, row2 y=77.5; col0 x=120.5, gap=13 mm
#              A1 y=85.5, A2 y=91.5; col0 x=120.5, gap=7.5 mm
# ---------------------------------------------------------------------------
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

FECHA_CONFIG = {
    "dia_rows": [51.5 / 297, 57.5 / 297],          # [0.1734, 0.1936]
    "dia_cols": [                                    # x/210, gap 7.5 mm
        110.5 / 210, 118.0 / 210, 125.5 / 210, 133.0 / 210, 140.5 / 210,
        148.0 / 210, 155.5 / 210, 163.0 / 210, 170.5 / 210, 178.0 / 210,
    ],
    "mes_row1": 71.5 / 297,                         # 0.2407
    "mes_row2": 77.5 / 297,                         # 0.2609
    "mes_cols_row1": [                               # Ene–Jun, gap 13 mm
        120.5 / 210, 133.5 / 210, 146.5 / 210,
        159.5 / 210, 172.5 / 210, 185.5 / 210,
    ],
    "mes_cols_row2": [                               # Jul–Dic, same x positions
        120.5 / 210, 133.5 / 210, 146.5 / 210,
        159.5 / 210, 172.5 / 210, 185.5 / 210,
    ],
    "anio_rows": [85.5 / 297, 91.5 / 297],          # [0.2879, 0.3081]
    "anio_cols": [                                   # x/210, gap 7.5 mm
        120.5 / 210, 128.0 / 210, 135.5 / 210, 143.0 / 210, 150.5 / 210,
        158.0 / 210, 165.5 / 210, 173.0 / 210, 180.5 / 210, 188.0 / 210,
    ],
}

# ---------------------------------------------------------------------------
# Curso
# Source (mm): tipo y=110, cols x=[14,28,42,56,70,84,98], gap=14 mm
#              C1 y=120.5, C2 y=126.5, C3 y=132.5; col0 x=22, gap=7.5 mm
# ---------------------------------------------------------------------------
CURSO_TYPES = ["RP", "RC", "CM", "CC", "CPD", "CAD", "C"]

CURSO_CONFIG = {
    "tipo_row": 110 / 297,                           # 0.3704
    "tipo_cols": [                                   # gap 14 mm
        14 / 210, 28 / 210, 42 / 210, 56 / 210, 70 / 210, 84 / 210, 98 / 210,
    ],
    "digit_rows": [120.5 / 297, 126.5 / 297, 132.5 / 297],   # [0.4057,0.4259,0.4461]
    "digit_cols": [                                  # x/210, gap 7.5 mm
        22 / 210, 29.5 / 210, 37 / 210, 44.5 / 210, 52 / 210,
        59.5 / 210, 67 / 210, 74.5 / 210, 82 / 210, 89.5 / 210,
    ],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Respuestas
# Source (mm): Q1/Q26 y=151.5, row gap=5.5 mm (→ 25 rows, last at 283.5 mm)
#              Left  cols A–E: x=[22,32,42,52,62], gap=10 mm
#              Right cols A–E: x=[114.5,124.5,134.5,144.5,154.5], gap=10 mm
# ---------------------------------------------------------------------------
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]

_LEFT_Q1_Y = 151.5 / 297       # 0.5101
_RIGHT_Q26_Y = 151.5 / 297     # 0.5101
_ROW_SPACING = 5.5 / 297       # 0.01852

RESPUESTAS_CONFIG = {
    "left": {
        "q_start": 1,
        "rows": [_LEFT_Q1_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [22 / 210, 32 / 210, 42 / 210, 52 / 210, 62 / 210],
    },
    "right": {
        "q_start": 26,
        "rows": [_RIGHT_Q26_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [114.5 / 210, 124.5 / 210, 134.5 / 210, 144.5 / 210, 154.5 / 210],
    },
}
