import numpy as np

from app.config import FECHA_CONFIG, MONTHS, FILL_THRESHOLD
from app.extractors.base import SectionExtractor
from app.extractors.bubble import sample_bubble


class FechaExtractor(SectionExtractor):
    def __init__(self) -> None:
        super().__init__(FILL_THRESHOLD)

    def _digit_row(
        self,
        warped_thresh: np.ndarray,
        row_y: float,
        cols: list[float],
        label: str,
    ) -> tuple:
        radius = self.bubble_radius(cols)
        fills = [
            sample_bubble(warped_thresh, *self.to_pixel(cx, row_y), radius)
            for cx in cols
        ]
        return self.pick_marked(fills, list(range(10)), label)

    def extract(self, warped_thresh: np.ndarray) -> tuple[dict, list[str]]:
        all_warnings: list[str] = []

        # --- Day ---
        d1, w = self._digit_row(
            warped_thresh, FECHA_CONFIG["dia_rows"][0], FECHA_CONFIG["dia_cols"], "Fecha D1"
        )
        all_warnings.extend(w)
        d2, w = self._digit_row(
            warped_thresh, FECHA_CONFIG["dia_rows"][1], FECHA_CONFIG["dia_cols"], "Fecha D2"
        )
        all_warnings.extend(w)
        dia = f"{d1}{d2}" if d1 is not None and d2 is not None else None

        # --- Month ---
        mes_radius = self.bubble_radius(FECHA_CONFIG["mes_cols_row1"])
        mes_fills: list[float] = []
        for cx in FECHA_CONFIG["mes_cols_row1"]:
            mes_fills.append(
                sample_bubble(warped_thresh, *self.to_pixel(cx, FECHA_CONFIG["mes_row1"]), mes_radius)
            )
        for cx in FECHA_CONFIG["mes_cols_row2"]:
            mes_fills.append(
                sample_bubble(warped_thresh, *self.to_pixel(cx, FECHA_CONFIG["mes_row2"]), mes_radius)
            )
        mes, w = self.pick_marked(mes_fills, MONTHS, "Fecha Mes")
        all_warnings.extend(w)

        # --- Year ---
        a1, w = self._digit_row(
            warped_thresh, FECHA_CONFIG["anio_rows"][0], FECHA_CONFIG["anio_cols"], "Fecha A1"
        )
        all_warnings.extend(w)
        a2, w = self._digit_row(
            warped_thresh, FECHA_CONFIG["anio_rows"][1], FECHA_CONFIG["anio_cols"], "Fecha A2"
        )
        all_warnings.extend(w)
        anio = f"{a1}{a2}" if a1 is not None and a2 is not None else None

        return {
            "fecha": {"dia": dia, "mes": mes, "anio": anio}
        }, all_warnings
