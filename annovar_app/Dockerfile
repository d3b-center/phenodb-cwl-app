# ANNOVAR info at https://annovar.openbioinformatics.org/en/latest/

FROM ubuntu:20.04

RUN apt update && \
    DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" \
    apt install -y \
    perl \
    python3 \
    python3-pip \
    unzip \
    vim \
    wget

RUN pip3 install \
    pytz

WORKDIR /usr/src/phenodb_annovar
COPY main_annovar.py .
COPY utils.py .

# install annovar scripts
COPY annovar.latest.tar.gz .
RUN tar xvf annovar.latest.tar.gz
RUN rm annovar.latest.tar.gz