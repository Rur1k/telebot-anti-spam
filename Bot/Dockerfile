FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
COPY ./entrypoint.sh /usr/src/entrypoint.sh

RUN pip install -r requirements.txt
RUN ["chmod", "+x", "/usr/src/entrypoint.sh"]

COPY . .

ENTRYPOINT ["/usr/src/entrypoint.sh"]