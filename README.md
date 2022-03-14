
# IAC 689-03 Capstone Project

Volvo has millions of data on their testing trucks and they want to use it to group their
trucks based on their customer’s usage. The analysis of the daily duty cycle data will be used in
unsupervised machine learning algorithms of K-Means and DBSCAN. A pairing with PCA will be used if
necessary to determine the best clustering model for the trucks or for visualization purposes. A system of data extraction,
processing and cleaning needs to be created in order to streamline an efficient process of feeding
the data in the best performing machine learning model.




## Author

- [@Vathana Him](https://www.github.com/vathanahim)




## Questions Targeted

- How can we efficiently extract the data for these trucks?

- Which machine learning models can provide the best clustering technique?

- How can we create a efficient system of data extraction and cleaning in order to feed our machine learning model?



## Technology used for this project
- Python 3.7.6
    - Sklearn
    - Pandas
    - Numpy
    - Matplotlib
    - Seaborn
    - Altair
- SQL within MariaDB
- Astra DB
- Apache Cassandra
- Data Pipeline
    - Airflow 2.0
- Devops 
    - Docker
    


## Stages


- Meet with testing engineers and data analytics engineers on the team to understand the process of how the data is collected and what it means
- Find a method to extract the data from their system and process it appropriately before feeding it into the machine learning algorithms
- Determine if PCA is needed to reduce dimensions of the data
- Find the best machine learning model for this dataset by comparing results between K-means and DBSCAN
- Create python functions for extraction and cleaning of data to streamline an efficient process for their data analytics engineers to use in order to feed data into the machine learning model
- If time permits, create an airflow DAG to automate an end-end machine learning model system which includes data extraction, cleaning and processing
- If time permits, ship the airflow framework into a docker compose file so it can be used in other computing platforms


## Project Architecture

<img width="1363" alt="Screen Shot 2022-03-02 at 5 43 59 PM" src="https://user-images.githubusercontent.com/70493707/156462377-04801893-5c94-4097-8020-28d9d8b3141c.png">
