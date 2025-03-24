ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /backend

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy model file and application code
COPY xgboost_regressor_time_model.json .
COPY . .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
