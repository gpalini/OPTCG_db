import json
import requests

api_url = "http://localhost:8080/"
JSON_PATH = "OPTCG_db.json"


def get_all():
    response = requests.get(api_url + "card")
    print(response.json())


def add_one_card(card):
    prod_short = card["card id"].split("-")[0].strip()
    print(card)
    id = card["card id"].split("-")[1].strip()
    del card["card id"]
    card["id"] = id
    card["prod_short"] = prod_short
    card["img_url"] = card["art"]
    del card["art"]
    if "alternate art" in card:
        card["img_url_2"] = card["alternate art"]
        del card["alternate art"]
    card["category"] = card["card category"]
    del card["card category"]
    print(card)
    response = requests.post(api_url + "card", json=card)
    print(response.status_code)


def test_add():
    with open(JSON_PATH, 'r+') as f:
        global cards_db
        cards_db = json.load(f)
        f.close()
    for sets in cards_db.values():
        for card in sets.values():
            add_one_card(card)



def __main__():
    get_all()
    test_add()
    get_all()


__main__()