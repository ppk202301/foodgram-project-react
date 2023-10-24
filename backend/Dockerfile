FROM python:3.9

WORKDIR /media
WORKDIR /static_backend
WORKDIR /data

ADD /data  /data

WORKDIR /app

COPY requirements.txt .
RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

WORKDIR /app/cookbook

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cookbook.wsgi"]

#CMD ["python", "manage.py", "runserver", "0:8000"]
