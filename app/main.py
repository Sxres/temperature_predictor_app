from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel, Field
import xgboost as xgb
import pandas as pd

model = xgb.Booster()
model.load_model("xgboost_regressor_model.json")

app = FastAPI()

class Weather(BaseModel):
    Year: int = Field(ge=2019)
    Month: int = Field(ge=1, le=12)
    Day: int = Field(ge=1, le=31)

@app.post("/PredictFutureTemperature")
async def predict_future_temperature(weather: Annotated[Weather, Query(description="Enter the year, month and day to predict the temperature for", example={"Year": 2022, "Month": 1, "Day": 1})]):
    future_date = pd.DataFrame({"Year": [weather.Year], "Month": [weather.Month], "Day": [weather.Day]})
    future_temp = model.predict(xgb.DMatrix(future_date))
    return {"Predicted temperature": round(future_temp[0])}


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