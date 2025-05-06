ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /backend

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy model file and application code
COPY xgboost_regressor_time_modelv2.json .

COPY timedata.csv .
#^ copy my dataset that I used to train the model 
COPY shap_data.pkl . 

COPY . . 
#^ blanket copy of everything in the current directory

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
