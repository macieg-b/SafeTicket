from smsapi.client import SmsAPI
from smsapi.responses import ApiError
from setting import sms_user, sms_pass, sms_token

def send_sms(phone, token):
	api = SmsAPI()

	api.set_username(sms_user)
	api.set_password(sms_pass)
	api.auth_token = sms_token

	try:
		api.service('sms').action('send')

		api.set_content('Witaj, Twoj kod aktywacyjny: ' + str(token))
		api.set_to(phone)
		api.set_from('Info')

		result = api.execute()

		for r in result:
			print r.id, r.points, r.status

	except ApiError, e:
		print '%s - %s' % (e.code, e.message)
