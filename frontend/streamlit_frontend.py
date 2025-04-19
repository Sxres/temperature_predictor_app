import streamlit as st 
import requests
import pandas as pd 
import shap 
import plotly.express as px
st.set_page_config(page_title="Oshawa Temp Prediction", page_icon="🌡️", layout="centered")

col1, col2 = st.columns([16, 1], vertical_alignment="center", gap="small") 

st.sidebar.title("Sidebar Menu")
sidebar_tab = st.sidebar.pills("Tabs",("Home", "Plotly", "Dataset", "Shap"))


with col1:
    st.title('Oshawa Temperature Prediction')    
    st.subheader('Predict the temperature in Oshawa, Ontario, Canada')
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
Year = st.number_input('Year', min_value=2021)
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
    st.write(f"Predicted Temperature (°C): {prediction.get('Predicted temperature (°C)')}")


# sidebar menu stuff below 
if sidebar_tab == "Home":
    st.sidebar.write("Made By Dragos Sorescu")
    st.sidebar.write("Github: https://github.com/Sxres")
    st.sidebar.write("Uses an XGBoost regressor model to predict the temperature in my hometown")

if sidebar_tab == "Dataset":
    st.sidebar.write("Download the dataset I used to train the model") # get ready to change this to backend url like above ^ 
    data_response = requests.get("https://backend-150513265584.us-central1.run.app/Dataset")

    if data_response.status_code == 200:
        st.sidebar.download_button(
            label="Download Dataset",
            data=data_response.content,
            file_name="timedata.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.error("Failed to download the dataset.")

if sidebar_tab == "Shap":
    st.sidebar.write("SHAP vizulization to see how the model makes its predictions based on features (WIP has weird bug with value of features)")
    if st.sidebar.button("Show Shap Visualization"):
        if "Year" in locals() and "Month" in locals() and "Day" in locals() and "Time" in locals():
            shap_input = {
                'Year': int(Year),
                'Month': int(Month),
                'Day': int(Day),
                'Time': int(Time)
            }
            with st.spinner("Fetching SHAP values..."):
                shap_response = requests.post('https://backend-150513265584.us-central1.run.app/ShapValues', json=shap_input)
                if shap_response.status_code == 200:
                    shap_data = shap_response.json()
                    feature_names = shap_data["features"]

                    shap_df = pd.DataFrame(
                        {
                            "Feature": [feature["name"] for feature in feature_names],
                            "Value": [feature["value"] for feature in feature_names],
                            "SHAP Value": [feature["shap_value"] for feature in feature_names]
                        })
                    
                    base_value = shap_data["base_value"]
                    shap_values = shap_df["SHAP Value"].values

                    explaination = shap.Explanation(
                        base_values=base_value, 
                        values=shap_values, 
                        data=shap_df["Value"].values,
                        feature_names=shap_df["Feature"].values
                    )
                    
                    fig2 = shap.plots.waterfall(explaination, max_display=10, show=True)
                    st.sidebar.pyplot(fig2, use_container_width=True)



if sidebar_tab == "Plotly":
    st.sidebar.write("Plotly visuzalization to see how temperature changes over time")
    if st.sidebar.button("Show Plotly Visualization"):
        if "Year" in locals() and "Month" in locals() and "Day" in locals() and "Time" in locals():
            visualization_data = pd.DataFrame({
                'Year': [Year],
                'Month': [Month],
                'Day': [Day],
                'Time (UTC)': [Time]
            })

            dates = pd.date_range(
                start=f"{Year}-{Month}-{Day} {Time}:00:00", 
                periods=72, # 72 hours from prediction time 
                freq='h' # hourly frequency
                )
        
            temps = []

            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()

            for i, date in enumerate(dates):
                visualization_input_data = {
                    'Year': date.year,
                    'Month': date.month,
                    'Day': date.day,
                    "Time": date.hour
                }

                progress = int((i + 1) / len(dates) * 100)
                progress_bar.progress(progress, text=f"Fetching predictions... {progress}%")
                status_text.text(f"Processing hour {date.strftime('%Y-%m-%d %H:00')}")

           
                response2 = requests.post('https://backend-150513265584.us-central1.run.app/PredictFutureTemperature', json=visualization_input_data)

                if response2.status_code == 200:
                    prediction2 = response2.json()
                    temps.append(prediction2.get('Predicted temperature (°C)'))
                else:
                    st.error(f"Error: {response2.status_code} - {response2.text}")
                    temps.append(None)
            
            progress_bar.empty()
            status_text.text("Fetching predictions complete!")

            fig = px.line(
                x=dates, 
                y=temps, 
                title="Temperature Prediction Over Time",
                labels={"x": "Date", "y": "Predicted Temperature (°C)"}
            )
            
            st.sidebar.plotly_chart(fig, use_container_width=True)
        