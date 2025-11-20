from slack_sdk import WebClient
import pyspark.pandas as ps
import os


slack_token = ""
client = WebClient(token=slack_token)


arquivos = dbutils.fs.ls("dbfs:/databricks-results/prata/valores_reais/")
nome_arquivo = sorted(arquivos, key=lambda x: x.modificationTime)[-1].name
path = f"/dbfs/databricks-results/prata/valores_reais/{nome_arquivo}"


client.files_upload_v2(
    channel="#id_seu_canal_slack",
    title="Arquivo CSV de valores convertidos",
    file=path,
    filename="valores_reais.csv",
    initial_comment="Segue o arquivo com os valores convertidos:"
)


df = ps.read_csv(f"dbfs:/databricks-results/prata/valores_reais/{nome_arquivo}")


os.makedirs("imagens", exist_ok=True)


for moeda in df.columns[1:]:
    fig = df.plot.line(x="data", y=moeda, title=f"Cotação {moeda}")
    fig.figure.savefig(f"imagens/{moeda}.png")


for moeda in df.columns[1:]:
    client.files_upload_v2(
        channel="#id_seu_canal_slack",
        title=f"Gráfico de {moeda}",
        file=f"imagens/{moeda}.png"
    )
