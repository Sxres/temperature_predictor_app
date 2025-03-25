import streamlit as st 
import requests

# Create a row with two columns for the title and the button
col1, col2 = st.columns([8, 1], vertical_alignment="bottom")  # Adjust the column width ratio as needed

with col1:
    st.title('Temperature Prediction')  # Place the title in the first column

with col2:
    # Place the theme change button in the second column
    ms = st.session_state
    if "themes" not in ms: 
        ms.themes = {"current_theme": "light",
                        "refreshed": True,
                        
                        "light": {"theme.base": "dark",
                                "button_face": "🌜"},

                        "dark":  {"theme.base": "light",
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
    response = requests.post('https://backend-150513265584.us-central1.run.app/PredictFutureTemperature', json=input_data)
    prediction = response.json()
    st.write(f"Predicted Temperature: {prediction.get('Predicted temperature (°C)')}")