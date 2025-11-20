# 📘 Estudo de Engenharia de Dados: Procedures, Azure, Databricks e PySpark

Este repositório documenta os principais tópicos que estudei nos últimos dias como parte da minha jornada em Engenharia de Dados. Aqui você encontrará exemplos práticos, anotações técnicas e reflexões sobre:

- Procedures SQL
- Serviços de dados na Azure
- Databricks
- PySpark

---

## 🧩 Sumário

1. [Procedures SQL](#1-procedures-sql)
2. [Azure Data Services](#2-azure-data-services)
3. [Databricks](#3-databricks)
4. [PySpark](#4-pyspark)
5. [Conclusões e próximos passos](#5-conclusões-e-próximos-passos)

---

## 1. Procedures SQL

Durante o estudo de Procedures SQL, desenvolvi uma rotina para automatizar o processo de inclusão de novos registros de aluguel na base de dados insight_places. A procedure novoAluguel_44 realiza diversas validações e cálculos antes de inserir os dados, garantindo integridade e consistência.

[Procedures SQL](procedures_sql/novoAluguel_44.sql)

---

## 2. Azure Data Services

Utilizei o ambiente de notebooks do Azure Databricks para construir um pipeline de ETL que extrai dados de câmbio via API, transforma com PySpark e salva em camadas de Data Lake. Também automatizei o processo com Airflow e integrei com Slack para envio de relatórios.

[Cluster Databricks](azure/databricks_cluster.md)

---

## 3. Databricks

Implementei um pipeline de ETL no ambiente Databricks utilizando PySpark. O fluxo realiza:

- Extração de dados de câmbio via API externa
- Transformações com PySpark, incluindo agregações e conversões de taxa
- Salvamento dos dados em camadas `bronze` e `prata` no Data Lake (`dbfs:/`)
- Geração de arquivos CSV e gráficos
- Envio automático de relatórios e imagens para o Slack
- Automação do processo com Airflow, agendando notebooks diariamente

📁 Arquivos relacionados:

- [ETL de Extração](databricks/etl_extracao.py)
- [Transformações PySpark](databricks/transformacoes.py)
- [Envio para Slack](databricks/slack_envio.py)
- [DAG do Airflow](databricks/airflow_dag.py)

---
