import json
import time
import http.client
import datetime
import winsound

post = "POST"
get = "GET"
secret = "U2FsdGVkX1+YLRftb9lThlR8kBkTdtAvQz7C18IOvvonY4PPnuGDsi605yM5nHQdOloecjxuVsyhPtGUp+rp3A=="
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
headers = {
    'User-Agent': user_agent
}
website = "cdn-api.co-vin.in"
conn = http.client.HTTPSConnection(website)

def get_sessions_by_district(id, date):
    '''
    curl --location --request GET "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=650&date=22-05-2021" --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

    '''
    endpoint = "/api/v2/appointment/sessions/public/findByDistrict?district_id="+id+"&date="+date
    # endpoint = "/api/v2/appointment/sessions/public/findByPin?pincode="+id+"&date="+date
    payload = ""
    conn.request(get, endpoint, payload, headers)
    response = conn.getresponse()
    code = response.getcode()
    if code != 200:
        print(code)
        return None
    sessions = json.loads(response.read().decode("utf-8"))['sessions']
    return sessions

def analyze_sessions(sessions):
    i = 1
    for session in sessions:
        min_age_limit = session['min_age_limit']
        if min_age_limit == 18:
            dose_two_capacity = session['available_capacity_dose2']
            district_name = session['district_name']
            fee = session['fee_type']
            pincode = session['pincode']
            vaccine = session['vaccine']
            if fee == 'Free' and vaccine == 'COVISHIELD' and dose_two_capacity > 20:
                print()
                center_name = session['name']
                frequency = 2500
                duration = 1000
                winsound.Beep(frequency, duration)
                print(i, "--", dose_two_capacity, "--", district_name, ',', pincode, ',', center_name, ',', datetime.datetime.now())
                i += 1

def get_district_ids(id):
    endpoint = '/api/v2/admin/location/districts/' + id
    payload = ""
    conn.request(get, endpoint, payload, headers)
    response = conn.getresponse();
    ids = []
    districts = json.loads(response.read().decode('utf-8'))['districts']
    for district in districts:
        id = district['district_id']
        ids.append(id)
    return ids


def get_slots(ids):
    while True:
        print("Searching", datetime.datetime.now())
        initial_date = datetime.date.today()
        for i in range (0,6):
            current_date = (initial_date + datetime.timedelta(days=i)).strftime("%d-%m-%Y")
            print(current_date)
            for id in ids:
                sessions = get_sessions_by_district(str(id), current_date)
                if sessions != None:
                    analyze_sessions(sessions)
                else:
                    continue
        time.sleep(5)

if __name__ == "__main__":
    ids = ['97']
    get_slots(ids)
