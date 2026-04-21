import numpy as np

from app.config import DNI_CONFIG, FILL_THRESHOLD
from app.extractors.base import SectionExtractor
from app.extractors.bubble import sample_bubble


class DniExtractor(SectionExtractor):
    def __init__(self) -> None:
        super().__init__(FILL_THRESHOLD)

    def extract(self, warped_thresh: np.ndarray) -> tuple[dict, list[str]]:
        all_warnings: list[str] = []
        radius = self.bubble_radius(DNI_CONFIG["cols"])
        digits: list[str] = []

        for row_idx, row_y in enumerate(DNI_CONFIG["rows"]):
            fills = [
                sample_bubble(warped_thresh, *self.to_pixel(col_x, row_y), radius)
                for col_x in DNI_CONFIG["cols"]
            ]
            digit, warnings = self.pick_marked(
                fills, DNI_CONFIG["digits"], f"DNI D{row_idx + 1}"
            )
            all_warnings.extend(warnings)
            digits.append(str(digit) if digit is not None else "?")

        dni_str = "".join(digits)
        return {"dni": None if "?" in dni_str else dni_str}, all_warnings
