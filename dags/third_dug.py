from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'depends_on_past': False,
}

with DAG(
    dag_id = 'a_third_dag',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:
    t1 = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="airflow",
        sql="""
            CREATE TABLE IF NOT EXISTS currency_pair_10 (
            date_scrapping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            price NUMERIC NOT NULL,
            pair VARCHAR
            );
          """,
    )

    t2 = PostgresOperator(
        task_id="insert_table",
        postgres_conn_id="airflow",
        sql="""
             INSERT INTO currency_pair_10 (date_scrapping, price)
             VALUES (default, 1234)
             ;
           """
    )

    t1 >> t2


