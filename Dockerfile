FROM python:3.9-slim-buster

WORKDIR /app

COPY main.py .
ENTRYPOINT ["python"]
CMD ["main.py"]