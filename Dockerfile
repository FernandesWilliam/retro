FROM python:alpine AS development

WORKDIR /app

ENV GIT_PYTHON_REFRESH quiet

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apk update
RUN apk add git
RUN apk add graphviz

COPY config config

COPY *.py .

COPY src src

CMD ["python3", "main.py", "https://github.com/audacity/audacity.git", "https://github.com/miguelmemm16/juiceshop.git"]