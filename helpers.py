from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
import os
import re


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'SHHHHHHHHHHh'
auth_token = 'SHHHHHHHHHHHHHHHhhh'
client = Client(account_sid, auth_token)

def next_sunday(date_a):
    while date_a.weekday() != 6:
        date_a = date_a.shift(days=1)
    return date_a.format('YYYY-MM-DD')

def parse_number(message):
  # Check for at least two numbers
  countryCode = '+1'
  if bool(re.search(r'\d{2}', message)):
    # Replace %2B with + and assign to variable because strings are immutable in Python
    number = message.replace('%2B', '+', 1)
    # Clean up number
    cleanedUpNumber = re.sub(r'([-() ])', "", number)
    # Check if it's less than 10 digits
    if len(cleanedUpNumber) < 10:
      return False
    elif len(cleanedUpNumber) == 10:
      return countryCode + cleanedUpNumber
    elif len(cleanedUpNumber) > 10:
      # Check for countryCode
      countryCode = '+1'
      if (cleanedUpNumber[0:2] == countryCode):
        return cleanedUpNumber
    else:
      return False
  else:
    return False

def lookup_number(number_to_lookup):
  name = client.lookups.phone_numbers(number_to_lookup).fetch(type='caller-name')
  if name:
    return (name.caller_name)['caller_name']
  else:
    return False

def send_message(message, to_number, **kwds):
  client.messages.create(
        to=to_number,
        from_="SHHHHHHHHHHHHhhh",
        body=message,
        **kwds
)

def number_lookup(number_to_lookup):
  name = client.lookups.phone_numbers(number_to_lookup).fetch(type='caller-name')
  if name:
    return (name.caller_name)['caller_name']
  else:
    return False
