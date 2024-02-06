'''
============================================================================================================
File ini dibuat untuk melakukan automatisasi transform dan load data (fecthing) ke ElasticSearch. 
Adapun dataset yang dipakai adalah dataset mengenai rincian e-commerce di United States pada tahun 2020.
============================================================================================================
'''

# import libraries
from airflow.models import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.utils.task_group import TaskGroup

from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

def load_csv_to_postgres(): # fungsi 1
    database = "airflow" # dari .env (sesuaikan)
    username = "airflow"
    password = "airflow"
    host = "postgres"

    # Membuat URL koneksi PostgreSQL
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    # Gunakan URL ini saat membuat koneksi SQLAlchemy
    engine = create_engine(postgres_url)
    # engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airflow")
    conn = engine.connect()

    df = pd.read_csv('/opt/airflow/dags/P2M3_permata_hajjarianti_raw.csv') # buat docker baca
    df.to_sql('table_m3', conn, index=False, if_exists='replace')  # Menggunakan if_exists='replace' agar tabel digantikan jika sudah ada

def ambil_data():
    # fetch data
    database = "airflow" # dari .env (sesuaikan)
    username = "airflow"
    password = "airflow"
    host = "postgres"

    # Membuat URL koneksi PostgreSQL
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    # Gunakan URL ini saat membuat koneksi SQLAlchemy
    engine = create_engine(postgres_url)

    # engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airflow")
    conn = engine.connect()

    df = pd.read_sql_query("select * from table_m3", conn)
    df.to_csv('/opt/airflow/dags/P2M3_permata_hajjarianti_new.csv', sep=',', index=False)

def preprocessing(): 
    data = pd.read_csv("/opt/airflow/dags/P2M3_permata_hajjarianti_new.csv")

    # Data cleaning

    # Drop missing values 
    data.dropna(inplace=True)

    # Drop data duplicate
    data.drop_duplicates(inplace=True)

    # Replace spaces with underscores and make lowercase in column names
    data.columns = [col.replace(' ', '_').lower() for col in data.columns]

    # Convert 'order_date' column from object to datetime dtype
    data['order_date'] = pd.to_datetime(data['order_date'], errors='coerce')  # 'coerce' will set invalid parsing as NaT



    data.to_csv('/opt/airflow/dags/P2M3_permata_hajjarianti_clean.csv', index=False)
    
def upload_to_elasticsearch():
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dags/P2M3_permata_hajjarianti_clean.csv')
    
    for i, r in df.iterrows():
        doc = r.to_dict()  # Convert the row to a dictionary
        res = es.index(index="table_milestone", id=i+1, 
                       body=doc, 
                       #op_type="index"
                       )
        print(f"Response from Elasticsearch: {res}")

default_args = {
    'owner': 'Permata',
    'start_date': datetime(2023, 12, 24, 12, 00)
}
# mendefine dag agar bisa dibaca di ariflow dengan penjadwalan setiap jam 6.30
with DAG(
    "P2M3_Rian_DAaG",
    description='Milestone_3',
    schedule_interval='30 6 * * *',
    default_args=default_args, 
    catchup=False
) as dag:
    # Task
    load_csv_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres)
    
    # Task: 1
    '''  Fungsi ini ditujukan untuk menjalankan ambil data dari postgresql. '''
    fetching_data = PythonOperator(
        task_id='fetching_data',
        python_callable=ambil_data)

    # Task: 2
    '''  Fungsi ini ditujukan untuk menjalankan pembersihan data.'''
    edit_data = PythonOperator(
        task_id='edit_data',
        python_callable=preprocessing)

    # Task: 3
    '''  Fungsi ini ditujukan untuk menjalankan upload data ke elasticsearch.'''
    upload_data = PythonOperator(
        task_id='upload_data_elastic',
        python_callable=upload_to_elasticsearch)

    # Urutan rangkaian perkerjaan dari task airflow
    # with TaskGroup("processing_tasks") as processing_tasks:
    load_csv_task >> fetching_data >> edit_data >> upload_data      