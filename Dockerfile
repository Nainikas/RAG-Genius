FROM python:3.10-slim
WORKDIR /app

# system deps (Linux); on Windows Docker uses Linux base
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
# Use the following command to build the Docker image:
# docker build -t streamlit-app .