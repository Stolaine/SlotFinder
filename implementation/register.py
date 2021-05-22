import json
import time

import requests
import hashlib
import http.client
import datetime
from playsound import playsound
import winsound

post = "POST"
get = "GET"
mobile = "9631496224"
secret = "U2FsdGVkX1+YLRftb9lThlR8kBkTdtAvQz7C18IOvvonY4PPnuGDsi605yM5nHQdOloecjxuVsyhPtGUp+rp3A=="
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
headers = {
    'User-Agent': user_agent
}
website = "cdn-api.co-vin.in"

def get_sessions_by_district(district_id, date):
    conn = http.client.HTTPSConnection(website)
    endpoint = "/api/v2/appointment/sessions/public/findByDistrict?district_id="+district_id+"&date="+date
    payload = ""
    conn.request(get, endpoint, payload, headers)
    response = conn.getresponse()
    sessions = json.loads(response.read().decode("utf-8"))['sessions']
    return sessions

def analyze_sessions(sessions):
    print("analyse_sessions")
    i = 1
    for session in sessions:
        min_age_limit = session['min_age_limit']
        fee_type = session['fee_type']
        if min_age_limit == 18 and fee_type == 'Free':
            dose_one_capacity = session['available_capacity_dose1']
            if dose_one_capacity >= 0:
                center_name = session['name']
                frequency = 2500
                duration = 1000
                winsound.Beep(frequency, duration)
                print(i, "--", dose_one_capacity, "--", center_name, "--", datetime.datetime.now())
                i += 1

def get_states():
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    payload = {}
    response = requests.request(get, url, headers=headers, data=json.dumps(payload))
    print(response.text)

def get_states_with_token(token):
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    payload = {
        "token": token
    }
    response = requests.request(get, url, headers=headers, data=json.dumps(payload))
    print(response.text)

def confirm_otp(otp, transaction_id):
    url = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"
    payload = {
        "otp": otp,
        "txnId": transaction_id
    }
    response = requests.request(post, url, headers=headers, data=json.dumps(payload))
    token = response.json()['token']
    return token


def encrypt(mobile_otp):
    sha_signature = hashlib.sha256(mobile_otp.encode()).hexdigest()
    return sha_signature

def get_transaction_id():
    url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
    payload = {
        "mobile": mobile,
        "secret": secret
    }
    response = requests.request(post, url, headers=headers, data=json.dumps(payload))
    transaction_id = response.json()['txnId']
    return transaction_id

def get_slots():
    while True:
        date = datetime.date.today().strftime("%d-%m-%Y")
        sessions = get_sessions_by_district("650", date)
        analyze_sessions(sessions)
        time.sleep(1)


if __name__ == "__main__":
    get_slots()


get_districts_command = 'curl --location --request GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/34" --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"'
get_states_command = 'curl --location --request GET "https://cdn-api.co-vin.in/api/v2/admin/location/states" --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"'
get_session_by_district = 'curl --location --request GET "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=650&date=21-05-2021" --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"'



