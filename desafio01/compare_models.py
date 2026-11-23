"""Desafio 1: compara @champion e @challenger no MESMO conjunto de teste.

Rode da raiz do repositório:
    python desafio01/compare_models.py              # só compara (é o que o estágio `compare` roda)
    python desafio01/compare_models.py --promover   # compara e aplica a decisão no Registry

Complete os 3 trechos marcados com TODO.
"""
import argparse
import json
import sys
from pathlib import Path

import mlflow
import pandas as pd
from mlflow import MlflowClient

sys.path.insert(0, "src")
from bike import MODEL_NAME, regression_metrics, tracking_uri, xy  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--promover", action="store_true", help="aplica a decisão no Registry")
args = parser.parse_args()

mlflow.set_tracking_uri(tracking_uri())
client = MlflowClient()

# 1) O candidato é a versão criada pelo último treino do pipeline
nova_versao = json.load(open("models/run.json"))["model_version"]
client.set_registered_model_alias(MODEL_NAME, "challenger", nova_versao)

# 2) O mesmo teste para os dois: o período mais recente
test = pd.read_csv("data/split/test.csv")
X, y = xy(test)

resultado = {}
for alias in ["champion", "challenger"]:
    versao = int(client.get_model_version_by_alias(MODEL_NAME, alias).version)
    # TODO 1: carregue o modelo pelo alias (dica: mlflow.pyfunc.load_model, como na função avaliar da T3)
    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}@{alias}")
    # TODO 2: calcule as métricas desse modelo em X, y (dica: regression_metrics)
    metricas = regression_metrics(y, model.predict(X))
    resultado[alias] = {"versao": versao, **metricas}

resultado["teste"] = {"inicio": test["dteday"].min(), "fim": test["dteday"].max(), "linhas": len(test)}
Path("reports").mkdir(exist_ok=True)
json.dump(resultado, open("reports/comparacao.json", "w"), indent=2)

champ, chall = resultado["champion"], resultado["challenger"]
print(pd.DataFrame({"champion": champ, "challenger": chall}).T.round(3))
periodo = f"{test['dteday'].min()} a {test['dteday'].max()}"
print(f"\nTeste: {periodo} ({len(test)} linhas)")

# TODO 3: a regra de decisão. O challenger vence se o RMSE dele for menor que o do champion
venceu = chall["rmse"] < champ["rmse"]
print(f"Challenger {'VENCEU' if venceu else 'NÃO venceu'}: "
      f"RMSE {chall['rmse']:.1f} vs {champ['rmse']:.1f} (champion)")

# 3) Decisão de governança, registrada na própria versão (só com --promover)
if args.promover:
    v = str(chall["versao"])
    motivo = f"RMSE {chall['rmse']:.1f} vs {champ['rmse']:.1f} do champion v{champ['versao']} no teste {periodo}"
    client.set_model_version_tag(MODEL_NAME, v, "motivo", motivo)
    if venceu:
        client.set_model_version_tag(MODEL_NAME, v, "decisao", "promovido")
        client.set_model_version_tag(MODEL_NAME, v, "validation_status", "approved")
        client.set_model_version_tag(MODEL_NAME, v, "previous_champion", str(champ["versao"]))
        client.set_registered_model_alias(MODEL_NAME, "champion", v)
        client.delete_registered_model_alias(MODEL_NAME, "challenger")
        print(f"✅ Promovido: champion -> versão {v} (anterior: {champ['versao']})")
    else:
        client.set_model_version_tag(MODEL_NAME, v, "decisao", "rejeitado")
        print(f"❌ Rejeitado: champion continua na versão {champ['versao']}")
