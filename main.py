# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Change MY_LAT/MY_LONG to your current location. latlong.net
# 3. Go to your email provider and make it allow less secure apps.
# 4. Update the SMTP ADDRESS to match your email provider.

import requests
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
import time

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"
MY_LAT = 26.245609  # Your latitude
MY_LONG = 68.406731  # Your longitude


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True  # IT's Dark

while True:
    # If the ISS is close to my current position
    # and it is currently dark
    # Then send me an email to tell me to look up.
    if is_overhead() and is_night():
        msg = EmailMessage()
        msg['From'] = MY_EMAIL
        msg['To'] = MY_EMAIL
        msg['Subject'] = "Look Up👆"
        body = """
        Hey!
            The ISS is above you in the sky.
        """
        msg.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS", context=context) as connection:
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="malikfarhan57@outlook.com",
                msg=msg.as_string()
            )
        time.sleep(60)
