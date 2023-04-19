from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import sqlalchemy as db
from sklearn.preprocessing import StandardScaler
import pandas as pd

app = FastAPI()

def process_data(df):
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

    if data == 'covertype_data':

        # Configuración de la base de datos
        database_username = 'root'
        database_password = 'topicosIA'
        database_host = '10.43.102.112'
        database_port = '3306'
        database_name = 'topicosIA'

        # # Conexión a la base de datos
        connection_string = f"mysql+pymysql://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"
        engine = create_engine(connection_string)

        # engine = create_engine(
        #     "mysql+pymysql://" + os.environ["USER_DB"] + ":" + os.environ["PASS_DB"] + "@" + os.environ["IP_SERVER"] + "/" + os.environ["NAME_DB"])
        with engine.connect() as conn:
            query = 'SELECT Elevation, Slope, Horizontal_Distance_To_Hydrology, Vertical_Distance_To_Hydrology, Horizontal_Distance_To_Roadways, Hillshade_9am, Hillshade_Noon, Horizontal_Distance_To_Fire_Points, Cover_Type FROM '+data
            if (db.inspect(conn).has_table('covertype_data')==True):
                print("[INFO] Ya existe una tabla")
                df_db = pd.read_sql_query(sql=text(query), con=conn)
            else:
                print("[INFO] No existe una tabla")
                df = pd.read_csv('data/covertype_train.csv')
                df = process_data(df)
                df.to_sql(con=engine, index_label='id', name='covertype_data', if_exists='replace')
                df_db = pd.read_sql_query(sql=text(query), con=conn)
        return df_db
    else:
        raise HTTPException(status_code=500, detail="Unkown dataset: "+data)


@app.get('/train_model')
def load_database():
    try:
        data = 'covertype_data'
        df_db = create_db(data)
  
    except:
        raise HTTPException(status_code=500, detail="Unkown dataset: "+data)

