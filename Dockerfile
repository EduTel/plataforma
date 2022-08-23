FROM python:3.9.1-alpine3.13
LABEL version="1.0"
LABEL description="plataforma Django"
LABEL maintainer = ["eduardo_jonathan@outlook.com"]
WORKDIR /app
EXPOSE 8000/tcp

COPY requirements.txt /app
COPY db.sqlite3 /app
COPY plataforma/ /app/plataforma/
COPY manage.py /app
RUN pip3  --no-cache-dir --use-feature=2020-resolver install -r /app/requirements.txt  --no-deps
CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]