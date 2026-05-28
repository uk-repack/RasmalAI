FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl tar && rm -rf /var/lib/apt/lists/*
RUN curl -L https://github.com/withcoral/coral/releases/download/v0.4.1/coral-x86_64-unknown-linux-gnu.tar.gz \
    | tar -xz && mv coral /usr/local/bin/coral && chmod +x /usr/local/bin/coral
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x start.sh
EXPOSE 8501
CMD ["bash", "start.sh"]
