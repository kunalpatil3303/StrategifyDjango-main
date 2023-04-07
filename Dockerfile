FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install git -y
RUN pip install --user -r requirements.txt
COPY . /code/
CMD python manage.py runserver 0.0.0.0:8000