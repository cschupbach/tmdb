import requests


def get_data(url):
    page = requests.get(url)
    data = page.json()
    return data
