FROM python:3.9-slim
WORKDIR /app
COPY reporter.py .
RUN pip install pika
CMD ["python", "reporter.py"]
