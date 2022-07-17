FROM python:3.8-slim

COPY . /blog_web

WORKDIR /blog_web

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    && apt upgrade -y \
    && apt-get install -y libc6-dev gcc mime-support dos2unix \
    && pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && apt-get remove -y gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /blog_web/wait-for-it.sh \
    && dos2unix wait-for-it.sh

ENV TZ = Asia/Shanghai

EXPOSE 8001

CMD python manage.py
