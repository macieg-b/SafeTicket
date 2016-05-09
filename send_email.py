import smtplib
from email.mime.text import MIMEText
from setting import mail_password

def send(address, code):
	print("Came into mail")
	msg = MIMEText("Witaj. Twoj kod aktywacyjny : " + str(code))

	print(msg)
	print(address)
	print(code)
	
	sender = "ibsi.anonymous@gmail.com"
	receiver = address
	password = mail_password

	print(password)

	msg['Subject'] = 'No-reply'
	msg['From'] = sender
	msg['To'] = receiver

	print("X")

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("ibsi.anonymous@gmail.com", password)
	server.sendmail(sender, receiver, msg.as_string())
	server.quit()
	
	return
