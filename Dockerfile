FROM python:alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev python3-dev
    
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psutil apache_log_parser

CMD ["make", "run"]
