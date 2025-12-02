import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.append(str(ROOT / "src"))

from orcamento_vivo.anomalies import AnomalyDetector
from orcamento_vivo.data_loader import load_budget_data, monthly_totals
from orcamento_vivo.digital_twin import DigitalTwin
from orcamento_vivo.forecasting import forecast_budget


class WorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        caminho = ROOT / "data" / "execucao_orcamentaria.csv"
        self.records = load_budget_data(caminho)

    def test_forecast_returns_expected_periods(self):
        aggregated = monthly_totals(self.records)
        previsoes = forecast_budget(aggregated, periods=3)
        self.assertEqual(len(previsoes), 3)
        self.assertEqual(previsoes[0].orgao, "previsao")

    def test_anomaly_detection_flags_outlier(self):
        detector = AnomalyDetector(z_threshold=1.5)
        aggregated = monthly_totals(self.records)
        anomalies = detector.detect(aggregated)
        labels = {rec.orgao for rec, _ in anomalies}
        self.assertIn("Infraestrutura", labels)

    def test_digital_twin_registers_agents(self):
        aggregated = monthly_totals(self.records)
        twin = DigitalTwin(aggregated)
        agentes = twin.rodar(previsao_periodos=2)
        self.assertGreaterEqual(len(agentes), 3)
        for agente in agentes.values():
            self.assertTrue(agente.ajustes)


if __name__ == "__main__":
    unittest.main()
