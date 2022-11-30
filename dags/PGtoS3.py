# import datetime
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.utils.dates import days_ago
# from operators.pgtos3 import PostgresToS3Operator
#
# default_args = {
#     'owner': 'eugeny',
#     'start_date': days_ago(0),
#     'depends_on_past': False
# }
#
# dag = DAG('PG_to_S3',
#           default_args=default_args,
#           #start_date=pendulum.datetime(2015, 12, 1, tz="UTC"),
#           schedule_interval='@daily',
#           catchup=False)
#
# t1 = PostgresToS3Operator(task_id = "PG_to_S3",
#                           database = "aws",
#                           host = ,
#                           port = gi,
#                           user = "postgres",
#                           password = "postgres",
#                           region_name = "us-east-1",
#                           access_key = ,
#                           secret_access_key = ,
#                           bucket = "golovanov1",
#                           filename = str(datetime.datetime.now()),
#                           sql = '''select * from countries''',
#                           dag=dag
#                           )
#
#
# t1
#
#
# # In[ ]:
#
#
#
#
