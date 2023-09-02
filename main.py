import requests
import time
import smtplib
import datetime as dt

MY_LAT = 43.87  # your latitude
MY_LNG = 75.355  # your longitude
MY_UTC = 1  # your utc

my_gmail = "your email"
gmail_connection = "smtp.gmail.com"
app_password = "your app pass"


def iss_passing_by():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT - 1 < iss_latitude < MY_LAT + 1 and MY_LNG - 1 < iss_longitude < MY_LNG + 1:
        return True
    else:
        return False


def is_night_time():

    today = dt.datetime.now()

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()

    sunrise = data["results"]["sunrise"]
    # Trimming
    sunrise_hour = int(sunrise[sunrise.index("T") + 1:sunrise.index(":")]) + MY_UTC

    sunset = data["results"]["sunset"]
    # Trimming
    sunset_hour = int(sunset[sunset.index("T") + 1:sunset.index(":")]) + MY_UTC

    if today.hour >= sunset_hour or today.hour <= sunrise_hour:
        return True
    else:
        return False


while True:

    time.sleep(60)

    if iss_passing_by() and is_night_time():
        try:
            with smtplib.SMTP(gmail_connection) as connection:
                connection.starttls()
                connection.login(user=my_gmail,
                                 password=app_password
                                 )
                connection.sendmail(from_addr=my_gmail,
                                    to_addrs=[my_gmail],
                                    msg="Subject:ISS PASSING!\n\nLook Up!\nThe ISS is passing by!"
                                    )
            print("Ok. The email has been sent.")
        except:
            print("can't send the Email")
