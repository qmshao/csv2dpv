FROM python:3.8-buster
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["gunicorn", "--workers=3", "-b", ":3800", "app:server"]