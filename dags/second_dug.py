from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import pendulum

default_args = {
    'owner': 'eugeny',
    'start_date': days_ago(0),
    'depends_on_past': False,
}

with DAG(
    dag_id = 'a_second_dug',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    t1 = BashOperator(
        task_id='echo_hi',
        bash_command='echo "Hello"',
    )
    t2 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )
    t1 >> t2