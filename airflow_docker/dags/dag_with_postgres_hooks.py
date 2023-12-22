import csv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tempfile import NamedTemporaryFile
import logging

default_args = {
    'owner': 'sarwar',
    'retires': 5,
    'retry_delay': timedelta(minutes=10)
}


def postgres_to_s3(ds_nodash, next_ds_nodash):
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from public.orders where date >= %s and date <= %s", (ds_nodash, next_ds_nodash))
    with NamedTemporaryFile(mode="w", suffix=f"{ds_nodash}") as f:
    # with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info('Saved orders in file: %s', f"dags/get_orders_{ds_nodash}.txt")

        s3_hook = S3Hook(
            aws_conn_id='minio_conn'
        )
        s3_hook.load_file(
            filename=f.name,
            key=f'orders/{ds_nodash}.txt',
            bucket_name='airflow',
            replace=True
        )
        logging.info('Orders file %s is pushed to s3', f.name)

with DAG(
    default_args=default_args,
    dag_id='dag_with_postgres_hooks_v04',
    description='Our first dag using python operator',
    start_date=datetime(2023, 12, 10),
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3,
    )
    task1