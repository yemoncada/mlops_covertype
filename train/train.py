from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import sqlalchemy as db
from sqlalchemy import create_engine, text

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import pandas as pd

import joblib
import os

app = FastAPI()

# Endpoint para entrenar un modelo de clasificación y guardar los pesos
@app.post("/train/")
def train_model():
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
        data = 'covertype_data'
        query = 'SELECT Elevation, Slope, Horizontal_Distance_To_Hydrology, Vertical_Distance_To_Hydrology, Horizontal_Distance_To_Roadways, Hillshade_9am, Hillshade_Noon, Horizontal_Distance_To_Fire_Points, Cover_Type FROM '+data
        if (db.inspect(conn).has_table('covertype_data')==True):
            print("[INFO] Conectandose a la tabla X")
            df = pd.read_sql_query(sql=text(query), con=conn)

    # Separar los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df.drop('Cover_Type', axis=1), df['Cover_Type'], test_size=0.2, random_state=42)

    # Entrenar el modelo de RandomForest
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluar el rendimiento del modelo en el conjunto de prueba
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)       

    # Guardar los pesos del modelo en la carpeta 'model_weights'
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(model, 'models/'+data+'_model.joblib')

    # Retornar la precisión del modelo como una respuesta JSON
    return JSONResponse(content={"accuracy": acc, "message": "El modelo ha sido entrenado"})