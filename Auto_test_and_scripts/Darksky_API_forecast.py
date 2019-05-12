import requests

r = requests.get('https://api.darksky.net/forecast/d5d51cd50fc7ee175a9bb6b187f97dda/46.4825,30.7233?units=ca')

forecast_items = []
for k, v in r.json()['currently'].items():
    if k == 'summary':
        forecast_items.append(v)
    if k == 'temperature':
        forecast_items.append(v)
    if k == 'windSpeed':
        forecast_items.append(v)
    if k == 'humidity':
        forecast_items.append(v)
forecast = "Current weather in Odessa:\n" \
           "%s\n" \
           "Temperature: %s °C\n" \
           "Wind: %s km/s\n" \
           "Humidity: %s %%" % (forecast_items[0], forecast_items[1], forecast_items[2], forecast_items[3])

f = open("forecast.txt", "w+")
f.write(forecast)
