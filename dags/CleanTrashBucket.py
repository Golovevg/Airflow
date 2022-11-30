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
    deleted_files = os.listdir('/opt/airflow/dags/trashbox')
    def data_for_column(data):
        f = "('"
        s = "'),"
        file_name = str()
        for i in data:
            brackets = (f"{f} {i} {s}")
            file_name += brackets
        return file_name[:-1]

    file_name = data_for_column(deleted_files)
    if len(file_name) == 0:
        print('Nothing to remove')
    else:
        try:
            sql_stmt = "INSERT INTO log_of_delete(file_name) VALUES {}".format(file_name)
            pg_hook = PostgresHook(
                postgres_conn_id='Postgres'
            )
            pg_conn = pg_hook.get_conn()
            cursor = pg_conn.cursor()
            cursor.execute(sql_stmt)
            pg_conn.commit()
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

##to mani time was spent on this task
