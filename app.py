from calendar import month
from unittest import result
import pandas as pd
from pendulum import today
import requests
import datetime
import numpy as np
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM
import calendar
import os
from dotenv import load_dotenv

load_dotenv()


# Get Data From API
api_url = os.getenv('API_URL')
api_url_not_send = os.getenv('API_URL_NOT_SEND')
d = requests.get(api_url_not_send).json()
r = requests.get(api_url)
x = r.json()


# To add email to receive
email_address = os.getenv('RECEIVE_EMAIL')

df = pd.DataFrame(x)
df2 = pd.DataFrame(d)
df['email'] = email_address
df['dateOfBirth'] = pd.to_datetime(df['dateOfBirth'], format='%Y-%m-%d %H:%M:%S')
df = df.replace(['1960-03-13T00:00:00'],'1960-05-17T00:00:00')
df['year'] = pd.DatetimeIndex(df['dateOfBirth']).year
df['month'] = pd.DatetimeIndex(df['dateOfBirth']).month
df['day'] = pd.DatetimeIndex(df['dateOfBirth']).day

# if d in df.values:
#     print('Yes')


result_dict = { item: True if item in df.values else False for item in d }
# condition = (df['dateOfBirth'].dt.year.mod(4).eq(0) 
#     & (df['dateOfBirth'].dt.year.mod(100).ne(0) | df['dateOfBirth'].dt.year.mod(400).eq(0))
# )

# df.assign(isleap=np.where(condition, 'TRUE', 'FALSE'))

df['employmentEndDate'] = df['employmentEndDate'].fillna(0)

# print(df)

# create func to send emails
def email_func(subject, birthday_receiver, name):
    # store email addresses for receiver , and the sender. Also store the sender email password
    receiver = birthday_receiver
    sender = os.getenv('SENDER')
    sender_password = os.getenv('SENDER_PWD')

    # create mimeMutlipart Object
    msg = MM()
    msg['Subject'] = subject+' '+str(name)+'!'

    # create hyml for msg
    HTML = """
        <html>
            <body>
                <h1>Happy Birthday !</h1>
                <img src="https://cdn.pixabay.com/photo/2013/07/12/19/02/happy-birthday-154242_960_720.png" alt="Happy birthdat Image" width="640" height="360"></img>
                <h2>
                    <p>
                    Hello <br>
                    I hope you have a wonderful day today <br><br>
                    From; <br>
                    Your Colleague 
                    </p>
                </h2>
            </body>
        </html>
    """

    # create a html MIMEText obj
    MTObj = MT(HTML,'html')

    # Attach the MIMETExt object into the message container
    msg.attach(MTObj)

    # create a secure connection with the server and send the email
    # create the secure socket layer (SSL) context object
    SSL_context = ssl.create_default_context()
    # create secure simple mail transfer protocol(smtp) connection
    server = smtplib.SMTP_SSL(host='smtp.gmail.com',port=465,context=SSL_context)
    # login email acc
    server.login(sender,sender_password)
    # send email
    server.sendmail(sender,receiver,msg.as_string())

# get current date
today = datetime.date.today() 
# get the current year
year = today.year 

# loop through the birthday list to send emails to friends whose birthdays are todays
for i in range(0, len(df)):

    # year
    # year = df['year'][i]
    # get the month
    month = df['month'][i]
    # get the day
    day = df['day'][i]

    # get name of person
    name = df['name'][i]
    # get the persons email address
    email = df['email'][i]
    # get the person birthdate
    birthdate = datetime.date(year , month , day)

    # if all(value == True for value in result_dict.values()):
    #     print('True')

    # if (df['employmentEndDate'] == 0).any():
    #     print(True)

    # if calendar.isleap(birthdate.year):
    #     print(True)
    # else:
    #     print(False)


    if (birthdate == today and all(value == True for value in result_dict.values()) and (df['employmentEndDate'] == 0).any()) or calendar.isleap(year):
        email_func('Happy Birthday', email, name)
        print('Sent Happy Birthday to ' + name)
    else:
        print('It is not '+ name+'s' + ' birthday')

