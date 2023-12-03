import json
import requests
import main_for_migration

api_url = "http://localhost:8080/"
JSON_PATH = "new_db.json"


def get_all():
    response = requests.get(api_url + "cards")
    print(response.json())


def add_one_card(card):
    prod_short = card["card id"].split("-")[0].strip()
    print(card)
    id = card["card id"].split("-")[1].strip()
    del card["card id"]
    card["id"] = id
    card["prodShort"] = prod_short
    card["img_url"] = card["art"]
    del card["art"]
    if "alternate art" in card:
        card["img_url_2"] = card["alternate art"]
        del card["alternate art"]
    card["category"] = card["card category"]
    if "counter power" in card:
        card["counter"] = card["counter power"]
        del card["counter power"]
    card["category"] = card["card category"]
    del card["card category"]
    print(card)
    response = requests.post(api_url + "cards", json=card)
    print(response.status_code)


def test_add():
    with open(JSON_PATH, 'r+') as f:
        global cards_db
        cards_db = json.load(f)
        f.close()
    for sets in cards_db.values():
        for card in sets.values():
            add_one_card(card)


def fix_db_camel():
    with open(JSON_PATH, 'r+') as f:
        global cards_db
        cards_db = json.load(f)
        f.close()
    for sets in cards_db.values():
        for card in sets.values():
            if "Name" in card:
                card["name"] = card.pop("Name")
            if "Card ID" in card:
                card["card id"] = card.pop("Card ID")
            if "Type" in card:
                card["type"] = card.pop("Type")
            if "Card Category" in card:
                card["card category"] = card.pop("Card Category")
            if "Effect" in card:
                card["effect"] = card.pop("Effect")
            if "Trigger" in card:
                card["trigger"] = card.pop("Trigger")
            if "Product" in card:
                card["product"] = card.pop("Product")
            if "Color" in card:
                card["color"] = card.pop("Color")
            if "Rarity" in card:
                card["rarity"] = card.pop("Rarity")
            if "Cost" in card:
                card["cost"] = card.pop("Cost")
            if "Life" in card:
                card["life"] = card.pop("Life")
            if "Power" in card:
                card["power"] = card.pop("Power")
            if "Counter Power" in card:
                card["counter power"] = card.pop("Counter Power")
            if "Attribute" in card:
                card["attribute"] = card.pop("Attribute")
            if "Art" in card:
                card["art"] = card.pop("Art")
            if "Alternate Art" in card:
                card["alternate art"] = card.pop("Alternate Art")
            if "Alternate Art 2" in card:
                card["alternate art 2"] = card.pop("Alternate Art 2")
    with open(JSON_PATH, 'w') as f2:
        json.dump(cards_db, f2, indent=4)
        print("JSON output successfully written in the file " + JSON_PATH + ".")


def __main__():
    main_for_migration.refresh_db()
    fix_db_camel()
    get_all()
    test_add()
    get_all()


__main__()