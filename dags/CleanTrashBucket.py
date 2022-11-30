from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import os
from datetime import timedelta, datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook


default_args = {
    'owner': 'Eugeny Golovanov',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['airflow.golovanov@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': False,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('clean_trash_bucket',
          default_args=default_args,
          schedule_interval='0 * * * *',
          catchup=False
          )

def clean_bucket():
    os.chdir('/opt/airflow/dags/trashbox')
    deleted_files = os.system("ls")
    try:
        sql_stmt = "create table if not exists log_of_delete(file_id serial, file_name varchar)"
        pg_hook = PostgresHook(
            postgres_conn_id='postgres',
            schema='public'
        )
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(sql_stmt)
        return cursor.fetchall()
        print('Connection has been establish')
        os.system("rm -rf *")
        print("The folowing files have been removed", deleted_files)
    except TypeError:
        print("Oops! Something went wrong.")

t1 = PythonOperator(
        task_id='clean_bucket',
        python_callable=clean_bucket,
        dag=dag
)

t1