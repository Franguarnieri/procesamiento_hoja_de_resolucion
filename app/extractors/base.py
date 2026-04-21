from abc import ABC, abstractmethod

import numpy as np

from app.config import NORMALIZED_W, NORMALIZED_H, BUBBLE_RADIUS_FRAC, MAX_BUBBLE_RADIUS


class SectionExtractor(ABC):
    def __init__(self, fill_threshold: float) -> None:
        self.fill_threshold = fill_threshold

    @abstractmethod
    def extract(self, warped_thresh: np.ndarray) -> tuple[dict, list[str]]:
        """Return (fields_dict, warnings)."""
        ...

    def to_pixel(self, frac_x: float, frac_y: float) -> tuple[int, int]:
        return int(frac_x * NORMALIZED_W), int(frac_y * NORMALIZED_H)

    def bubble_radius(self, col_fracs: list[float]) -> float:
        if len(col_fracs) < 2:
            return 10.0
        spacing = (col_fracs[1] - col_fracs[0]) * NORMALIZED_W
        return min(MAX_BUBBLE_RADIUS, max(5.0, spacing * BUBBLE_RADIUS_FRAC))

    def pick_marked(
        self,
        fill_ratios: list[float],
        labels: list,
        section: str,
    ) -> tuple:
        """
        Choose the marked bubble for a single row.
        Returns (label, warnings): label is None when no mark is found.
        """
        warnings: list[str] = []
        marked = [
            (r, lbl) for r, lbl in zip(fill_ratios, labels) if r > self.fill_threshold
        ]
        if not marked:
            warnings.append(f"{section}: no mark detected")
            return None, warnings
        if len(marked) > 1:
            warnings.append(f"{section}: multiple marks detected")
            marked.sort(key=lambda x: x[0], reverse=True)
        return marked[0][1], warnings
