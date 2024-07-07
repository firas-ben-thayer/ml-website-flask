FROM python:3.11.8

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]