from datetime import date, timedelta
import json
import os
import requests

apiKey = os.environ['GIANT_BOMB_API_KEY']
startTimeDelta = timedelta(days=1)
endTimeDelta = timedelta(days=7)


def processGameCheck(event, context):
    currentDate = date.today()
    startDate = currentDate + startTimeDelta
    endDate = currentDate + endTimeDelta

    print(f'Query for games between [{startDate}] and [{endDate}]')
    games = searchGames(startDate, endDate)
    convertedGames = processGames(games)
    print(f'Converted games: {convertedGames}')



def searchGames(startDate, endDate):
    url = 'https://www.giantbomb.com/api/releases'
    headers = {'user-agent': 'lambda-function'}
    fieldList = 'name,expected_release_day,expected_release_month,expected_release_year,release_date,platform'
    filter = f'release_date:{startDate:%Y-%m-%d}|{endDate:%Y-%m-%d}'
    sort = 'release_date:asc'
    payload = {
        'api_key': apiKey,
        'format': 'json',
        'field_list': fieldList,
        'filter': filter,
        'sort': sort
    }

    print(f'Request payload: {payload}')
    r = requests.get(url, headers=headers, params=payload)

    # response comes back as str. convert to dict
    response = json.loads(r.text)
    # print(json.dumps(response, indent=2))  # pretty print json string
    print(json.dumps(response))
    return response['results']


def processGames(games):
    convertedGames = set()

    for game in games:
        name = game['name']
        releaseYear = game['expected_release_year']
        releaseMonth = game['expected_release_month']
        releaseDay = game['expected_release_day']
        platform = game['platform']
        platformName = platform['name']

        if any(v is None for v in [releaseYear, releaseMonth, releaseDay]):
            print(f'Skip game: {name}')
            continue

        releaseDate = date(releaseYear, releaseMonth, releaseDay)
        gameInfo = f'{releaseDate:%D} | {name} | {platformName}'
        convertedGames.add(gameInfo)

    return sorted(convertedGames)


if __name__ == "__main__":
    processGameCheck('', '')