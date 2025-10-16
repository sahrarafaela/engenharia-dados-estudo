import requests
from pyspark.sql.functions import lit
from datetime import datetime
from pyspark.sql import SparkSession


dbutils.widgets.text("data_execucao", "")
data_execucao = dbutils.widgets.get("data_execucao")

def extraindo_dados(date, base="BRL"):
    url = f"https://api.apilayer.com/exchangerates_data/{date}?base={base}"
    headers = {
        "apikey": "kFeXLvg2zmtAw2DEtjzsjE5F4KoAgmi9"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Erro ao extrair dados da API.")
    return response.json()

def dados_para_dataframe(dado_json):
    return [(moeda, float(taxa)) for moeda, taxa in dado_json["rates"].items()]

def salvar_arquivo_parquet(conversoes_extraidas):
    ano, mes, dia = conversoes_extraidas['date'].split('-')
    caminho = f"dbfs:/databricks-results/bronze/{ano}/{mes}/{dia}"
    dados = dados_para_dataframe(conversoes_extraidas)
    df = spark.createDataFrame(dados, schema=['moeda', 'taxa'])
    df = df.withColumn("data", lit(f"{ano}-{mes}-{dia}"))
    df.write.format("parquet").mode("overwrite").save(caminho)
    print(f"Arquivo salvo em: {caminho}")


cotacoes = extraindo_dados(data_execucao)
salvar_arquivo_parquet(cotacoes)
