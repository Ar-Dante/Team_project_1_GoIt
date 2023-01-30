import json
from datetime import datetime
import requests


def get_currency(currencyname):
    try:
        today = datetime.now().strftime("%Y%m%d")
        URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + today + '&json'
        content = requests.get(URL)
        headers = {'User-Agent':'Mozilla/5.0'}
        result = json.loads(content.text)[0]
    except Exception:
        return "Problems with network"
    else:
        return f"\n{result['exchangedate']}  {result['txt']}: {result['rate']}\n"