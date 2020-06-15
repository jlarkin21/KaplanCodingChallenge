import sys
import requests
import json
from threading import Thread
from flask import Flask, request
from twilio.rest import Client
import atexit

# OANDA ACCOUNT INFO
account_id = "001-001-4278412-001"
url = "https://api-fxtrade.oanda.com/v3/accounts/" + account_id
api_token = "c62f0f8fac5472cb5d4d2a5d270a4cba-4981fc0fecaey5w54w5f80e891312da7a11"

authentication_string = "Bearer " + api_token
header = {
    "Authorization": authentication_string,
    "content-type": "application/json",
    "Accept-Datetime-Format": "RFC3339"
}

# TWILIO SMS ACCOUNT INFO
account_sid = "AC6d497ef0878gawers331f3d4"
auth_token = "d85c0b335c5uyif12e4aawds92de9dc576"
messaging_service_id = "MG6ee57fasad345atfu613ccc1675d4df6f7552"
client = Client(account_sid, auth_token)

app = Flask(__name__)

holding_position = False

def get_account_details():
    response = requests.get(url, headers=header)
    print(response.text)


def place_order(currency_pair, units, time_in_force="FOK", order_type="MARKET", position_fill="DEFAULT"):
    order_data = {
        "order": dict(units=units, instrument=currency_pair, timeInForce=time_in_force, type=order_type,
                      positionFill=position_fill)
    }
    response = requests.post(url + "/orders", data=json.dumps(order_data), headers=header)
    print(response.text)


def cancel_order(currency_pair):
    order_data = {"longUnits": "ALL"}
    response = requests.post(url + "/positions/" + currency_pair + "/close", data=json.dumps(order_data), headers=header)
    print(response.text)


@app.route('/', methods=['POST'])
def alert_result():
    alert_data = request.json

    trade_id = alert_data.get('id') 

    ticker = alert_data.get('ticker')
    instrument = ticker[:3] + '_' + ticker[3:]

    units = alert_data.get('contracts')
    if trade_id == "Short":
        units = '-' + units

    if "Close" in trade_id and holding_position:
        cancel_order(instrument)
    else:
        place_order(instrument, units)

    print(alert_data)
    send_sms(trade_id + " " + units + " units of " + ticker)


    # EXPECTED ALERT JSON     -         {'id': 'Close entry(s) order Short', 'order': 'buy', 'contracts': '7734', 'ticker': 'NZDJPY'}


    return ''

# On Flask Error
@app.errorhandler(Exception)
def handle_error(e):
    send_sms("Error with trade bot! Exception: " + str(e))
    with open("exceptions.txt", "w") as log_file: 
        # Writing data to a file 
        file1.write(str(e)) 
    return ''

def send_sms(text):
    client.messages.create(
            body=text,
            messaging_service_sid=messaging_service_id,
            to='+1444444444' 
    )

    print("sms message sent")

atexit.register(send_sms("ForexBot stopped running"))

if __name__ == "__main__":
    app.run(port=2020)

