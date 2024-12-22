FROM alpine:latest
LABEL github user: zfb132

COPY . /frp

WORKDIR /frp

RUN apk add --update --no-cache py-pip; \
    sed -i '/^uwsgi/d' requirements.txt; \
    sed -i 's/6665/6666/g' runserver.py; \
    pip install --break-system-packages --no-cache-dir -r requirements.txt; \
    mkdir -p /frp/log; chmod 777 /frp/log;

EXPOSE 6666

ENTRYPOINT ["python3", "runserver.py"]