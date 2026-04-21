import numpy as np

from app.config import RESPUESTAS_CONFIG, ANSWER_OPTIONS, FILL_THRESHOLD
from app.extractors.base import SectionExtractor
from app.extractors.bubble import sample_bubble


class RespuestasExtractor(SectionExtractor):
    def __init__(self) -> None:
        super().__init__(FILL_THRESHOLD)

    def extract(self, warped_thresh: np.ndarray) -> tuple[dict, list[str]]:
        all_warnings: list[str] = []
        respuestas: dict[str, str | None] = {}

        for block_name in ("left", "right"):
            block = RESPUESTAS_CONFIG[block_name]
            q_start: int = block["q_start"]
            rows: list[float] = block["rows"]
            cols: list[float] = block["cols"]
            radius = self.bubble_radius(cols)

            for i, row_y in enumerate(rows):
                q_num = str(q_start + i)
                fills = [
                    sample_bubble(warped_thresh, *self.to_pixel(cx, row_y), radius)
                    for cx in cols
                ]
                answer, w = self.pick_marked(fills, ANSWER_OPTIONS, f"Respuesta {q_num}")
                all_warnings.extend(w)
                respuestas[q_num] = answer

        return {"respuestas": respuestas}, all_warnings
