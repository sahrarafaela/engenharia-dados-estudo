from slack_sdk import WebClient
import pyspark.pandas as ps
import os

# Token do Slack
slack_token = "seu_token_slack"
client = WebClient(token=slack_token)

# Caminho do último arquivo CSV gerado
arquivos = dbutils.fs.ls("dbfs:/databricks-results/prata/valores_reais/")
nome_arquivo = sorted(arquivos, key=lambda x: x.modificationTime)[-1].name
path = f"/dbfs/databricks-results/prata/valores_reais/{nome_arquivo}"

# Enviando CSV para o Slack
client.files_upload_v2(
    channel="#id_seu_canal_slack",
    title="Arquivo CSV de valores convertidos",
    file=path,
    filename="valores_reais.csv",
    initial_comment="Segue o arquivo com os valores convertidos:"
)

# Leitura do CSV com pandas API on Spark
df = ps.read_csv(f"dbfs:/databricks-results/prata/valores_reais/{nome_arquivo}")

# Criando pasta local para imagens
os.makedirs("imagens", exist_ok=True)

# Gerando e salvando gráficos
for moeda in df.columns[1:]:
    fig = df.plot.line(x="data", y=moeda, title=f"Cotação {moeda}")
    fig.figure.savefig(f"imagens/{moeda}.png")

# Enviando imagens para o Slack
for moeda in df.columns[1:]:
    client.files_upload_v2(
        channel="#id_seu_canal_slack",
        title=f"Gráfico de {moeda}",
        file=f"imagens/{moeda}.png"
    )