import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import json
import os

log = logging.getLogger('Email Service')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("email_service.log", "a"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class Email:
	def __init__(self):
		self.smtp_server = "smtp.gmail.com"
		self.sender_email = "social.network.mining.ua@gmail.com"
		self.password = os.environ.get('MAIL_PASSWORD', '')  # Ir buscar aos segredos do github
		self.port = 587
		self.context = ssl.create_default_context()

	def send_train_started(self, receiver_email, config_file="conf/train_started.json"):
		self.__send_email(receiver_email, self.__data_loader(config_file))

	def send_train_finished(self, receiver_email, config_file="conf/train_finished.json"):
		self.__send_email(receiver_email, self.__data_loader(config_file))

	def __data_loader(self, config_file):
		with open(config_file, 'r') as f:
			data = json.load(f)

		with open(data['html'], 'r') as f:  # Read html content
			data['html'] = f.read()

		return data

	def __send_email(self, receiver_email, data):
		log.info(f"Sending email to {receiver_email} with data: {data}")

		try:
			server = smtplib.SMTP(self.smtp_server, self.port)
			server.ehlo()
			server.starttls(context=self.context)  # Secure the connection
			server.ehlo()
			server.login(self.sender_email, self.password)

			message = MIMEMultipart("alternative")

			message["Subject"] = data['subject']
			message["From"] = self.sender_email
			message["To"] = receiver_email

			part1 = MIMEText(data['text'], "plain")
			part2 = MIMEText(data['html'], "html")

			message.attach(part1)
			message.attach(part2)

			server.sendmail(self.sender_email, receiver_email, message.as_string())

			log.info(f"Email sent with success")
		except Exception as e:
			log.error(e)
		finally:
			log.debug("Closing connection with smtp_server")
			server.quit()
