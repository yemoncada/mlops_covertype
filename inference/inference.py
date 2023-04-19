from fastapi import FastAPI, HTTPException
from joblib import load

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from sqlalchemy_utils import database_exists, create_database

import pandas as pd
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os

app = FastAPI()

database_username = 'root'
database_password = 'topicosIA'
database_host = '10.43.102.112'
database_port = '3306'
database_name = 'database_z'

# Conexión a la base de datos
connection_string = f"mysql+pymysql://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"
engine = create_engine(connection_string)

# Crear la base de datos si no existe
if not database_exists(engine.url):
    create_database(engine.url)

engine = create_engine(connection_string)

# Definición de la sesión
SessionLocal = sessionmaker(bind=engine)
# Definición de la clase base para las clases de la base de datos
Base = declarative_base()

# Definición de la clase para la tabla de covertype
class CoverType(Base):
    __tablename__ = "covertype_data_inference"
    id = Column(Integer, primary_key=True, index=True)
    Elevation = Column(Integer, index=True)
    Slope = Column(Integer, index=True)
    Horizontal_Distance_To_Hydrology = Column(Integer)
    Vertical_Distance_To_Hydrology = Column(Integer)
    Horizontal_Distance_To_Roadways = Column(Integer)
    Hillshade_9am = Column(Integer)
    Hillshade_Noon = Column(Integer)
    Horizontal_Distance_To_Fire_Points = Column(Integer)
    Cover_Type = Column(Integer)

# Creación de la tabla de penguins en la base de datos
Base.metadata.create_all(bind=engine)

# Definir el esquema de entrada de datos
class CoverTypeCreate(BaseModel):
    Elevation: int
    Slope: int
    Horizontal_Distance_To_Hydrology: int
    Vertical_Distance_To_Hydrology: int
    Horizontal_Distance_To_Roadways: int
    Hillshade_9am: int
    Hillshade_Noon: int
    Horizontal_Distance_To_Fire_Points: int

@app.delete("/delete_data_inference/")
def delete_penguins():
    db = SessionLocal()
    db.query(CoverType).delete()
    db.commit()
    return {"message": "All inference data have been deleted."}


@app.get("/cover_type_data")
async def get_all_cover_type_data():
    db = SessionLocal()
    results = db.query(CoverType).all()

    cover_type_data = []
    for result in results:
        data = {
            "Elevation": result.Elevation,
            "Slope": result.Slope,
            "Horizontal_Distance_To_Hydrology": result.Horizontal_Distance_To_Hydrology,
            "Vertical_Distance_To_Hydrology": result.Vertical_Distance_To_Hydrology,
            "Horizontal_Distance_To_Roadways": result.Horizontal_Distance_To_Roadways,
            "Hillshade_9am": result.Hillshade_9am,
            "Hillshade_Noon": result.Hillshade_Noon,
            "Horizontal_Distance_To_Fire_Points": result.Horizontal_Distance_To_Fire_Points,
            "Cover_Type": result.Cover_Type
            }
        cover_type_data.append(data)
    return {"cover_type_data": cover_type_data}


# Crear una ruta para la inferencia
@app.post("/predict_model")
async def predict_model(cover: CoverTypeCreate, model:str='covertype_data'):

    model_path = '/train/models/'+model+'_model.joblib'
    #model_path = '/home/estudiante/mlops_covertype/train/models/covertype_data_model.joblib'

    if not os.path.isfile(model_path):
        raise HTTPException(status_code=500, detail="Unkown model: "+ model+" Try to train model first.")

    model_loaded = load(model_path)
    prediction = model_loaded.predict(pd.DataFrame([cover.dict()]))[0]

    db = SessionLocal()

    db_inference = CoverType(

        Elevation = cover.Elevation,
        Slope =  cover.Slope,
        Horizontal_Distance_To_Hydrology =  cover.Horizontal_Distance_To_Hydrology ,
        Vertical_Distance_To_Hydrology =  cover.Vertical_Distance_To_Hydrology,
        Horizontal_Distance_To_Roadways =  cover.Horizontal_Distance_To_Roadways,
        Hillshade_9am =  cover.Hillshade_9am,
        Hillshade_Noon =  cover.Hillshade_Noon,
        Horizontal_Distance_To_Fire_Points =  cover.Horizontal_Distance_To_Fire_Points,
        Cover_Type = int(prediction)

    )

    db.add(db_inference)
    db.commit()
    db.refresh(db_inference)

    return JSONResponse(content={"prediction": int(prediction)})