FROM python:3.9-slim
WORKDIR /app
COPY generator.py .
RUN pip install pika
CMD ["python", "generator.py"]