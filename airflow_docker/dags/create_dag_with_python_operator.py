from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'sarwar',
    'retires': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f'hello world; first name: {first_name} last_nam:{last_name} and age: {age}')

def get_name(ti):
    ti.xcom_push(key='first_name', value='golam')
    ti.xcom_push(key='last_name', value='sarwar')

with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v05',
    description='Our first dag using python operator',
    start_date=datetime(2023, 12, 19),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 20}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    task2 >> task1