import json
import time
import http.client
import datetime
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
    i = 1
    for session in sessions:
        min_age_limit = session['min_age_limit']
        fee_type = session['fee_type']
        # if min_age_limit == 18 and fee_type == 'Free':
        if min_age_limit == 18:
            dose_one_capacity = session['available_capacity_dose1']
            if dose_one_capacity > 19:
                center_name = session['name']
                frequency = 2500
                duration = 1000
                winsound.Beep(frequency, duration)
                print(i, "--", dose_one_capacity, "--", center_name, "--", datetime.datetime.now())
                i += 1


def get_slots():
    while True:
        print("Searching", datetime.datetime.now())
        date = datetime.date.today().strftime("%d-%m-%Y")
        sessions = get_sessions_by_district("650", date)
        analyze_sessions(sessions)
        time.sleep(10)

if __name__ == "__main__":
    get_slots()
