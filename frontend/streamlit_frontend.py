import streamlit as st 
import requests

st.title('Temperature Prediction')
# Theme changer I found on forums
ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "black",
                              "theme.primaryColor": "#c98bdb",
                              "theme.secondaryBackgroundColor": "#5591f5",
                              "theme.textColor": "white",
                              "theme.textColor": "white",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#5591f5",
                              "theme.secondaryBackgroundColor": "#82E1D7",
                              "theme.textColor": "#0a1464",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


col1, col2 = st.columns([5, 6])  # Adjust column widths as needed
with col1:
    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.button(btn_face, on_click=ChangeTheme)


if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()

# Get user input on month, day, and year
Year = st.number_input('Year', min_value=2011)
Month = st.number_input('Month', min_value=1, max_value=12)
Day = st.number_input('Day', min_value=1, max_value=31)
Time = st.number_input('Time (24 Hour)', min_value=0, max_value=23)



input_data = {
    'Year': Year,
    'Month': Month,
    'Day': Day,
    "Time": Time
    }

#when u click a button then it makes the post request to the backend
#and gets the response
if st.button('Predict Future Temperature'): 
    response = requests.post('http://backend:8080/PredictFutureTemperature', json=input_data)
    prediction = response.json()
    st.write(f"Predicted Temperature: {prediction.get('Predicted temperature (°C)')}")