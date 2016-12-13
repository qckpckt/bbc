FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y \
      python \
      python3 \
      python3-pip && \
    pip3 install -r requirements.txt


CMD bash
