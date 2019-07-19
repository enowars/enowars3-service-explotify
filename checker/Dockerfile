FROM python:3.6.8-stretch
LABEL maintainer="ENOFLAG <mail@enoflag.de>"

# Install python3 and uswgi
RUN apt-get update
RUN apt-get install -y nginx git espeak-ng ffmpeg curl

# use python3
RUN pip3 install uwsgi

# copy our files in.
WORKDIR /checker
COPY ./requirements.txt /checker/requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir distopianM
RUN curl -L -o distopianM/distopian.mp3 https://appchama.com/distopian.mp3

ENTRYPOINT [ "uwsgi", "--uid", "uwsgi", \
               "--socket", "[::]:3031", \
               "--protocol", "http","--http-keepalive", \
               "--ini", "/checker/uwsgi.ini" ]