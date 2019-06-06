import smtplib

from email.mime.text import MIMEText
from uuid import uuid4

def send_email_to_one_recipient(server, account, password, address, subject, body):
    smtp_connection = smtplib.SMTP(server)
    smtp_connection.ehlo()
    smtp_connection.starttls()
    smtp_connection.login(account, password)
    message = MIMEText(body)
    message.set_charset('utf-8')
    message.add_header('Message-ID', '<{uuid}@{domain}>'.format(uuid=uuid4(), domain=account.split('@')[-1]))
    message.add_header('From', account)
    message.add_header('To', address)
    message.add_header('Subject', subject)
    smtp_connection.sendmail(account, address, message.as_string())
    smtp_connection.quit()
