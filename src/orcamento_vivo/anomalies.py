import math
from statistics import mean, pstdev
from typing import Iterable, List, Tuple

from .data_loader import BudgetRecord


class AnomalyDetector:
    """Detector simples usando desvio-padrão para marcar outliers."""

    def __init__(self, z_threshold: float = 2.0):
        self.z_threshold = z_threshold

    def _z_score(self, value: float, avg: float, std: float) -> float:
        if std == 0:
            return 0.0
        return (value - avg) / std

    def detect(self, records: Iterable[BudgetRecord]) -> List[Tuple[BudgetRecord, float]]:
        values = [rec.valor for rec in records]
        if not values:
            return []

        avg = mean(values)
        std = pstdev(values)

        anomalies: List[Tuple[BudgetRecord, float]] = []
        for rec in records:
            z = self._z_score(rec.valor, avg, std)
            if math.fabs(z) >= self.z_threshold:
                anomalies.append((rec, z))
        return anomalies
