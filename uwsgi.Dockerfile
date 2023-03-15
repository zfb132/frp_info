FROM alpine:latest
LABEL github user: zfxkj and zfb132

COPY . /frp

WORKDIR /frp

RUN apk add --update --no-cache py-pip gcc libc-dev linux-headers python3-dev; \
    pip install --no-cache-dir -U pip setuptools wheel;\
    pip install --no-cache-dir -r requirements.txt;

EXPOSE 6666

ENTRYPOINT ["sh", "/frp/entrypoint.sh"]