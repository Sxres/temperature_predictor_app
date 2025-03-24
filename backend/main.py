from fastapi import FastAPI
from pydantic import BaseModel, Field
import xgboost as xgb
import pandas as pd

timemodel = xgb.Booster()
timemodel.load_model("xgboost_regressor_time_model.json")

app = FastAPI(docs_url="/TemperaturePrediction", title="Temperature Prediction API", description="API to predict the future temperature based on the year, month and day")

class Weather(BaseModel):
    Year: int = Field(ge=2011)
    Month: int = Field(ge=1, le=12)
    Day: int = Field(ge=1, le=31)
    Time: int = Field(ge=0, le=23)

@app.post("/PredictFutureTemperature")
async def predict_future_temperature(weather: Weather):
    future_date = pd.DataFrame({"Year": [weather.Year], "Month": [weather.Month], "Day": [weather.Day], "Time (UTC)": [weather.Time]})
    future_temp = timemodel.predict(xgb.DMatrix(future_date))
    return {"Predicted temperature (°C)": round(float(future_temp[0]), 1)} # could be bug 



#async def predict_future_temp(year, month, day):
   # future_date = pd.DataFrame({"Year": [year], "Month": [month], "Day": [day]})
   # future_temp = model.predict(xgb.DMatrix(future_date))
   # return future_temp[0]

#ask user to input year month and day to predict future temperature
#year = int(input("Enter year: "))
#month = int(input("Enter month: "))
#day = int(input("Enter day: "))
#future_temp = predict_future_temp(year, month, day)
#print(f"Predicted temperature on {year}-{month}-{day} is {round(future_temp)} degrees Celsius")