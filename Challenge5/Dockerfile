FROM python:3.6.5-stretch
#FROM ubuntu:latest
MAINTAINER @mmisztal1980

#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential

#RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev

RUN pip install PILLOW numpy scikit-learn flask scipy

RUN mkdir /app
WORKDIR /app
COPY . .

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["main.py"]