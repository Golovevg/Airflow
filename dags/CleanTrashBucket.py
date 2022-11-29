from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import os
import sys

import pandas as pd
import csv
import requests
import datetime
import pendulum

default_args = {
    'owner': 'Eugeny Golovanov',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email': ['airflow.golovanov@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),

}

dag = DAG('Clean Trash Bucket',
          default_args=default_args,
          schedule_interval='0 * * * *',
          catchup=False)






def clean_bucket():
    os.chdir('/Users/eugenygolovanov/Library/Mobile Documents/com~apple~CloudDocs/.Trash')
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-t' or sys.argv[1] == '-T':
            os.system("tree ./")
    elif sys.argv[1] == '-l' or sys.argv[1] == '-L':
        os.system("ls -al")
    else:
    print("Nothing in the bin to delete")
    os.system("rm -rf *")

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
