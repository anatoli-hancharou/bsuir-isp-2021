FROM python:3
WORKDIR /app
RUN pip3 install -U pygame --user
COPY . /app

CMD ["python3", "./solution.py"]
