from __future__ import print_function
from helpers import *
from constants import *
from gsheet import logging_no_serve, find_next_week
import arrow

def no_response():
    message = """ I guess you are busy for the coming sunday. No worries!
    I will add you to the service the week after! Thank you!"""
    return message

def creepy_response(number):
    message = ''
    # Check for number
    if number:
      # Find out who the number belongs to
      callerName = lookup_number(number)
      if callerName:
        message = 'This number appears to be registered to: ' + callerName
      else:
        message = 'Aw. Sorry to let you down but we can\'t associate a name with that number.'
    else:
      message = 'Hello. Usherbot is confused by your statement. Have a pika!'
    return message

def get_name(number):
    for name, num in PHONE_NUMBER_MAP.items():
        if num == number:
            return name

def switch_peeps(no_person, is_prod=False):
    print(f"{no_person} can no serve :( ")
    cant_serve = logging_no_serve(no_person)
    return find_next_week(cant_serve, no_person, is_prod=is_prod)

def zpj_msg(num):
    msg = f""" Jason Wang is the Zone Pastor of Ignite (the Young Adult and College Congregation) at River of Life Christian Church. He has attended the church since his high school days back in 2000 and has served the church in various positions since.

Jason was born and raised in the Bay Area where he attended James Logan High School in Union City, then went to UC Davis where he graduated with a degree in Managerial Economics and Chinese, and from there went to Cal Poly, San Luis Obispo where he graduated with a Master's in Taxation. Prior to stepping into his new role at Ignite, Jason was a Payroll Manager at Ultimate Software working with Google Payroll. Before that, he worked at Accenture and PricewaterhouseCoopers as a Certified Public Accountant.

Currently, he lives in Fremont and is attending Western Seminary where he is pursuing his Master's in Divinity. In his spare time, Jason enjoys growing the church, playing basketball, drinking tea, keeping up with current events, and watching sports talk shows.
    """
    send_message(msg, num, media_url='https://static1.squarespace.com/static/5524619ae4b0df69c584c8cb/t/5bd0aa31eef1a11c4c75dc64/1540401725628/Jason+Headshot?format=1000w')

def troll_msg(num):
    msg= f"""
    hi, y u TROLOLOLOLOLOLOLLLLLL
    """
    print(msg)
    troll_url = 'https://media.giphy.com/media/17RaL7HOgI1CE/giphy.gif'
    send_message(msg, num, media_url = 'https://media.giphy.com/media/17RaL7HOgI1CE/giphy.gif')

def switcheroo_msg(name, num, is_prod=False):
    msg = f""" hi {name},
    you will be helping out!
    Please reply no if you can't!
    Thank you!
    """
    print(msg)
    if is_prod:
        send_message(msg, num)


def lambda_handler(event, context):
    # Obtain the number from the incoming text
    info = parse_number(event['Body'])
    to_number = '+' + event['From'][3:]
    phone_m = event['Body']
    list_body = [x.lower() for x in phone_m.split('+')]
    if 'zpj' in list_body:
        zpj_msg(to_number)
        return
    if 'troll' in list_body:
        troll_msg(to_number)
        return
    if 'no' in list_body:
        if to_number == 'SHHHHHHHHHHHHHhhh':
            print("just master playing")
            message = no_response()
            no_person = list_body[0].capitalize()
            switcheroo, switch_num, is_troll = switch_peeps(no_person)
            if is_troll:
                troll_msg(to_number)
                return
            else:
                switcheroo_msg(switcheroo, switch_num)
        else:
            message = no_response()
            no_person = get_name(to_number)
            # this needs prod on to truly switch
            switcheroo, switch_num, is_troll = switch_peeps(no_person, is_prod=True)
            # this needs prod on to truly switch
            if is_troll:
                troll_msg(to_number)
                return
            else:
                switcheroo_msg(switcheroo, switch_num, is_prod=True)

    else:
        message = creepy_response(info)

    # Since the to_number is not formatted corrected, we add a + and slice off the first three chars and add a +
    # For example, the number looks like %2B16025551234, so we slice off %2B and add a plus.
    send_message(message, to_number, media_url='https://media.giphy.com/media/39GAXpLVKvYRO/giphy.gif')

    print("Received event: " + str(event))
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>All done!</Message></Response>'
