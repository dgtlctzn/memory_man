import pickle
import os

if not os.path.exists('/Users/admin/PycharmProjects/Memory_Man/pickle_sms.pkl'):
    sms_cred = {}
    sms_cred['Twilio SID'] = 'AC2e4f195180fa16d7264e119fef84a293'
    sms_cred['Twilio Auth'] = 'a05766224c2a19f4d9d24a19e990dd2e'
    with open('/Users/admin/PycharmProjects/Memory_Man/pickle_sms.pkl', 'wb') as pfile:
        pickle.dump(sms_cred, pfile)