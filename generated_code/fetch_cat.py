import requests

def fetch_cat_photo():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        data = response.json()
        return data[0]["url"]
    else:
        return None

def test_fetch_cat_photo():
    assert fetch_cat_photo() != None
