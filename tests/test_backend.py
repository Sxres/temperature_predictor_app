import pytest 
from backend.main import Weather, predict_future_temperature



@pytest.mark.asyncio
async def test_predict_future_temperature():
    weather = Weather(Year=2021, Month=1, Day=1, Time=0)
    response = await predict_future_temperature(weather)
    assert response == {"Predicted temperature (°C)": 0.7}
