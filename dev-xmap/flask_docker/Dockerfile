FROM python:3.10.1

LABEL MAINTAINER="WAIYU LAM <waiyu0616@gmail.com>"

ENV GROUP_ID=1000 \
  USER_ID=1000

WORKDIR /var/www/

ADD docker_code/ /var/www/

RUN pip install pip==22.0.4
RUN pip install gunicorn

RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 5001

CMD [ "gunicorn", "-w", "4", "--error-logfile", "-", "--bind", "0.0.0.0:5001", "app"]