FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY steamstatus/ steamstatus/

EXPOSE 5000

ENV FLASK_APP=steamstatus
# ENV FLASK_ENV=development
ARG API_KEY=xxx

RUN flask init-db
CMD ["flask", "run", "--host=0.0.0.0"]
