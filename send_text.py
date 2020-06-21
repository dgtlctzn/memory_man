from twilio.rest import Client
import pickle


def send_text(message):
    with open('/Users/admin/PycharmProjects/Memory_Man/pickle_sms.pkl', 'rb') as pkl:
        pickle_sms = pickle.load(pkl)
        client = Client(pickle_sms['Twilio SID'], pickle_sms['Twilio Auth'])
        client.messages.create(to='14043583607',
                               from_='+12565154057',
                               body=message)



