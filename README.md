# congress-caller
This is a simple python application intended to call your local Congress representations and appeal for the End Qualified Immunity Act.

##Dependencies
1. Twilio's Programmable Voice API - you must register for a Twilio account (not a trial one).
   - feel free to use TWILIOQUEST as a promo code for $50 in credit. Before sure to monitor your call usage to not rack up a bill after your credit runs out.
   - the phone number that Twilio provides you will cost you $1/month to use.
2. ProPublica Congress API - you must register for a free ProPublica API Key.
3. Heroku - register for free

## Heroku
This application can be run locally. However, it was written and intended to be used with Heroku (free tier). To avoid using any add-ons and stick to free dynos, I used Heroku's worker functionality.

After cloning the repo and enabling Heroku on your local repo, you can enable to worker with the command "heroku scale worker=1".

*I am not liable or responsible for whatever infractions or reprecussions you may incur from using this application to contact your congress members. Enjoy!
