FROM python:3.10.16-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update 
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y mc wrk

# setup the Java runtime in the path
#ENV JAVA_HOME=/opt/java 
#ENV PATH=${JAVA_HOME}/bin:$PATH
RUN apt-get install -y --no-install-recommends openjdk-17-jre

# Prints installed java version, just for checking
RUN java --version


RUN useradd -rm -d /home/learniken -s /bin/bash -g root -G sudo -u 1001 learniken
USER root
RUN chown -R learniken:root /home/learniken
WORKDIR /home/learniken
USER learniken

EXPOSE 8000
#EXPOSE 8888

COPY ./requirements.txt /home/learniken/requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
