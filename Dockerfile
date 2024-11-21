FROM python:3.11.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
ENV TZ=UTC

WORKDIR  /app
RUN pip install --upgrade pip setuptools

ADD requirements.txt  requirements.txt

RUN python3 -m venv venv

RUN  ./venv/bin/pip3 install --upgrade pip && \
    ./venv/bin/pip3 install -r /app/requirements.txt && \ 
    pip3 install gunicorn gevent && \  
    pip3 cache purge



COPY .  /app

COPY ./bin/nginx.conf /etc/nginx/nginx.conf


RUN chmod +x  /app

RUN chmod +x /app/bin/docker_start.sh

ENTRYPOINT ["bash","/app/bin/docker_start.sh"]
