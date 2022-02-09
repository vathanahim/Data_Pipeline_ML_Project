from airflow import DAG
from datetime import date, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator  
import cassandra 
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent_with_args
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

default_args = {
    'owner':'vathana',
    'depends_on_past':False,
    'start_date': datetime(2022, 2, 1),
    'retries': 0
}

def astra_connect():
    cloud_config= {
            'secure_connect_bundle': 'secure-connect-capstone-project2.zip'
    }
    auth_provider = PlainTextAuthProvider('OZTxZCgzatSukjKBoWpZimZs', 'cfph4pZMPt-REY_B0BTCZ-qxZfwgpIeZA2T69DIzccYlZ2I1+8gKKk6Ruk+G+70.CyFNoZymWef1Eo1KJZk,SjYbo9SgRZwY97JfG6J8uFLvNEJ8,nCjMbcGz.wgmlJC')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('iac689')
    query = "SELECT * FROM iac689.data_2;"

    df = pd.DataFrame(list(session.execute(query)))
    sec_col = df.pop('truck_id')
    df.insert(1,'truck_id', sec_col)
    df['datel'] = pd.to_datetime(df['datel'].astype(str))

    df = df.dropna()
    df_info = df.iloc[:,:3]
    df_kmeans = df.iloc[:,3:]
   

    scaler =  MinMaxScaler().fit(df_kmeans)
    df_kmeans_scale = scaler.transform(df_kmeans)

    

    km = KMeans(n_clusters = 4, max_iter=150, random_state=123)
    km.fit(df_kmeans_scale)
    labels = km.labels_

    df_cols = df_kmeans.columns.tolist()
    df_scale = pd.DataFrame(df_kmeans_scale, columns=df_cols)
    df_scale['cluster'] = labels

    df_scale.insert(0, 'uid', df_info['ui'].values)
    df_scale.insert(1, 'date', df_info['datel'].values)
    df_scale.insert(2,'truck_id',df_info['truck_id'].values)

    l = []
    for i in df_scale[['uid','cluster','date','distance_at_diff_altitude','distance_at_diff_engine_speeds','distance_at_diff_roadinclination','distance_at_wheelbased_vehicle_speed','time_at_diff_altitude','time_at_diff_engine_speeds','time_at_diff_roadinclination','time_at_wheelbased_vehicle_speed','truck_id']].columns:
        l.append(df_scale[i].tolist())
    query = """insert into kmeans (uid , cluster, datel , distance_at_diff_altitude , distance_at_diff_engine_speeds , distance_at_diff_roadinclination , distance_at_wheelbased_vehicle_speed , time_at_diff_altitude , time_at_diff_engine_speeds , time_at_diff_roadinclination , time_at_wheelbased_vehicle_speed , truck_id)
    values (?,?,?,?,?,?,?,?,?,?,?,?);"""
    prepared = session.prepare(query)
    execute_concurrent_with_args(session, prepared, zip(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11]))

    return print(len(df.columns))
    

def astra_query():
    return print('hello')
    
    

with DAG(dag_id='Sample_one', 
    default_args=default_args, 
    catchup=False, 
    schedule_interval='@once') as dag:

    start = PythonOperator(task_id='connect_to_astra_db', python_callable=astra_connect)

    end = PythonOperator(task_id='query_from_astra_db', python_callable=astra_query)
    # end = BashOperator(task_id= 'save_csv', bash_command='python3 /Users/vathanahim/Documents/GradSchool/capstone/689_Final_Project/airflow_folder/dags/connect.py')

start >> end