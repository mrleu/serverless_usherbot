from oauth2client.service_account import ServiceAccountCredentials
import gspread
import ast
import arrow
from helpers import next_sunday
from constants import *
creeper = 'SHHHHHHHHH'
scope = ['https://spreadsheets.google.com/feeds']
URL = 'SHHHHHHHHHHHHHhh'
credentials = ServiceAccountCredentials.from_json_keyfile_name('usher_auth.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url(URL)
wks_volunteer = wks.get_worksheet(1)

def logging_no_serve(person):
    coming_sun = next_sunday(arrow.now())
    credentials = ServiceAccountCredentials.from_json_keyfile_name('usher_auth.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url(creeper)
    creep_sheet = wks.get_worksheet(0)
    no_sho = ast.literal_eval(creep_sheet.acell("A1").value)
    try:
        no_sho[coming_sun].append(person)
    except KeyError:
        no_sho[coming_sun] = [person]
    creep_sheet.update_acell('A1', no_sho)
    return no_sho[coming_sun]

def cur_week_ushers(a_date):
    URL = 'SHHHHHHHHHHHHhh'
    credentials = ServiceAccountCredentials.from_json_keyfile_name('usher_auth.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url(URL)
    wks_volunteer = wks.get_worksheet(1)
    year = arrow.get(a_date).format('YYYY')
    for num in range(8,59):
        date = wks_volunteer.acell("C" + str(num)).value
        parse_date = date[4:]
        print(f'og says {date}')
        print('sheet says: {}'.format(parse_date))
        print(len(parse_date))
        if len(parse_date) > 1:
            arrow_date = arrow.get(year + '-' + MONTH_HASH_MAP[date[:3]] + '-' + date[4:])
        else:
            arrow_date = arrow.get(year + '-' + MONTH_HASH_MAP[date[:3]] + '-0' + date[4:])
        print(date[:3])
        print(date[4:])
        print(year + '-' + MONTH_HASH_MAP[date[:3]] + '-0' + date[4:])
        print(f"arrow date is {arrow_date}")
        arrow_date_str = arrow_date.format('YYYY-MM-DD')
        print("looking for {}:".format(a_date.format('YYYY-MM-DD')))
        print("current is {}:".format(arrow_date_str))
        if arrow_date_str == a_date.format('YYYY-MM-DD'):
            print(date)
            print('these are the ushers:')
            usher1 = wks_volunteer.acell("H" + str(num)).value
            usher2 = wks_volunteer.acell("I" + str(num)).value
            usher3 = wks_volunteer.acell("J" + str(num)).value
            usher4 = wks_volunteer.acell("K" + str(num)).value
            break
    save = dict()
    save[usher1] = 'H' + str(num)
    save[usher2] = 'I' + str(num)
    save[usher3] = 'J' + str(num)
    save[usher4] = 'K' + str(num)
    return save

def find_next_week(cant_serve, person, is_prod=False):
    #TODO(aleu): once owrk, no more future days
    coming_week = arrow.now().shift(days=7)
    upcoming_church_date = next_sunday(coming_week)
    coming = cur_week_ushers(upcoming_church_date)

    new_week = coming_week.shift(days=7)
    new_week_church = next_sunday(new_week)
    new_coming = cur_week_ushers(new_week_church)

    for name, cell in new_coming.items():
        if name not in cant_serve:
            if is_prod:
                wks_volunteer.update_acell(coming[person], name)
                wks_volunteer.update_acell(new_coming[name], person)
            else:
                print('no prod. nothing changed')
            print(f"{person} is no, {name} is next.")
            return name, PHONE_NUMBER_MAP[name]



