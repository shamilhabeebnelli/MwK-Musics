FROM python:3.8-slim-buster
WORKDIR /app 
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y 
COPY . . 

CMD python3 main.py
