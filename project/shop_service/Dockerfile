FROM python:3.7

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

CMD bash -c "python app.py db upgrade & python app.py runserver -p 5001 -h 0.0.0.0"

