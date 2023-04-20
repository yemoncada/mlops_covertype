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

# Create a connection string using the database credentials
connection_string = "mysql+pymysql://" + os.environ["USER_DB"] + ":" + os.environ["PASS_DB"] + "@" + os.environ["IP_SERVER"] + "/" + os.environ["NAME_DB"]

# Create an engine using the connection string
engine = create_engine(connection_string)

# Create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)

# Re-create the engine to include the new database
engine = create_engine(connection_string)

# Define the session factory for the database
SessionLocal = sessionmaker(bind=engine)

# Define the base class for the database tables
Base = declarative_base()

class CoverType(Base):
    """
    SQLAlchemy ORM class for the covertype_data_inference table in the database.

    """
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

# Create the covertype_data_inference table in the database
Base.metadata.create_all(bind=engine)

class CoverTypeCreate(BaseModel):
    """
    Pydantic model for the input data for cover type prediction.

    """
    Elevation: int
    Slope: int
    Horizontal_Distance_To_Hydrology: int
    Vertical_Distance_To_Hydrology: int
    Horizontal_Distance_To_Roadways: int
    Hillshade_9am: int
    Hillshade_Noon: int
    Horizontal_Distance_To_Fire_Points: int


@app.delete("/delete_data_inference/")
def delete_cover_type_data():
    """
    Deletes all cover type inference data from the database.

    """
    db = SessionLocal()
    db.query(CoverType).delete()
    db.commit()
    return {"message": "All inference data have been deleted."}


@app.get("/cover_type_data")
async def get_cover_type_data():
    """
    Retrieves all cover type inference data from the database.

    """
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

@app.post("/predict_model")
async def predict_model(cover: CoverTypeCreate, model:str='covertype_data'):
    """
    Performs cover type prediction based on the input data and the specified model.
    Saves the input data and the prediction result to the database.

    Args:
        cover (CoverTypeCreate): The input data for cover type prediction.
        model (str, optional): The name of the trained model to use for prediction. Defaults to 'covertype_data'.

    Returns:
        JSONResponse: A JSON response containing the cover type prediction.

    Raises:
        HTTPException: If the specified model is not found.

    """
    model_path = '/train/models/'+model+'_model.joblib'
    #model_path = '/home/estudiante/mlops_covertype/train/models/covertype_data_model.joblib'

    if not os.path.isfile(model_path):
        raise HTTPException(status_code=500, detail="Unkown model: "+ model+" Try to train model first.")

    # Load the trained model and perform the prediction on the input data
    model_loaded = load(model_path)
    prediction = model_loaded.predict(pd.DataFrame([cover.dict()]))[0]

    # Add the input data and prediction result to the database
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

    # Return the cover type prediction as a JSON response
    return JSONResponse(content={"prediction": int(prediction)})