import requests
from bs4 import BeautifulSoup
import json


def get_courses(courses_url):
    response = requests.get(courses_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    courses = {}
    for row in soup.select('table.forextable tr')[1:]:
        currency = row.select_one('td:nth-child(1)').text.strip()
        exchange_rate = row.select_one('td:nth-child(3)').text.strip()
        courses[currency] = float(exchange_rate)
    return courses


def overwriting_json(courses):
    with open('currency.json', 'r+') as file:
        data = json.load(file)
        for currency in courses:
            data[currency] = courses[currency]
        file.seek(0)
        json.dump({k: v for k, v in sorted(data.items())}, file)
        file.truncate()


url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'

overwriting_json(get_courses(url))
