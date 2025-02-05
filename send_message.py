import smtplib
from email.message import EmailMessage
import requests


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "amous0389@gmail.com"
    msg["from"] = user
    password = "hqhjqkfoifdmmhyk"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    return


def send_otp(phoneNo):
    msg = "Emergency - Walking Stick!!\n\nThe user has fired up the emergency contact protocol!\n\nTeam IPD"
    baseUrl = "https://www.fast2sms.com/dev/bulkV2?"
    auth = "authorization=2a7Azhwnyd8vU1veSRdK09fmsswhKRzM2F5YZo0ay2JBvR4fWlxBFyHGuVVP"
    route = "&route=v3"
    senderId = "&sender_id=FastSM"
    number = "&numbers=" + str(phoneNo)
    message = "&message=" + msg
    url = baseUrl + auth + route + senderId + number + message
    response = requests.get(url)
    return response.json()
