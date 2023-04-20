import json
import os
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Conexión a la base de datos
connection_string = "mysql+pymysql://" + os.environ["USER_DB"] + ":" + os.environ["PASS_DB"] + "@" + os.environ["IP_SERVER"] + "/" + os.environ["NAME_DB"]
engine = create_engine(connection_string)

if not database_exists(engine.url):
    print("[INFO] La Base de Datos no Existe")

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

@app.get("/save_inferences")
async def save_log_inference():
    """
    This function retrieves all the inference data saved in the 'covertype_data_inference' table
    and saves it in a JSON file at the path '/database/data/cover_type_inferences.json'.
    """
    db = SessionLocal()
    results = db.query(CoverType).all()

    # Crear una lista vacía para almacenar los datos de cada registro
    cover_data = []

    # Iterar sobre los resultados y agregarlos a la lista
    for result in results:
        cover_data.append({
            "id": result.id,
            "Elevation": result.Elevation,
            "Slope": result.Slope,
            "Horizontal_Distance_To_Hydrology": result.Horizontal_Distance_To_Hydrology,
            "Vertical_Distance_To_Hydrology": result.Vertical_Distance_To_Hydrology,
            "Horizontal_Distance_To_Roadways": result.Horizontal_Distance_To_Roadways,
            "Hillshade_9am": result.Hillshade_9am,
            "Hillshade_Noon": result.Hillshade_Noon,
            "Horizontal_Distance_To_Fire_Points": result.Horizontal_Distance_To_Fire_Points,
            "Cover_Type": result.Cover_Type
        })
        
    # Convertir la lista de registros en formato JSON
    cover_data_json = json.dumps(cover_data)

    # Guardar los registros en un archivo
    json_path = "/database/data/cover_type_inferences.json"
    #json_path = "cover_data.json"
    with open(json_path, "w") as f:
        f.write(cover_data_json)

    return {"cover_type_data": cover_data}