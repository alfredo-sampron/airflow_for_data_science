from airflow import DAG
# así le indicamos a airflow que esto es una DAG para levantar
from airflow.providers.postgres.operators.postgres import PostgresOperator 

from datetime import datetime

with DAG("user_processing",                     
         # este es el nombre del DAG, tiene que ser único
         start_date=datetime(2023,1,1),     
         # acá iniciará/debería haber iniciado a correr el DAG.
         schedule_interval="@daily",            
         # esto toma sintaxis Cron para ver cuando batchea
         catchup=False
         # esto sirve para si "tendría que haber iniciado antes", 
         # si es True, entonces corre todas las instancias 
         # que no ejecutó desde start_date hasta hoy
         # usualmente va False
         ) as dag:
     # acá van los operators

     create_table = PostgresOperator(
          #este es el operador de Postgres
          task_id="create_table",
          # task_id es el identificador unico que tiene la tarea
               # siempre tiene que haber una task_id para cada Operator
               # task_id debe ser único
               # es buena práctica mantener el mismo nombre 
               # para la task_id y el nombre de la variable
          postgres_conn_id="postgres",
          # este es el id de esa conexión
          # hay que definirla (véase )
          sql="""CREATE TABLE IF NOT EXISTS users(
               firstname TEXT NOT NULL
               lastname TEXT NOT NULL
               country TEXT NOT NULL
               username TEXT NOT NULL
               email TEXT NOT NULL
          )
          """
          # es muy importante el if not exists 
          # para que la task sea reproducible muchas veces. 
          )