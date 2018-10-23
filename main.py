import json
import requests
import pandas as pd
from datetime import date, timedelta


def get_token(client_id,client_secret):
  payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
  }

  headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept':'application/json'}

  r = requests.post(url + '/oauth2/token', data=payload, headers=headers)
  if r.status_code == 200:
    json_data = r.json()
    token = json_data['access_token']
    return token
  else:
    print(r.status_code)
    print(r.text)


def get_stat(dateStart, dateEnd):
    payload = {
        'reportType': 'CampaignPerformance',
        'startDate': dateStart,
        'endDate': dateEnd,
        'dimensions': [
            'Day',
            'CampaignId'
        ],
        'metrics': [
            'Displays',
            'Clicks',
            'AdvertiserCost'
        ],
        'format': 'Json',
        'currency': 'RUB',
        'timezone': 'GMT'
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/octet-stream',
        'Authorization': 'Bearer ' + get_token(client_id, client_secret)
    }

    r = requests.post(url + '/v1/statistics', data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        json_data = r.json()
        df = pd.DataFrame(json_data['Rows'])
        df = df[['Campaign ID', 'Day', 'Impressions', 'Clicks', 'Cost']]
        df['Day'] = pd.to_datetime(df['Day'])
        df.columns = ['campaignId', 'date', 'impressions', 'clicks', 'cost']
        return df
    else:
        print(r.status_code)
        print(r.text)


def main():
    client_id = '****'
    client_secret = '****'
    url = 'https://api.criteo.com/marketing'

    # дата с которой начинаем забирать данные
    dateStart = date.today() - timedelta(30)
    dateStart = dateStart.strftime('%Y-%m-%d')
    dateEnd = date.today() - timedelta(1)
    dateEnd = dateEnd.strftime('%Y-%m-%d')

    df = get_stat(dateStart, dateEnd)


if __name__ == '__main__':
    main()