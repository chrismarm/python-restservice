FROM python:3
MAINTAINER Christian Marmolejo "chrismarm.development@gmail.com"
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
CMD python3 service.py