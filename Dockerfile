# See https://confluence.viator.com/pages/viewpage.action?pageId=14169226
# Build as
# 	docker build -t viatorinc/locomail .
# Run as
#	docker run --rm --name loco-mail -it -p -p 15000:10000 -p 5000:5000 loco-mail
#
# Push as
#    docker push viatorinc/locomail


FROM debian:jessie
RUN apt-get update
RUN apt-get -y --fix-missing install python3 telnet wget sqlite3

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN /usr/bin/python3 get-pip.py

RUN pip3 install requests flask gevent

RUN mkdir -p /opt/locomail
COPY src/ /opt/locomail

EXPOSE 5000
EXPOSE 25

COPY externalFiles/entryPoint.sh /
ENTRYPOINT "/entryPoint.sh"
