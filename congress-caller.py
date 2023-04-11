from twilio.rest import Client
from datetime import datetime
from itertools import chain
import names        # randomized names
import requests     # HTTP requests
import time         # sleep fxn
import os           # env vars

def call_congress_handler():
    # TODO: Get ProPublica and Twilio Api Key/Auth Tokens, save as env variables on Heroku 
    account_sid = os.environ["ACCOUNT_SID"]     # Twilio
    auth_token = os.environ["AUTH_TOKEN"]       # Twilio
    from_number = os.environ["TWILIO_PHONE"]     # Twilio

    #TODO: Replace {2} with your name if you'd like. Otherwise, it's randomized.
    message = '''<Response><Say voice="Polly.Emma" language="en-US"> Hello, Congress leader {0} {1}. My name is {2}, and I am a
    California resident. It is very important to me that you pass the Ending Qualified Immunity Act. Qualified immunity means that victims of brutality or harassment 
    by law enforcement almost always get no relief in court and have no ability to hold offending officers accountable for their actions.
    That means the officers who commit the brutality and harassment that we are witnessing in the news today, and the governments that employ them,
    have little incentive to improve their practices, follow the law, and protect the people. Police are legally, politically, and culturally insulated
    from consequences for violating the rights of the people whom they have sworn to serve. That must change immediately so that these incidents of
    brutality stop happening.

    Ending qualified immunity would restore Americans' ability to obtain relief when police officers violate their constitutionally secured rights. It would
    also provide a powerful incentive for municipalities to restructure their law enforcement agencies and adopt policies and practices that curtail 
    abuses of power.

    I urge you to vote YES to pass the Ending Qualified Immunity Act. Thanks for your time and attention today! </Say></Response>''';

    caller_client = Client(account_sid, auth_token)
    congress_members = get_congress_members()

    while True:
        for member in congress_members:
            member_first_name = member["first_name"]
            member_last_name = member["last_name"]   
            member_phone_number = member["phone"]
            
            # get random female name to act as caller agent
            caller_name = names.get_first_name(gender="female")

            print("[%s] Time to call %s %s" % (datetime.now(), member_first_name, member_last_name))

            call = caller_client.calls.create(
               status_callback_event = ["initiated", "answered"],
               twiml = message.format(member_first_name, member_last_name, caller_name),
               to = member_first_name,
               from_ = from_number
           )

            print("Call SID: %s" % (call.sid))

            # take a break every 20 minutes
            time.sleep(1200)            
                   

def get_congress_members():
    api_key = os.environ["API_KEY"]         # ProPublica

    senate_url = "https://api.propublica.org/congress/v1/116/senate/members.json"
    house_url = "https://api.propublica.org/congress/v1/116/house/members.json"
    headers = {"x-api-key": api_key}

    senate_members = requests.get(senate_url, headers=headers).json()["results"][0]["members"]
    house_members = requests.get(house_url, headers=headers).json()["results"][0]["members"]

    # TODO: Replace CA with your state
    senate = (member for member in senate_members if member["state"] == "CA")
    house = (member for member in house_members if member["state"] == "CA")
    return chain(senate, house)

def main():
    print("Initializing Congress caller bot\n")
    call_congress_handler()


if __name__ == '__main__':
    main()
