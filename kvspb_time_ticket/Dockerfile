# pull the official base image
FROM python:3.12.0-alpine


RUN apk add --update bash
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 8000

RUN ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]

