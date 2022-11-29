import csv
from airflow.models.baseoperator import BaseOperator
import boto3
import psycopg2
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os.path



class PostgresToS3Operator(BaseOperator):

    ui_color = '#D133FF'

    def __init__(self, database: str, host: str, port: str, user:str, password:int,
                region_name:str, access_key: str, secret_access_key: str, sql:str,
                 bucket: str, filename: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.region_name = region_name
        self.access_key =access_key
        self.secret_access_key = secret_access_key
        self.sql = sql
        self.bucket = bucket
        self.filename = filename


    def execute(self, context):
        self.s3()

    def postgres(self):
        conn = psycopg2.connect(
            database=self.database, user=self.user,
            password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(self.sql)
        df = pd.DataFrame(cursor.fetchall())
        results = df.to_csv(index=False)

        return(results)
        cursor.close()
        conn.commit()
        conn.close()


    def s3(self):
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key
        )
        s3 = session.resource('s3')
        data = self.postgres()
        object = s3.Object(self.bucket, self.filename)
        return object.put(Body=data)




    #



    # hook = PostgresHook(postgres_con_id = self.database)
    # conn = hook.get_conn()
    # cursor = conn.cursor()
    # cursor.execute(self.sql)
    # with open("/opt/airflow/data", "w") as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerows(cursor)
    #     cursor.close()









    #
    # def SayHallo(self):
    #     print(self.host)




        #
        #
        # conn = psycopg2.connect(
        #     host="localhost",
        #     database="suppliers",
        #     user="postgres",
        #     password="Abcd1234")
        #
        #
        #
        #
        # s3 = boto3.resource(
        #     service_name='s3',
        #     region_name='us-east-2',
        #     aws_access_key_id='mykey',
        #     aws_secret_access_key='mysecretkey'
        # )
