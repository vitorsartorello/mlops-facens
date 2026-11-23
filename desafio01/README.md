# Desafio 1: chegaram dados novos

**Contexto.** É janeiro de 2013. O time de operações exportou os dados do 2º semestre de 2012.
Sua missão: versionar os dados, retreinar com o pipeline e **decidir, com evidência**, se o
modelo novo deve substituir o `@champion`.

**Pré-requisitos:** T0–T4 concluídas no seu Codespace e o servidor MLflow no ar
(`bash scripts/start_mlflow.sh` em um terminal).

**Antes de começar:** arraste a pasta `desafio01/` para a raiz do seu repositório no Codespace
(no explorador de arquivos, ao lado de `src/` e `params.yaml`).

**O que você recebe e o que você constrói:**

| O que você recebe | O que você constrói |
|---|---|
| Os comandos para versionar os dados v3 (abaixo) | A versão `dados-v3` |
| `desafio01/compare_models.py`, com a estrutura da comparação | Os 3 trechos marcados com `TODO` (carregar, medir, decidir) |
| O pipeline da T1, com 5 estágios | O 6º estágio, `compare`, no `dvc.yaml` |
| `desafio01/RELATORIO.md`, com as seções | As tabelas e a decisão justificada |

## Passo 1: dados v3 (a receita da T4)

```bash
python src/get_data.py --until 2012-12-31
dvc add data/raw/bike.csv
git add data/raw/bike.csv.dvc
git commit -m "Dados v3: 2012 completo"
git tag dados-v3
dvc push
```

## Passo 2: complete o `compare_models.py`

Abra `desafio01/compare_models.py` e complete os 3 `TODO`. As dicas estão no próprio arquivo.
O script avalia `@champion` e `@challenger` **no mesmo teste** e grava `reports/comparacao.json`.

## Passo 3: escreva o estágio `compare` no `dvc.yaml`

Acrescente um 6º estágio no fim do `dvc.yaml`, no mesmo molde dos estágios da T1:

| Chave | O que colocar |
|---|---|
| `cmd` | `python desafio01/compare_models.py` |
| `deps` | o próprio script, a pasta `models` e `data/split/test.csv` |
| `metrics` | `reports/comparacao.json`, com `cache: false` (igual ao `metrics.json` do `evaluate`) |

Confira com `dvc dag`: o `compare` deve aparecer depois do `train`.

## Passo 4: retreinar e comparar

```bash
dvc repro                    # prepare → split → train (nova versão no Registry) → evaluate, plot e compare
cat reports/comparacao.json
dvc metrics diff             
dvc push
```

## Passo 5: decidir

```bash
python desafio01/compare_models.py --promover
```

Com `--promover`, o script aplica a decisão no Registry: grava as tags `decisao` e `motivo` na versão nova
e, se ela venceu, move o `@champion` (guardando `previous_champion`). Confira na interface: **Models → bike-demand**.

## Passo 6: relatório

Preencha `desafio01/RELATORIO.md`. As instruções estão em cada seção.

## Passo 7: entrega

```bash
git add dvc.yaml dvc.lock metrics.json reports/ desafio01/
git commit -m "Desafio 1: dados v3, estágio compare e decisão"
git push
git push --tags
```

Envie o link do repositório no Canvas.

## Critérios de avaliação (10 pontos)

| Critério | O que vou conferir no repositório | Pontos |
|---|---|---|
| Dados v3 versionados | tag `dados-v3`, `bike.csv.dvc` no Git, `dvc push` feito | 2 |
| Estágio `compare` | no `dvc.yaml` e no `dvc.lock` (6 estágios) | 3 |
| Comparação justa | `compare_models.py` completo e `reports/comparacao.json` commitado | 1 |
| Governança | `@champion` correto; tags `decisao`, `motivo` e `previous_champion` | 1 |
| Relatório | tabelas preenchidas e decisão justificada | 3 |

> 💡 O MLflow desta aula vive **dentro do seu Codespace**. Não apague o Codespace antes da Aula 2.
> Codespaces parados são apagados automaticamente após um período sem uso (30 dias, por padrão).
