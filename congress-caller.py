from twilio.rest import Client
from datetime import datetime
from itertools import chain
import names
import requests
import time
import os

def callCongress():
    #TODO: Get ProPublica and Twilio Api Key/Auth Tokens, save as env variables
    api_key = os.environ['API_KEY']
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    fromNumber = os.environ['TWILIO_PHONE']

    senateUrl = "https://api.propublica.org/congress/v1/116/senate/members.json"
    houseUrl = "https://api.propublica.org/congress/v1/116/house/members.json"
    headers = {'x-api-key': api_key}

    #TODO: Replace {2} with your name if you'd like. Otherwise, it's randomized.
    message = '''<Response><Say voice="Polly.Emma" language="en-US"> Hello, Congress leader {0} {1}. My name is {2}, and I am a
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

    callerClient = Client(account_sid, auth_token)
    senateMembers = requests.get(senateUrl, headers=headers).json()["results"][0]["members"]
    houseMembers = requests.get(houseUrl, headers=headers).json()["results"][0]["members"]

    #TODO: Replace CA with your state
    senate = (member for member in senateMembers if member["state"] == "CA")
    house = (member for member in houseMembers if member["state"] == "CA")
    congress = chain(senate, house)

    while True:
        for member in congress:
            memberFirstName = member["first_name"]
            memberLastName = member["last_name"]   
            memberPhoneNumber = member["phone"]
            callerName = names.get_first_name(gender='female')

            print("[%s] Time to call %s %s" % (datetime.now(), memberFirstName, memberLastName))

            call = callerClient.calls.create(
                                   status_callback_event = ['initiated', 'answered'],
                                   twiml = message.format(memberFirstName, memberLastName, callerName),
                                   to = memberPhoneNumber,
                                   from_ = fromNumber
                               )

            print("Call SID: %s" % (call.sid))
            #take a break every 5 minutes
            #time.sleep(300)            

        #calls every 30 minutes
        time.sleep(1800)            


def main():
    print('Initializing Congress caller bot\n')
    callCongress()


if __name__ == '__main__':
    main()
