#! /usr/bin/python3

import datetime as dt
from twilio.rest import Client
import pickle


current_date = dt.date.today()
this_year = dt.date.today().year


def send_text(message):
    with open('pickle_sms.pkl', 'rb') as pkl:
        pickle_sms = pickle.load(pkl)
        client = Client(pickle_sms['Twilio SID'], pickle_sms['Twilio Auth'])
        client.messages.create(to='15058576634',
                               from_='+12991823362',
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


# first, last are the possible date ranges for fathers/mothers day for the next decade or so
def parents_day(my_month, first, last):
    def get_day(my_year):
        for i in range(first, last):
            if dt.date(year=my_year, month=my_month, day=i).isoweekday() == 7:
                return dt.date(year=my_year, month=my_month, day=i)
    return get_day


dad_day = parents_day(6, 16, 22)
mom_day = parents_day(5, 8, 15)
parents_day_dict = {'father': dad_day(this_year), 'mother': mom_day(this_year)}

birthday_dict = {"Melissa": (1984, 9, 11),
                 "John": (1999, 2, 29),
                 "Joe": (1985, 8, 1),
                 "Melinda": (1967, 4, 13),
                 "Craig": (1962, 11, 17),
                 "Dad": (1950, 10, 22),
                 "Mom": (1951, 1, 9),
                 "Kevin": (1989, 5, 2)}

# a dict for birthday datetimes
first_bday_dict = {i: dt.date(year=birthday_dict[i][0],
                              month=birthday_dict[i][1],
                              day=birthday_dict[i][2])
                   for i in birthday_dict}

# a dict for birthdays datetimes this year
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
        with open('birthday_error.txt', 'a') as err:
            err.write(str(dt.datetime.now()) + ': ' + '\n' + str(err))
