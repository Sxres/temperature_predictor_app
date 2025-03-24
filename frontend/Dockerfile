ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /frontend

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run" ]
CMD [ "streamlit_frontend.py" ]
