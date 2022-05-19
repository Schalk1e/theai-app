FROM python:3

EXPOSE ${PORT}

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app --reload