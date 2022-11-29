
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import csv
import requests
import datetime
import pendulum

default_args = {
    'owner': 'eugeny',
    'start_date': days_ago(0),
    'depends_on_past': False
}

dag = DAG('first_dag',
          default_args=default_args,
          start_date=pendulum.datetime(2015, 12, 1, tz="UTC"),
          schedule_interval='@daily',
          catchup=False)

t1 = BashOperator(
        task_id='make_dir',
        bash_command= 'touch data.csv')


def load_data():
    req = requests.get('https://footystats.org/c-dl.php?type=league&comp=1625')
    url_content = req.content
    data = open('data.csv', 'wb')
    data.write(url_content)
    data.close()


t2 = PythonOperator(task_id='download', python_callable=load_data, dag=dag)

t1 >> t2


# In[ ]:




