FROM python:3.10-slim

MAINTAINER Uuganbayar <uuganbayar@zerotech>

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pos-backend.wsgi:application"]

