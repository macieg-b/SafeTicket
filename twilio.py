	# Your Account Sid and Auth Token from twilio.com/user/account
	account_sid = "AC122b62b4982017c9239580ad0bc21e2c"
	auth_token  = "6e00535423c7711d86543125d4386fb1"
	client = TwilioRestClient(account_sid, auth_token)
	message = client.messages.create(body="\nMB - The best programmer ever",
	    to="+48691669003",    # Replace with your phone number
	    from_="+48732483582") # Replace with your Twilio number
	print message.sid
