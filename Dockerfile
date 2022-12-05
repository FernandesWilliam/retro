FROM python:alpine AS development

WORKDIR /app

ENV GIT_PYTHON_REFRESH quiet

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apk update
RUN apk add git

COPY *.py .

CMD ["python3", "main.py", "https://github.com/audacity/audacity.git"]