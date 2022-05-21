FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /web
WORKDIR /web
COPY requirements.txt /web/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /mysite/

## THE LIFE SAVER
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait