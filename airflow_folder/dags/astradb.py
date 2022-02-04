from airflow import DAG
from datetime import date, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator  
import cassandra 
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd

default_args = {
    'owner':'vathana',
    'depends_on_past':False,
    'start_date': datetime(2022, 2, 1),
    'retries': 0
}

def astra_connect(**kwargs):
    cloud_config= {
            'secure_connect_bundle': 'secure-connect-capstone-project2.zip'
    }
    auth_provider = PlainTextAuthProvider('OZTxZCgzatSukjKBoWpZimZs', 'cfph4pZMPt-REY_B0BTCZ-qxZfwgpIeZA2T69DIzccYlZ2I1+8gKKk6Ruk+G+70.CyFNoZymWef1Eo1KJZk,SjYbo9SgRZwY97JfG6J8uFLvNEJ8,nCjMbcGz.wgmlJC')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('iac689')
    query = "SELECT * FROM iac689.data_2;"
    # ti = kwargs['ti']
    df = pd.DataFrame(list(session.execute(query)))
    return print('success')
    # ti.xcom_push('data', df.to_json(default_handler=str))
    

def astra_query(**kwargs):
    # ti = kwargs['ti']
    # extract_data = ti.xcom_pull(task_ids='astra_connect', key='data')
    # df = pd.read_json(extract_data)
    # df.to_csv('data.csv')
    return print('he')
    
    

with DAG(dag_id='Sample_one', 
    default_args=default_args, 
    catchup=False, 
    schedule_interval='@once') as dag:

    start = PythonOperator(task_id='connect_to_astra_db', python_callable=astra_connect)

    end = PythonOperator(task_id='query_from_astra_db', python_callable=astra_query)

start >> end