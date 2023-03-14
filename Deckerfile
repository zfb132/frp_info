FROM alpine:latest
MAINTAINER github user: zfxkj and zfb132
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk update
RUN apk add python3 python3-dev py3-pip
COPY . /frp
WORKDIR /frp
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
        ; \
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip; \
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt; \
        apk del .build-deps gcc libc-dev linux-headers;
RuN sed -i 's/home = ./#home = ./g' /frp/uwsgi_frp-info.ini

ENTRYPOINT [ "uwsgi", "--ini", "uwsgi_frp-info.ini" ]