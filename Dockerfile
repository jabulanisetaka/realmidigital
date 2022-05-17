FROM python:3.9.6

ADD app.py .

RUN pip install requests datetime numpy smtplib ssl dotenv pandas

CMD [ "python", "./app.py" ]