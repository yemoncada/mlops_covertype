from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import sqlalchemy as db
from sqlalchemy import create_engine, text

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import pandas as pd

import joblib
import os

app = FastAPI()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import sqlalchemy as db
from sqlalchemy import create_engine, text

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import pandas as pd
import joblib
import os

app = FastAPI()

@app.get("/train/")
def train_model():
    """
    Endpoint to train a RandomForest classification model and save its weights.
    
    Returns:
    --------
    JSONResponse:
        JSON object containing the accuracy of the trained model and a message.
    """

    # Configuration of the database
    database_username = 'root'
    database_password = 'topicosIA'
    database_host = '10.43.102.112'
    database_port = '3306'
    database_name = 'topicosIA'

    # Connection to the database
    connection_string = f"mysql+pymysql://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"
    engine = create_engine(connection_string)

    # Read data from the database table 'covertype_data'
    with engine.connect() as conn:
        data = 'covertype_data'
        query = 'SELECT Elevation, Slope, Horizontal_Distance_To_Hydrology, Vertical_Distance_To_Hydrology, Horizontal_Distance_To_Roadways, Hillshade_9am, Hillshade_Noon, Horizontal_Distance_To_Fire_Points, Cover_Type FROM '+data
        if (db.inspect(conn).has_table('covertype_data')==True):
            print("[INFO] Connecting to table X")
            df = pd.read_sql_query(sql=text(query), con=conn)

    # Separate the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df.drop('Cover_Type', axis=1), df['Cover_Type'], test_size=0.2, random_state=42)

    # Train the RandomForest model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model's performance on the test set
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)       

    # Save the model weights to the 'models' directory
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(model, 'models/'+data+'_model.joblib')

    # Return the model's accuracy as a JSON response
    return JSONResponse(content={"accuracy": acc, "message": "The model has been trained."})