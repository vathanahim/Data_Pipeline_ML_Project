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
from sklearn.decomposition import PCA

default_args = {
    'owner':'vathana',
    'depends_on_past':False,
    'start_date': datetime(2022, 2, 1),
    'retries': 0
}

def kmeans():
    cloud_config= {
            'secure_connect_bundle': 'secure-connect-capstone-project2.zip'
    }
    auth_provider = PlainTextAuthProvider('OZTxZCgzatSukjKBoWpZimZs', 'cfph4pZMPt-REY_B0BTCZ-qxZfwgpIeZA2T69DIzccYlZ2I1+8gKKk6Ruk+G+70.CyFNoZymWef1Eo1KJZk,SjYbo9SgRZwY97JfG6J8uFLvNEJ8,nCjMbcGz.wgmlJC')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('iac689')
    query = "SELECT * FROM iac689.newdata limit 2000;"

    #get data
    df = pd.DataFrame(list(session.execute(query)))
    sec_col = df.pop('truck_id')
    df.insert(1,'truck_id', sec_col)
    df['datel'] = pd.to_datetime(df['datel'].astype(str))

    #data cleaning
    df = df.dropna()
    df_info = df.iloc[:,:3]
    df_kmeans = df.iloc[:,3:]
   
    #data scaling
    scaler =  MinMaxScaler().fit(df_kmeans)
    df_kmeans_scale = scaler.transform(df_kmeans)

    
    #goes through kmeans process
    km = KMeans(n_clusters = 4, max_iter=150, random_state=123)
    km.fit(df_kmeans_scale)
    labels = km.labels_

    df_cols = df_kmeans.columns.tolist()
    df_scale = pd.DataFrame(df_kmeans_scale, columns=df_cols)
    df_scale['cluster'] = labels

    df_scale.insert(0, 'uid', df_info['ui'].values)
    df_scale.insert(1, 'date', df_info['datel'].values)
    df_scale.insert(2,'truck_id',df_info['truck_id'].values)

    #insert into database
    l = []
    for i in df_scale[['uid','cluster','date','distance_at_diff_altitude','distance_at_diff_engine_speeds','distance_at_diff_roadinclination','distance_at_wheelbased_vehicle_speed','time_at_diff_altitude','time_at_diff_engine_speeds','time_at_diff_roadinclination','time_at_wheelbased_vehicle_speed','truck_id']].columns:
        l.append(df_scale[i].tolist())
    query = """insert into kmeans (uid , cluster, datel , distance_at_diff_altitude , distance_at_diff_engine_speeds , distance_at_diff_roadinclination , distance_at_wheelbased_vehicle_speed , time_at_diff_altitude , time_at_diff_engine_speeds , time_at_diff_roadinclination , time_at_wheelbased_vehicle_speed , truck_id)
    values (?,?,?,?,?,?,?,?,?,?,?,?);"""
    prepared = session.prepare(query)
    execute_concurrent_with_args(session, prepared, zip(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11]))
    session.shutdown()
    return print('kmeans_done')
    

def pca_process():
    cloud_config= {
            'secure_connect_bundle': 'secure-connect-capstone-project2.zip'
    }
    auth_provider = PlainTextAuthProvider('OZTxZCgzatSukjKBoWpZimZs', 'cfph4pZMPt-REY_B0BTCZ-qxZfwgpIeZA2T69DIzccYlZ2I1+8gKKk6Ruk+G+70.CyFNoZymWef1Eo1KJZk,SjYbo9SgRZwY97JfG6J8uFLvNEJ8,nCjMbcGz.wgmlJC')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect('iac689')
    #get data
    query = "SELECT * FROM iac689.kmeans;"
    df = pd.DataFrame(list(session.execute(query)))

    #get data ready for pca
    df_uid = df['uid']
    df_cluster = df['cluster']
    df_pca = df.iloc[:,3:-1]

    #do PCA reduction for visualization
    pca = PCA(n_components=3)
    x_pca = pca.fit_transform(df_pca)

    df_scale_pca = pd.DataFrame(x_pca, columns=['pca_1','pca_2','pca_3'])
    df_scale_pca.insert(0,'uid', df_uid.values)
    df_scale_pca.insert(1, 'clusters', df_cluster.values)

    #insert pca_data into database
    l = []
    for i in df_scale_pca.columns:
        l.append(df_scale_pca[i].tolist())

    query = """insert into pca_result (uid , cluster, pca1, pca2, pca3)
    values (?,?,?,?,?);"""
    prepared = session.prepare(query)
    execute_concurrent_with_args(session, prepared, zip(l[0],l[1],l[2],l[3],l[4]))
    session.shutdown()

    return print('PCA DONE')
    
    

with DAG(dag_id='Sample_one', 
    default_args=default_args, 
    catchup=False, 
    schedule_interval='@once') as dag:

    start = PythonOperator(task_id='process_kmeans', python_callable=kmeans)

    end = PythonOperator(task_id='process_pca', python_callable=pca_process)
    # end = BashOperator(task_id= 'save_csv', bash_command='python3 /Users/vathanahim/Documents/GradSchool/capstone/689_Final_Project/airflow_folder/dags/connect.py')

start >> end