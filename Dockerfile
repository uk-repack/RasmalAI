FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl tar && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/withcoral/coral/releases/download/v0.4.1/coral-x86_64-unknown-linux-gnu.tar.gz \
    | tar -xz && mv coral /usr/local/bin/coral && chmod +x /usr/local/bin/coral

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV SLACK_TOKEN=${SLACK_TOKEN}
ENV GROQ_API_KEY=${GROQ_API_KEY}

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
