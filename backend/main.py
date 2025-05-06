from fastapi import FastAPI
from pydantic import BaseModel, Field
import xgboost as xgb
import pandas as pd
import os 
from fastapi.responses import FileResponse
import pickle 
import numpy as np 

timemodel = xgb.Booster()
timemodel.load_model("xgboost_regressor_time_modelv2.json")
with open("shap_data.pkl", "rb") as f:
    shap_data = pickle.load(f)

app = FastAPI(docs_url="/Docs", title="Temperature Prediction API", description="API to predict the future temperature based on the year, month and day")

class Temperature(BaseModel):
    Year: int = Field(ge=2021)
    Month: int = Field(ge=1, le=12)
    Day: int = Field(ge=1, le=31)
    Time: int = Field(ge=0, le=23)

@app.post("/PredictFutureTemperature")
async def predict_future_temperature(temperature: Temperature):
    future_date = pd.DataFrame({"Year": [temperature.Year], "Month": [temperature.Month], "Day": [temperature.Day], "Time (UTC)": [temperature.Time]})
    future_temp = timemodel.predict(xgb.DMatrix(future_date))
    return {"Predicted temperature (°C)": round(float(future_temp[0]), 1)} 

@app.get("/Dataset") # one error was using aiofiles in docker said it needed aiofiles so had to add that to requirements.txt
async def get_dataset():
    dataset_path = "timedata.csv"
    if not os.path.exists(dataset_path):
        return {"error": "Dataset not found"}
    return FileResponse(dataset_path, media_type='text/csv', filename="timedata.csv")


@app.post("/ShapValues")
async def shap_values(temperature: Temperature):
    if shap_data is None:
        return {"error": "SHAP data not found"}
    
    shap_input_data = pd.DataFrame({
        "Year": [temperature.Year],
        "Month": [temperature.Month],
        "Day": [temperature.Day],
        "Time (UTC)": [temperature.Time]
    })

    # this is straight vibe coded here 
    input_array = shap_input_data.values[0]

    distances = np.sum((shap_data["data"] - input_array) ** 2, axis=1)
    closest_index = np.argmin(distances)

    feature_names = shap_data["feature_names"]
    shap_values = shap_data["shap_values"][closest_index]
    base_value = float(shap_data["base_values"][closest_index])

    result = {
        "base_value": base_value,
        "features": [
            {
                "name": feature_names[i],
                "value": float(shap_data['data'][closest_index][i]),
                "shap_value": float(shap_values[i])
            } for i in range(len(feature_names))
        ],
        "prediction": base_value + float(np.sum(shap_values))
    }
    
    return result

