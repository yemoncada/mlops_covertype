from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from fastapi.responses import JSONResponse
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy as db
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

app = FastAPI()

def process_data(df):

    """
    Esta función se utiliza para procesar los datos antes de entrenar el modelo.
    La función normaliza los datos utilizando la clase StandardScaler y reemplaza 
    los valores faltantes por la media de cada variable.
    
    Parámetros:
    -----------
    df : Pandas DataFrame
        Los datos de entrenamiento.
    
    Retorno:
    -------
    df_norm : Pandas DataFrame
        Los datos de entrenamiento normalizados.
    """
    
    #Cambiamos los valores nan por la media de cada variable
    df.fillna(df.mean())

    df_norm = df.drop('Cover_Type', axis=1)
    y = df['Cover_Type']

    # Instanciar la clase StandardScaler
    scaler = StandardScaler()

    #normalizamos el dataframe
    X_norm = pd.DataFrame(scaler.fit_transform(df_norm), columns=df_norm.columns)

    #unimos la variable objetivo con el dataframe normalizado
    df_norm = pd.concat([X_norm, y], axis=1)
    
    return df_norm


def create_db(data):

    """
    Esta función se utiliza para crear y cargar los datos de entrenamiento desde una base de datos MySQL. 
    
    Parámetros:
    -----------
    data : str
        El nombre de la tabla que contiene los datos de entrenamiento.
        
    Retorno:
    -------
    df_db : Pandas DataFrame
        Los datos de entrenamiento cargados desde la base de datos.
        
    Excepciones:
    ------------
    HTTPException: si la tabla especificada no existe en la base de datos.
    """

    if data == 'covertype_data':

        connection_string = "mysql+pymysql://" + os.environ["USER_DB"] + ":" + os.environ["PASS_DB"] + "@" + os.environ["IP_SERVER"] + "/" + os.environ["NAME_DB"]
        query = 'SELECT Elevation, Slope, Horizontal_Distance_To_Hydrology, Vertical_Distance_To_Hydrology, Horizontal_Distance_To_Roadways, Hillshade_9am, Hillshade_Noon, Horizontal_Distance_To_Fire_Points, Cover_Type FROM '+data

        engine = create_engine(connection_string)

        # Create the database if it does not exist
        if not database_exists(engine.url):
            create_database(engine.url)

            print("[INFO] No existe la base de datos")

            # Re-create the engine to include the new database
            engine = create_engine(connection_string)

            with engine.connect() as conn:

                #impute the data
                df = pd.read_csv('data/covertype_train.csv')
                df = process_data(df)
                df.to_sql(con=engine, index_label='id', name='covertype_data', if_exists='replace')
                df_db = pd.read_sql_query(sql=text(query), con=conn)
        
        else:
            with engine.connect() as conn:
                if (db.inspect(conn).has_table('covertype_data')==True):
                    print("[INFO] Ya existe la base de datos")
                    df_db = pd.read_sql_query(sql=text(query), con=conn)
        
        return df_db

@app.get('/load_data')
def load_database():
    try:
        data = 'covertype_data'
        df_db = create_db(data)
        return JSONResponse(content=df_db.to_json(orient='records'))
  
    except:
        raise HTTPException(status_code=500, detail="Fallo Carga en la Base de Datos: "+data)


