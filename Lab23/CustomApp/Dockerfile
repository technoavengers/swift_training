FROM python:3.10-slim

RUN pip install kubernetes

WORKDIR /app
COPY list_pod.py /app

CMD ["python", "list_pod.py"]