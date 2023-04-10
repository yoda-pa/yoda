FROM python:3.9-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
      libavcodec-extra \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .
