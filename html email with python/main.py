import smtplib
import os
from email.mime.text import MIMEText


def send_email():
    sender = "1@1.1"
    password = '123'

    text = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=deice-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1 style="color: green;">Hello!!</h1>
        <span<u>How are you?</u></span>
    </body>
    </html>
    '''

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        with open("email_template.html") as file:
            template = file.read()
    except IOError:
        return "No template file"

    try:
        server.login(sender, password)
        msg = MIMEText(template, 'html')
        msg["From"] = sender
        msg["To"] = sender
        msg["Subject"] = "Happy BDayS"
        server.sendmail(sender, sender, msg.as_string())

        return "The message was sent!"
    except Exception as _ex:
        return f"{_ex}\n Check your login or password!"


def main():
    print(send_email())


if __name__ == 'main':
    main()
