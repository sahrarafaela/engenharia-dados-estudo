from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

with DAG(
    dag_id='Executando-notebook-etl',
    start_date=datetime(2023, 6, 1),
    schedule_interval="0 9 * * *",  # Executa diariamente às 9h
    catchup=False
) as dag:

    extrair = DatabricksRunNowOperator(
        task_id='extrair_dados',
        databricks_conn_id='databricks_default',
        job_id='seu_job_id_extracao',
        notebook_params={"data_execucao": '{{ ds }}'}
    )

    transformar = DatabricksRunNowOperator(
        task_id='transformar_dados',
        databricks_conn_id='databricks_default',
        job_id='seu_job_id_transformacao'
    )

    enviar = DatabricksRunNowOperator(
        task_id='enviar_relatorio',
        databricks_conn_id='databricks_default',
        job_id='seu_job_id_envio'
    )

    extrair >> transformar >> enviar