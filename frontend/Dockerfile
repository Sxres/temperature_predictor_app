ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /frontend

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

EXPOSE 8501

ENTRYPOINT sh -c "streamlit run streamlit_frontend.py --server.port=${PORT:-8501} --server.address=0.0.0.0"
