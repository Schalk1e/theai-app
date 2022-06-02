FROM python:3

EXPOSE ${PORT}

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/app
RUN mkdir ${APP_HOME}
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ${APP_HOME}
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${APP_HOME}

RUN chown -R app:app ${APP_HOME}

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app --reload
