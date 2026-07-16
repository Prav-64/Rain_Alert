import os

import requests
from twilio.rest import Client

OWM_API_KEY = os.environ.get("OWM_API_KEY")
OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
LAT = os.environ.get("LAT")
LON = os.environ.get("LON")

RECIPIENT_NUMBER = os.environ("RECIPIENT_NUMBER")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

weather_request_params = {
    "lat": LAT,
    "lon": LON,
    "appid": OWM_API_KEY,
    "cnt": "4"
}

with requests.get(url=OWM_API_ENDPOINT, params=weather_request_params) as response:
    weather_data = response.json()
    response.raise_for_status()

num_of_forecasts = int(weather_request_params["cnt"])

id_list = []
for forecast in range(num_of_forecasts):
    weather_id_for_forecasts = weather_data["list"][forecast]["weather"][0]["id"]
    id_list.append(weather_id_for_forecasts)

is_going_to_rain = False
for weather_id in id_list:
    if weather_id < 700:
        is_going_to_rain = True

if is_going_to_rain:
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain remember to bring an Umbrella! ☔🤧",
        from_=f"whatsapp:{TWILIO_NUMBER}",
        to=f"whatsapp:{RECIPIENT_NUMBER}",
    )

    print(message.status)
