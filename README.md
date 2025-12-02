# Orçamento Vivo

Protótipo simplificado da plataforma de simulação e detecção de anomalias proposta para o ciclo orçamentário brasileiro. O objetivo é oferecer uma base reproduzível, com dados sintéticos, que demonstra:

- Carregamento e agregação de dados orçamentários mensais.
- Previsão de valores futuros usando uma tendência média simples.
- Detecção de anomalias com base em desvio-padrão.
- Gêmeo digital minimalista com agentes reagindo a previsões e anomalias.

## Estrutura do código

- `src/orcamento_vivo/data_loader.py`: lê o CSV de execução e agrega valores por mês e órgão.
- `src/orcamento_vivo/forecasting.py`: aplica uma projeção simples a partir da variação média mensal.
- `src/orcamento_vivo/anomalies.py`: identifica outliers via _z-score_.
- `src/orcamento_vivo/digital_twin.py`: cria agentes para cada órgão e registra ajustes recomendados.
- `src/orcamento_vivo/cli.py`: CLI que conecta os módulos, imprime previsões e ajustes.
- `data/execucao_orcamentaria.csv`: base sintética de execução para demonstração.
- `tests/test_workflow.py`: testes de regressão cobrindo previsão, anomalias e gêmeo digital.

## Como executar

```bash
python -m orcamento_vivo.cli --fonte data/execucao_orcamentaria.csv --periodos 4
```

## Como rodar os testes

```bash
python -m unittest
```
