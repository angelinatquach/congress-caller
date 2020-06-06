from twilio.rest import Client
from datetime import datetime
from boto.s3.connection import S3Connection
import time
import os

def callCongress():
	account_sid = S3Connection(os.environ['ACCOUNT_SID'])
	auth_token = S3Connection(os.environ['AUTH_TOKEN'])
	fromNumber = S3Connection(os.environ['TWILIO_PHONE'])
	#phoneNumbers = ['16503420300', '2022253531'];
	phoneNumbers = ['7147208654'];
	message = '''<Response><Say voice="Polly.Emma" language="en-US"> Hello, Congress woman Jackie Speier. My name is Angelina, and I am a
	California resident. It is very important to me that you pass the End Qualified Immunity Act. Qualified immunity means that victims of brutality or harassment 
	by law enforcement almost always get no relief in court and have no ability to hold offending officers accountable for their actions.
	That means the officers who commit the brutality and harassment that we are witnessing in the news today, and the governments that employ them,
	have little incentive to improve their practices, follow the law, and protect the people. Police are legally, politically, and culturally insulated
	from consequences for violating the rights of the people whom they have sworn to serve. That must change immediately so that these incidents of
	brutality stop happening.

	Ending qualified immunity would restore Americans' ability to obtain relief when police officers violate their constitutionally secured rights. It would
	also provide a powerful incentive for municipalities to restructure their law enforcement agencies and adopt policies and practices that curtail 
	abuses of power.

	I urge you to vote YES to pass the End Qualified Immunity Act. Thanks for your time and attention today! </Say></Response>''';

	client = Client(account_sid, auth_token)

	while True:
		for toNumber in phoneNumbers:
			print("Time of call: %s" % (datetime.now()))

			call = client.calls.create(
			                        status_callback_event = ['initiated', 'answered'],
			                        twiml = message,
			                        to = toNumber,
			                        from_ = fromNumber
			                    )
			print("Call SID: %s" % (call.sid))
			time.sleep(900)

def main():
	print('Initializing congress caller bot\n')
	callCongress()


if __name__ == '__main__':
    main()
