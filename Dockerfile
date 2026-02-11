FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

EXPOSE 7860
EXPOSE 8000

CMD ["python", "-m", "app.ui"]