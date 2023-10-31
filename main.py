import json

JSON_PATH = "OPTCG_db.json"
INPUT_TXT = "input.txt"
INPUT2_TXT = "input_st_p.txt"


def add_to_wishlist():
    print("Add to wishlist...")


def search_start():
    search_mode = input("\nSelect the search mode\nI: card ID\nN: name\nC: color\nS: set\nR: rarity\n")
    if search_mode.lower()[0] == "i":
        search_param = "Card ID"
    elif search_mode.lower()[0] == "n":
        search_param = "Name"
    elif search_mode.lower()[0] == "s":
        search_param = "Product"
    elif search_mode.lower()[0] == "r":
        search_param = "Rarity"


def add_new_card(card_string):
    card_lines = card_string.split("*")
    card_lines = [x for x in card_lines if x != ""]
    if len(card_lines) < 6:
        return False
    key = card_lines[3].strip()
    is_attr_name = True
    attr_name = ""
    new_card = {}
    print("New card " + key + "! Proceeding...")
    for line in card_lines:
        if line == "\n":
            break
        else:
            if is_attr_name:
                attr_name = line.strip()
                is_attr_name = False
            else:
                if attr_name != "Color" and attr_name != "Type":
                    new_card[attr_name] = line.strip()
                elif attr_name == "Color":
                    new_card[attr_name] = []
                    for single_color in line.split("/"):
                        new_card[attr_name].append(single_color.strip())
                elif attr_name == "Type":
                    new_card[attr_name] = []
                    for single_type in line.split("/"):
                        new_card[attr_name].append(single_type.strip())
                is_attr_name = True
    return new_card


def refresh_db():
    data = ""
    with open(JSON_PATH, 'r+') as f:
        try:
            data = json.load(f)
            data["Red"]
        except json.decoder.JSONDecodeError as decodeError:
            data = {}
        except KeyError as keyError:
            data = {}
    read_input(INPUT_TXT, data)
    read_input(INPUT2_TXT, data)


def read_input(file, data):
    with open(file) as f:
        lines = f.readlines()
        lines = "*".join(lines).replace("\n", "")
        for card in lines.split("/////"):
            card_to_add = add_new_card(card)
            if card_to_add["Product"] not in data.keys():
                data[card_to_add["Product"]] = {}
            data[card_to_add["Product"]][card_to_add["Card ID"]] = card_to_add
        with open(JSON_PATH, 'w') as f2:
            json.dump(data, f2, indent=4)
            print("JSON output successfully written in the file " + JSON_PATH + ".")


def __main__():
    select = input("Do you wanna refresh the database? Y for yes\n")
    if select.lower()[0] == "y":
        refresh_db()
    while select.lower()[0] != "e":
        select = input("\nWhat you wanna do?\nS: search\nA: add to wishlist\nE: exit\n")
        if select.lower()[0] == "s":
            search_start()
        elif select.lower()[0] == "a":
            add_to_wishlist()


#__main__()