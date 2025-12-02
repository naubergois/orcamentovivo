import argparse
from pathlib import Path

from .data_loader import load_budget_data, monthly_totals
from .digital_twin import DigitalTwin
from .forecasting import forecast_budget


def main() -> None:
    parser = argparse.ArgumentParser(description="Orçamento Vivo - protótipo analítico")
    parser.add_argument(
        "--fonte",
        default=Path("data/execucao_orcamentaria.csv"),
        type=Path,
        help="Caminho do CSV de execução (data,orgao,valor)",
    )
    parser.add_argument("--periodos", type=int, default=6, help="Meses de previsão")
    args = parser.parse_args()

    records = load_budget_data(args.fonte)
    agregados = monthly_totals(records)
    previsoes = forecast_budget(agregados, periods=args.periodos)

    twin = DigitalTwin(agregados)
    agentes = twin.rodar(previsao_periodos=args.periodos)

    print("Previsão de valores médios para os próximos meses:")
    for rec in previsoes:
        print(f"{rec.date.date()} -> R$ {rec.valor:,.2f}")

    print("\nAjustes recomendados por agente:")
    for agente in sorted(agentes.values(), key=lambda a: a.orgao):
        historico_total = sum(rec.valor for rec in agente.historico)
        media = historico_total / len(agente.historico)
        ajustes = ", ".join(agente.ajustes) or "nenhum"
        print(f"{agente.orgao}: média R$ {media:,.2f} | ajustes: {ajustes}")


if __name__ == "__main__":
    main()
