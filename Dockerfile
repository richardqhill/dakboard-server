FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT gunicorn --bind :8000 --workers 1 --threads 2 --timeout 0 --chdir ./src server:app
CMD ["python", "src/server.py"]