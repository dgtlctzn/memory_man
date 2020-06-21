#! /usr/bin/python3

import datetime as dt
from twilio.rest import Client
import pickle


current_date = dt.date.today()
this_year = dt.date.today().year


def send_text(message):
    with open('/home/pi/PiPy/pickle_sms.pkl', 'rb') as pkl:
        pickle_sms = pickle.load(pkl)
        client = Client(pickle_sms['Twilio SID'], pickle_sms['Twilio Auth'])
        client.messages.create(to='14043583607',
                               from_='+12565154057',
                               body=message)


def number_str(number):
    digit_2 = number % 10
    if digit_2 == 3:
        num_str = 'rd'
    elif digit_2 == 2:
        num_str = 'nd'
    elif digit_2 == 1:
        num_str = 'st'
    else:
        num_str = 'th'
    return str(number) + num_str


def parents_day(my_month, first, last):
    def get_day(my_year):
        for i in range(first, last):
            if dt.date(year=my_year, month=my_month, day=i).isoweekday() == 7:
                return dt.date(year=my_year, month=my_month, day=i)
    return get_day


dad_day = parents_day(6, 16, 22)
mom_day = parents_day(5, 8, 15)
parents_day_dict = {'father': dad_day(this_year), 'mother': mom_day(this_year)}

birthday_dict = {"Melissa": (1989, 12, 29),
                 "John": (1994, 6, 5),
                 "Joe": (1989, 7, 20),
                 "Melinda": (1960, 7, 5),
                 "Craig": (1959, 4, 14),
                 "Dad": (1958, 12, 16),
                 "Mom": (1955, 8, 6),
                 "Kevin": (1993, 8, 26)}

first_bday_dict = {i: dt.date(year=birthday_dict[i][0],
                              month=birthday_dict[i][1],
                              day=birthday_dict[i][2])
                   for i in birthday_dict}

this_bday_dict = {i: dt.date(year=this_year,
                             month=birthday_dict[i][1],
                             day=birthday_dict[i][2])
                  for i in birthday_dict}


def main():
    for name, this_bday in this_bday_dict.items():
        age = this_bday.year - first_bday_dict[name].year
        if current_date < this_bday and name != 'Joe':
            if (this_bday - current_date).days == 21:
                send_text(f"Three weeks till it's {name}'s {number_str(age)} birthday!")
            elif (this_bday - current_date).days == 7:
                send_text(f"One more week till it's {name}'s birthday!")
        elif current_date == this_bday and name != 'Joe':
            send_text(f"It's {name}'s birthday!")
        elif current_date == this_bday and name == 'Joe':
            send_text(f"Happy birthday from your Raspberry Pi!!!")
    for parent, holiday in parents_day_dict.items():
        if current_date < holiday:
            if (holiday - current_date).days == 14:
                send_text(f"Two weeks till {parent}'s day!")
        elif current_date == holiday:
            send_text(f"Today is {parent}'s day! Tell your {parent} to have a good one")


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        with open('/home/pi/PiPy/birthday_error.txt', 'a') as err:
            err.write(str(dt.datetime.now()) + ': ' + '\n' + str(err))
