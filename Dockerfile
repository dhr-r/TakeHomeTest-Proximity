FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt /

RUN apk add --update gcc libc-dev fortify-headers linux-headers && rm -rf /var/cache/apk/*
    # Source: https://github.com/giampaolo/psutil/issues/664#issuecomment-460080035

RUN pip install -r /requirements.txt

COPY run.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run.sh

COPY app .

ENTRYPOINT ["run.sh"]