import smtplib
from email.mime.text import MIMEText
from setting import mail_password

def send(address, code):
	msg = MIMEText("Witaj. Twoj kod aktywacyjny : " + str(code))

	sender = "ibsi.anonymous@gmail.com"
	receiver = address
	password = mail_password

	msg['Subject'] = 'No-reply'
	msg['From'] = sender
	msg['To'] = receiver

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("ibsi.anonymous@gmail.com", password)
	server.sendmail(sender, receiver, msg.as_string())
	server.quit()
	
	print("Mail sent to " + address)

	return
