# Dockerfile

FROM python:3.12-slim

# Install system dependencies for llama-cpp-python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      libstdc++-12-dev \
      libgcc-12-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy rest of code
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
