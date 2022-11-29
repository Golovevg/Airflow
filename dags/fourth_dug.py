from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'eugeny',
    'start_date': days_ago(0),
    'depends_on_past': False
}

with DAG(
    'a_fourth_dug',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    t1 = BashOperator(
        task_id='make_dir',
        bash_command= 'mkdir test_directory'
    )


    t2 = BashOperator(
        task_id='fill_dir',
        bash_command= 'echo 333 > test_directory'
    )

    t3 = BashOperator(
        task_id='rm_dir',
        bash_command= 'rm -rf test_directory'
    )

    t1 >> t2 >> t3
