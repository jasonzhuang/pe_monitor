import smtplib
from email.mime.text import MIMEText
import requests

def send_email(subject, content, email_config):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = email_config['sender']
    msg['To'] = email_config['receiver']

    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['sender'], email_config['password'])
        server.send_message(msg)

def send_wechat(content, sckey):
    requests.post(f"https://sctapi.ftqq.com/{sckey}.send", data={
        "title": "低估提醒",
        "desp": content
    })