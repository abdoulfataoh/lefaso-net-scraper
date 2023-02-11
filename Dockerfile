# Coding: utf-8

# [Base image]
FROM python:3.10

# [Meta data]
LABEL name="lefaso-net-scraper"
LABEL authors="abdoulfataoh"

# [Wordir]
WORKDIR /src

# [Env variables]
ENV BOT_API_TOKEN=${BOT_API_TOKEN}

# [Source code]
ADD ./ /src

# [Install poetry]
RUN pip install -U pip
RUN pip install -r requirements.txt


RUN python3 start.py

ADD ./assets/dataset/* /src/
