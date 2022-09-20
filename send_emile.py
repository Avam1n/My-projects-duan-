import smtplib
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(message_from_email):
    sender = config.email_address
    password = config.password_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg['Subject'] = "Логи бота!"

        msg.attach(MIMEText(message_from_email))

        with open('mylog.log', 'r') as fl:
            file = MIMEText(fl.read())


        file.add_header('content-disposition', 'attachment', filename='mylog.log')
        msg.attach(file)

        server.sendmail(sender, sender, msg.as_string())
        return "Сообщение отправлено!"
    except Exception as error:
        return f"{error}\nПроверь свой логин и пароль!"


def main(message_from_email):
    print(send_email(message_from_email))


if __name__ == '__main__':
    main()
