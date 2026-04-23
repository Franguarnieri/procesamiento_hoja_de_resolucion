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
#   Physical bubble radius ≈ 2.5 mm → ~14.3 px on canvas.
#   Tightest column gap (fecha/curso digits, 7.5 mm) → 42.9 px * 0.42 = 18 px.
#   Setting cap to 11 px gives uniform radius across all sections.
# ---------------------------------------------------------------------------
FILL_THRESHOLD = 0.30
BUBBLE_RADIUS_FRAC = 0.42   # must be >= 11.0/42.86 so even tightest col gap caps at MAX
MAX_BUBBLE_RADIUS = 11.0

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
# D1 y=47.5 … D8 y=89.5, row gap=6.0 mm
# col0 x=22.0, gap=7.5 mm (identical to Curso digit cols)
# ---------------------------------------------------------------------------
DNI_CONFIG = {
    "rows": [47.5/297, 53.5/297, 59.5/297, 65.5/297,
             71.5/297, 77.5/297, 83.5/297, 89.5/297],
    "cols": [22.0/210, 29.5/210, 37.0/210, 44.5/210, 52.0/210,
             59.5/210, 67.0/210, 74.5/210, 82.0/210, 89.5/210],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Fecha
# dia: col0 x=120.8 mm (+18 px cumulative), rows unchanged
# mes: rows −24 px (1 diameter up) from prev
# anio: rows −12 px (1 radius up), cols −3 px (1/8 diam left) from prev
# ---------------------------------------------------------------------------
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

FECHA_CONFIG = {
    "dia_rows": [47.5 / 297, 53.5 / 297],
    "dia_cols": [                                    # x/210, gap 7.5 mm
        120.15 / 210, 127.65 / 210, 135.15 / 210, 142.65 / 210, 150.15 / 210,
        157.65 / 210, 165.15 / 210, 172.65 / 210, 180.15 / 210, 187.65 / 210,
    ],
    "mes_row1": 61.5 / 297,
    "mes_row2": 67.5 / 297,
    "mes_cols_row1": [                               # Ene–Jun, gap 13 mm
        120.15 / 210, 133.15 / 210, 146.15 / 210,
        159.15 / 210, 172.15 / 210, 185.15 / 210,
    ],
    "mes_cols_row2": [                               # Jul–Dic, same x positions
        120.15 / 210, 133.15 / 210, 146.15 / 210,
        159.15 / 210, 172.15 / 210, 185.15 / 210,
    ],
    "anio_rows": [78.1 / 297, 84.1 / 297],
    "anio_cols": [                                   # x/210, gap 7.5 mm
        120.2 / 210, 127.7 / 210, 135.2 / 210, 142.7 / 210, 150.2 / 210,
        157.7 / 210, 165.2 / 210, 172.7 / 210, 180.2 / 210, 187.7 / 210,
    ],
}

# ---------------------------------------------------------------------------
# Curso
# Calibrated offsets vs jsPDF source: y −4 mm.
# tipo y=106; C1 y=116.5, C2 y=122.5, C3 y=128.5; col0 x=22, gap=7.5 mm
# tipo_cols x=[14,28,42,56,70,84,98], gap=14 mm
# ---------------------------------------------------------------------------
CURSO_TYPES = ["RP", "RC", "CM", "CC", "CPD", "CAD", "C"]

CURSO_CONFIG = {
    "tipo_row": 107.6 / 297,                          # +3 px (1/8 diam down)
    "tipo_cols": [                                   # gap 14 mm
        14 / 210, 28 / 210, 42 / 210, 56 / 210, 70 / 210, 84 / 210, 98 / 210,
    ],
    "digit_rows": [118.1 / 297, 124.1 / 297, 130.1 / 297],      # +3 px
    "digit_cols": [                                  # x/210, gap 7.5 mm
        22 / 210, 29.5 / 210, 37 / 210, 44.5 / 210, 52 / 210,
        59.5 / 210, 67 / 210, 74.5 / 210, 82 / 210, 89.5 / 210,
    ],
    "digits": list(range(10)),
}

# ---------------------------------------------------------------------------
# Respuestas
# Calibrated offsets vs jsPDF source: y −4 mm; right cols x +5 mm.
# Q1/Q26 y=147.5, row gap=5.5 mm (→ 25 rows, last at 279.5 mm)
# Left  cols A–E: x=[22,32,42,52,62], gap=10 mm
# Right cols A–E: x=[119.5,129.5,139.5,149.5,159.5], gap=10 mm
# ---------------------------------------------------------------------------
ANSWER_OPTIONS = ["A", "B", "C", "D", "E"]

_LEFT_Q1_Y  = 149.4 / 297                          # +3 px (1/8 diam down)
_RIGHT_Q26_Y = 149.4 / 297
_ROW_SPACING = 5.5 / 297

RESPUESTAS_CONFIG = {
    "left": {
        "q_start": 1,
        "rows": [_LEFT_Q1_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [22 / 210, 32 / 210, 42 / 210, 52 / 210, 62 / 210],
    },
    "right": {
        "q_start": 26,
        "rows": [_RIGHT_Q26_Y + i * _ROW_SPACING for i in range(25)],
        "cols": [120.0 / 210, 130.0 / 210, 140.0 / 210, 150.0 / 210, 160.0 / 210],  # +3 px right
    },
}

# ---------------------------------------------------------------------------
# Fiducial / registration marks – ⊕ symbols printed at 4 known positions.
# Coordinates in mm (jsPDF origin, top-left of A4 page).
# Order: [top-left, top-right, bottom-left, bottom-right]
# ---------------------------------------------------------------------------
FIDUCIAL_MM = [
    (15.0,  29.0),   # F1 – top-left
    (195.0, 29.0),   # F2 – top-right
    (15.0,  288.0),  # F3 – bottom-left
    (195.0, 288.0),  # F4 – bottom-right
]
