from pyspark.sql.functions import to_date, first, col, round


df = spark.read.parquet("dbfs:/databricks-results/bronze/*/*/*")


moedas = ['USD', 'EUR', 'GBP']
df_filtrado = df.filter(df.moeda.isin(moedas)).withColumn("data", to_date("data"))


df_taxas = df_filtrado.groupBy("data")\
    .pivot("moeda")\
    .agg(first("taxa"))\
    .orderBy("data", ascending=False)


df_reais = df_taxas
for moeda in moedas:
    df_reais = df_reais.withColumn(moeda, round(1 / col(moeda), 4))


df_taxas = df_taxas.coalesce(1)
df_reais = df_reais.coalesce(1)


df_taxas.write.mode("overwrite").format("csv").option("header", "true")\
    .save("dbfs:/databricks-results/prata/taxas_conversao")

df_reais.write.mode("overwrite").format("csv").option("header", "true")\
    .save("dbfs:/databricks-results/prata/valores_reais")
