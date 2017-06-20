FROM python:2-onbuild

COPY . /usr/src/app

CMD ["python", "main.py"]

