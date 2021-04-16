FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin

WORKDIR /app

# Copy requirement file
COPY requirements.txt ./

COPY entrypoint.sh ./

# Install all required dependencies

RUN apt-get update && \
    apt-get install -y software-properties-common tzdata && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y && \
    apt-get install -y python3.7 python3-pip python3.7-distutils && \
    ln -s /usr/bin/python3.7 /usr/bin/python && \
    python -m pip install rq when-changed && \
    python -m pip install -r requirements.txt

CMD ["bash", "entrypoint.sh"]