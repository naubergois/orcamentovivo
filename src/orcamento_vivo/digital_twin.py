from dataclasses import dataclass
from typing import Dict, Iterable, List

from .anomalies import AnomalyDetector
from .data_loader import BudgetRecord
from .forecasting import forecast_budget


@dataclass
class BudgetAgent:
    """Agente simplificado que reage a previsões e anomalias."""

    orgao: str
    historico: List[BudgetRecord]
    ajustes: List[str]

    def analisar(self, previsoes: List[BudgetRecord], anomalias: List[BudgetRecord]) -> None:
        tendencia = sum(rec.valor for rec in previsoes) / len(previsoes) if previsoes else 0
        media_atual = sum(rec.valor for rec in self.historico) / len(self.historico)
        if tendencia > 1.05 * media_atual:
            self.ajustes.append("expansao")
        elif tendencia < 0.95 * media_atual:
            self.ajustes.append("contencao")
        else:
            self.ajustes.append("estavel")

        if any(rec.orgao == self.orgao for rec in anomalias):
            self.ajustes.append("investigar")


class DigitalTwin:
    """Orquestra os componentes centrais do protótipo."""

    def __init__(self, records: Iterable[BudgetRecord]):
        self.records = list(records)
        self.agentes: Dict[str, BudgetAgent] = {}
        self.anomaly_detector = AnomalyDetector()
        self._registrar_agentes()

    def _registrar_agentes(self) -> None:
        for rec in self.records:
            self.agentes.setdefault(rec.orgao, BudgetAgent(orgao=rec.orgao, historico=[], ajustes=[]))
            self.agentes[rec.orgao].historico.append(rec)

    def rodar(self, previsao_periodos: int = 6) -> Dict[str, BudgetAgent]:
        previsoes = forecast_budget(self.records, periods=previsao_periodos)
        anomalias = [item[0] for item in self.anomaly_detector.detect(self.records)]

        for agente in self.agentes.values():
            agente.analisar(previsoes, anomalias)
        return self.agentes
