import numpy as np

from app.config import CURSO_CONFIG, CURSO_TYPES, FILL_THRESHOLD
from app.extractors.base import SectionExtractor
from app.extractors.bubble import sample_bubble


class CursoExtractor(SectionExtractor):
    def __init__(self) -> None:
        super().__init__(FILL_THRESHOLD)

    def _digit_row(
        self,
        warped_thresh: np.ndarray,
        row_y: float,
        cols: list[float],
        digits: list,
        label: str,
    ) -> tuple:
        radius = self.bubble_radius(cols)
        fills = [
            sample_bubble(warped_thresh, *self.to_pixel(cx, row_y), radius)
            for cx in cols
        ]
        return self.pick_marked(fills, digits, label)

    def extract(self, warped_thresh: np.ndarray) -> tuple[dict, list[str]]:
        all_warnings: list[str] = []

        # --- Course type ---
        radius = self.bubble_radius(CURSO_CONFIG["tipo_cols"])
        tipo_fills = [
            sample_bubble(warped_thresh, *self.to_pixel(cx, CURSO_CONFIG["tipo_row"]), radius)
            for cx in CURSO_CONFIG["tipo_cols"]
        ]
        tipo, w = self.pick_marked(tipo_fills, CURSO_TYPES, "Curso tipo")
        all_warnings.extend(w)

        # --- Digit rows C1, C2, C3 ---
        course_digits: list = []
        for i, row_y in enumerate(CURSO_CONFIG["digit_rows"]):
            digit, w = self._digit_row(
                warped_thresh,
                row_y,
                CURSO_CONFIG["digit_cols"],
                CURSO_CONFIG["digits"],
                f"Curso C{i + 1}",
            )
            all_warnings.extend(w)
            course_digits.append(digit)

        return {
            "curso": {
                "tipo": tipo,
                "c1": course_digits[0],
                "c2": course_digits[1],
                "c3": course_digits[2],
            }
        }, all_warnings
