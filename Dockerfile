FROM python:3.10.5-slim-buster

#RUN apt-get update && apt-get install -y \
#  binutils \
#  libproj-dev \
#  gdal-bin \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /progimage/app
COPY requirements.txt /progimage/app/
RUN pip install -r requirements.txt
COPY . /progimage/app/
RUN chmod +x /progimage/app/docker-entrypoint.sh

ENV PYTHONUNBUFFERED=1
EXPOSE 8080
ENTRYPOINT [ "/progimage/app/docker-entrypoint.sh" ]
