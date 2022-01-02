# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

from_num = os.getenv('FROM_NUM')
to_num = os.getenv('TO_NUM')
message = client.messages \
                .create(
                    body="돈 많이 벌자!",
                    from_=from_num,
                    to=to_num
                )

print(message.sid)
