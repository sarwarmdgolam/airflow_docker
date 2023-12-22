from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner': 'sarwar',
    'retires': 5,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='dag_with_taskflow_api_v01',
     default_args=default_args,
     start_date=datetime(2023, 12, 19),
     schedule_interval='@daily')
def hello_world_etl():

    @task()
    def get_name():
        return 'Golam Sarwar'

    @task()
    def get_age():
        return 39

    @task()
    def greet(name, age):
        print(f'Hello my name: {name} and age: {age}')

    name = get_name()
    age = get_age()
    greet(name=name, age=age)

greet_dag = hello_world_etl()