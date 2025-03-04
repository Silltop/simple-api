FROM debian:stable-slim
ENV PIP_ROOT_USER_ACTION=ignore
COPY ./requirements.txt .
RUN apt-get update && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && python3 -m pip install --break-system-packages -r requirements.txt \
    && apt-get remove -y python3-pip \
    && rm /requirements.txt
RUN mkdir -p /opt/simple-api
COPY ./* /opt/simple-api/
WORKDIR /opt/simple-api
ENTRYPOINT ["python3", "main.py"]
