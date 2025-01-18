FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /usr/src/app/states/

CMD [ "python", "./main.py" ]