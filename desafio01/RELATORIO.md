# Desafio 1: relatório

**Aluno(a):**

## 1. Versões dos dados

Rode o comando abaixo e complete a tabela com os 8 primeiros caracteres de cada md5:

```bash
for tag in dados-v1 dados-v2 dados-v3; do
  echo "$tag $(git show $tag:data/raw/bike.csv.dvc | awk '/md5/{print $3}')"
done
```

| Tag | md5 (8 primeiros caracteres) | Período |
|---|---|---|
| `dados-v1` | `fc7d423a` | 01/01/2011 a 31/12/2011 |
| `dados-v2` | `11e40c60` | 01/01/2011 a 30/06/2012 |
| `dados-v3` | `7747b2ef` | 01/01/2011 a 31/12/2012 |

## 2. Comparação no mesmo teste

Copie os números de `reports/comparacao.json`.

**Período do teste:**2012-12-04 a 2012-12-31 (670 linhas)

| Alias | Versão | RMSE | MAE | R² |
|---|---|---|---|---|
| `@champion` | 7 | 90.753 | 62.872 | 0.683 |
| `@challenger` | 11 | 64.602 | 43.847 | 0.839 |

## 3. Decisão

**Promovido ou rejeitado?** Promovido.

**Justificativa:** A versão 11 foi promovida porque teve RMSE menor que o champion no mesmo teste: 64.6 contra 90.8. Ela também teve MAE menor e R² maior, indicando melhor desempenho nesse período.

## 4. O que cada ferramenta fez nesse projeto?

**Pergunta 01:**
Com suas palavras, quais os dois usos do DVC nesse projeto?
O DVC foi usado para versionar os dados e para organizar as etapas do pipeline, permitindo reproduzir o processo.


**Pergunta 02:**
Com suas palavras, para que serve o MLflow nesse projeto?
O MLflow foi usado para registrar as execuções, métricas e versões dos modelos. Seu Registry permitiu comparar os modelos e controlar qual versão estava como champion.

