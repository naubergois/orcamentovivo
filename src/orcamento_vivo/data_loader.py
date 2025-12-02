import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


@dataclass
class BudgetRecord:
    """Representa uma linha de execução orçamentária."""

    date: datetime
    orgao: str
    valor: float


def load_budget_data(path: Path) -> List[BudgetRecord]:
    """Carrega dados de um CSV no formato data,orgao,valor."""

    records: List[BudgetRecord] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                BudgetRecord(
                    date=datetime.fromisoformat(row["data"]),
                    orgao=row["orgao"],
                    valor=float(row["valor"]),
                )
            )
    return records


def monthly_totals(records: Iterable[BudgetRecord]) -> List[BudgetRecord]:
    """Agrega os valores por mês (somando por órgão)."""

    totals = {}
    for rec in records:
        key = (rec.date.replace(day=1), rec.orgao)
        totals.setdefault(key, 0.0)
        totals[key] += rec.valor

    aggregated = [
        BudgetRecord(date=key[0], orgao=key[1], valor=value)
        for key, value in sorted(totals.items(), key=lambda item: item[0][0])
    ]
    return aggregated
