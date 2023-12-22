from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'sarwar',
    'retires': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
    default_args=default_args,
    dag_id='dag_with_minio_s3_v02',
    description='Our first dag using python operator',
    start_date=datetime(2023, 12, 10),
    schedule_interval='@daily',
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_mino_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn',
        mode='poke',
        poke_interval=5,
        timeout=30
    )
    task1