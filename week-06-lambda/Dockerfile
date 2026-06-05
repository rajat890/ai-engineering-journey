FROM python:3.11-slim

WORKDIR /var/task

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    pip install awslambdaric --no-cache-dir

COPY . .

ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD ["main.handler"]