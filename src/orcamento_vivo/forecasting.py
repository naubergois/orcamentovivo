from datetime import datetime
from typing import Iterable, List, Tuple

from .data_loader import BudgetRecord


def _average_delta(series: List[Tuple[datetime, float]]) -> float:
    deltas = []
    for (prev_date, prev_value), (curr_date, curr_value) in zip(series, series[1:]):
        months = (curr_date.year - prev_date.year) * 12 + (curr_date.month - prev_date.month)
        if months == 0:
            continue
        deltas.append((curr_value - prev_value) / months)
    return sum(deltas) / len(deltas) if deltas else 0.0


def forecast_budget(records: Iterable[BudgetRecord], periods: int = 6) -> List[BudgetRecord]:
    """Gera previsão simples baseada na média do crescimento mensal."""

    series = sorted(((rec.date, rec.valor) for rec in records), key=lambda item: item[0])
    if not series:
        return []

    avg_delta = _average_delta(series)
    last_date, last_value = series[-1]
    forecasts: List[BudgetRecord] = []

    for step in range(1, periods + 1):
        month_increment = (last_date.month - 1 + step) % 12 + 1
        year_increment = (last_date.year + (last_date.month - 1 + step) // 12)
        next_date = last_date.replace(year=year_increment, month=month_increment)
        next_value = last_value + avg_delta * step
        forecasts.append(BudgetRecord(date=next_date, orgao="previsao", valor=round(next_value, 2)))

    return forecasts
