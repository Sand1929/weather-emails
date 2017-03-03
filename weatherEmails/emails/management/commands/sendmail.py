from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from emails.models import Subscriber

import requests
import json
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Sends a personalized email to each subscriber."

    def handle(self, *args, **kwargs):
        for s in Subscriber.objects.all():
            # get the local weather
            city = s.city.name.replace(" ", "_")
            state = s.city.state
            r = requests.get("http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(settings.WEATHER_API_KEY, state, city))
            if r.status_code != 200:
                raise CommandError('Weather API call failed')
            current_data = json.loads(r.text)

            # get the historical weather
            r = requests.get("http://api.wunderground.com/api/{}/almanac/q/{}/{}.json".format(settings.WEATHER_API_KEY, state, city))
            if r.status_code != 200:
                raise CommandError('Weather API call failed')
            hist_data = json.loads(r.text)

            # determine subject line
            current_weather = current_data['current_observation']['weather']
            current_weather_image = current_data['current_observation']['icon_url']
            current_temp = current_data['current_observation']['temp_f']
            avg_high = hist_data['almanac']['temp_high']['normal']['F']
            avg_low = hist_data['almanac']['temp_low']['normal']['F']
            if current_weather == 'Sunny' or current_temp >= int(avg_high) + 5:
                subject = "It's nice out! Enjoy a discount on us."
            elif current_weather == 'Precipitating' or current_temp <= int(avg_low) - 5:
                subject = "Not so nice out? That's okay, enjoy a discount on us."
            else:
                subject = "Enjoy a discount on us."

            message = "{}, {}: {} degrees, {}".format(s.city.name, state, current_temp, current_weather)
            html_message = loader.render_to_string('emails/weather_email.html', {'message': message, 'image': current_weather_image})

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [s.email], html_message=html_message)
