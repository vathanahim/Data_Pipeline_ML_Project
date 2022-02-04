# import cassandra 
# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider
# import pandas as pd

# def astra_connect():
#     cloud_config= {
#             'secure_connect_bundle': 'secure-connect-capstone-project2.zip'
#     }
#     auth_provider = PlainTextAuthProvider('OZTxZCgzatSukjKBoWpZimZs', 'cfph4pZMPt-REY_B0BTCZ-qxZfwgpIeZA2T69DIzccYlZ2I1+8gKKk6Ruk+G+70.CyFNoZymWef1Eo1KJZk,SjYbo9SgRZwY97JfG6J8uFLvNEJ8,nCjMbcGz.wgmlJC')
#     cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
#     session = cluster.connect('iac689')
#     query = "SELECT * FROM iac689.data_2;"
#     df = pd.DataFrame(list(session.execute(query)))
#     df = df.drop(columns=['ui'])
#     return df