import json
import tkinter as tk
import io
from tkinter import messagebox

import requests
from PIL import Image, ImageTk

import main

JSON_PATH = "OPTCG_db.json"
JSON_DECKS = "saved_decks.json"
JSON_COLL = "collection.json"

colors = ["All"]
rarities = ["All"]
types = ["All"]
card_cats = ["All"]
products = ["All"]
decks_list = []
collection_list = []


def handle_json_reload():
    main.refresh_db()
    with open(JSON_PATH, 'r+') as f:
        global cards_db
        cards_db = json.load(f)
        f.close()
    repopulate_listbox(None)
    messagebox.showinfo("UPDATE", "Card JSON Database successfully updated")


def repopulate_listbox(event):
    listbox.delete(0, 999)
    for sets in cards_db.values():
        for card in sets.values():
            if check_filters(card):
                listbox.insert(999, get_long_name(card))
                if alternate_sel.get() == 1 and card_in_collection(card):
                    listbox.itemconfig(listbox.size() - 1, {'fg': 'red'})
                else:
                    listbox.itemconfig(listbox.size() - 1, {'fg': 'black'})
    title_var.set('Card list - ' + str(listbox.size()) + ' total items')
    print("repopulate size: " + str(listbox.size()))
    title.grid(row=1, column=1)
    listbox.see(0)
    listbox.activate(0)


try:
    with open(JSON_PATH, 'r+') as f1:
        cards_db = json.load(f1)
        f1.close()
except json.decoder.JSONDecodeError as decode_error:
    handle_json_reload()
    with open(JSON_PATH, 'r+') as f1:
        cards_db = json.load(f1)
        f1.close()

with open(JSON_DECKS, 'r+') as f2:
    decks_data = json.load(f2)
    if decks_data != {}:
        decks_list = list(decks_data.keys())
    else:
        decks_list.append("")
    f2.close()

with open(JSON_COLL, 'r+') as f3:
    coll_data = json.load(f3)
    if coll_data != {}:
        collection_list = list(coll_data.keys())
    else:
        collection_list.append("")
    f3.close()


def not_in_list(card_id, results):
    for result in results:
        if card_id == result["Card ID"]:
            return False
    return True


def get_long_name(card):
    if card["Rarity"] == "Leader":
        return card["Name"] + " --- " + "/".join(card["Color"]) + " " + card["Rarity"] + " --- " + card["Card ID"]
    else:
        return card["Name"] + " --- " + "/".join(card["Color"]) + " " + card["Rarity"] + " " + card[
            "Card Category"].capitalize() + " --- " + card["Card ID"]


def first_populate_listbox():
    main.refresh_db()
    for sets in cards_db.values():
        for card in sets.values():
            listbox.insert(999, get_long_name(card))
            fill_selects(card["Color"], card["Rarity"], card["Type"], card["Card Category"], card["Product"])
    title_var.set('Card list - ' + str(listbox.size()) + ' total items')
    print("size: " + str(listbox.size()))
    title.grid(row=1, column=1)
    rarities.sort(key=return_lambda)
    colors.sort(key=return_lambda)
    types.sort()
    card_cats.sort(key=return_lambda)
    products.sort(key=return_lambda)


def check_filters(card):
    if alternate_sel.get() == 0 or got_alt_art(card):
        if color_sel.get() == "All" or color_sel.get() in card["Color"]:
            if rarity_sel.get() == "All" or rarity_sel.get() == card["Rarity"]:
                if type_sel.get() == "All" or type_sel.get() in card["Type"]:
                    if card_cat_sel.get() == "All" or card_cat_sel.get().lower() in card["Card Category"].lower():
                        if product_sel.get() == "All" or product_sel.get() in card["Product"]:
                            if enable_cost_sel.get() == 1 and card["Rarity"] != "Leader":
                                try:
                                    if w1.get() <= int(card["Cost"]) <= w2.get():
                                        return search_entry.get().strip() in card["Name"].lower()
                                except KeyError:
                                    return search_entry.get().strip() in card["Name"].lower()
                            elif enable_cost_sel.get() == 0:
                                return search_entry.get().strip() in card["Name"].lower()


def card_in_collection(card):
    if len(collection_list) > 0 and card["Card ID"] in collection_list:
        return 1


def got_alt_art(card):
    return 'Alternate Art' in card and 'OP-' in card["Product"]


def fill_selects(color_list, rarity, types_list, card_type, product):
    for color in color_list:
        if color not in colors:
            colors.append(color)
    if rarity not in rarities:
        rarities.append(rarity)
    for _type in types_list:
        if _type not in types:
            types.append(_type)
    if card_type.capitalize() not in card_cats:
        card_cats.append(card_type.capitalize())
    if product not in products:
        products.append(product)


def return_lambda(el):
    if el == "All":
        return 1
    elif el == "Leader" or el == "Red" or el == "Leader" or el == "Romance Dawn [OP-01]":
        return 2
    elif el == "Common" or el == "Green" or el == "Character" or el == "Paramount War [OP-02]":
        return 3
    elif el == "Uncommon" or el == "Blue" or el == "Event" or el == "Pillars of Strength [OP-03]":
        return 4
    elif el == "Rare" or el == "Purple" or el == "Stage" or el == "Kingdoms of Intrigue [OP-04]":
        return 5
    elif el == "Super Rare" or el == "Black" or el == "Awakening of the New Era [OP-05]":
        return 6
    elif el == "Secret Rare" or el == "Yellow":
        return 7
    elif el == "Straw Hat Crew [ST-01]":
        return 180
    elif el == "Worst Generation [ST-02]":
        return 181
    elif el == "The Seven Warlords of the Sea [ST-03]":
        return 182
    elif el == "Animal Kingdom Pirates [ST-04]":
        return 183
    elif el == "One Piece Film Edition [ST-05]":
        return 184
    elif el == "Navy [ST-06]":
        return 185
    elif el == "Big Mom Pirates [ST-07]":
        return 186
    elif el == "Side - Monkey D. Luffy [ST-08]":
        return 187
    elif el == "Side - Yamato [ST-09]":
        return 188
    elif el == "Three Captains [ST-10]":
        return 189
    elif el == "Promo":
        return 198
    elif el == "Promo [P]":
        return 199
    else:
        return 200


def get_card_from_card_id(code):
    for sets in cards_db.values():
        for card in sets.values():
            if card["Card ID"] == code:
                return card


def get_current_card_from_listbox():
    code = listbox.get(listbox.curselection()).split(" --- ")[2].strip()
    for sets in cards_db.values():
        for card in sets.values():
            if card["Card ID"] == code:
                return card


def image_data_from_url(url):
    response = requests.get(url)
    return response.content


def handle_switch_arts(img_no, images_list, img_label, switch_button):
    if img_no == len(images_list) - 1:
        img_no = 0
    else:
        img_no += 1
    img_label.config(image=images_list[img_no])
    switch_button.config(command=lambda: handle_switch_arts(img_no, images_list, img_label, switch_button))


def handle_view_card_details(card):
    if card is None or str(card)[0:18] == "<ButtonPress event":
        card = get_current_card_from_listbox()
    details_window = tk.Toplevel()
    details_window.title("Card details - " + card["Card ID"] + " - " + card["Name"])
    details_window.resizable(False, False)
    dw_height = 870
    dw_width = 610
    screen_h = root.winfo_screenheight()
    screen_w = root.winfo_screenwidth()
    x_c = int((screen_w / 2) - (dw_width / 2))
    y_c = int((screen_h / 2) - (dw_height / 2))
    details_window.geometry("{}x{}+{}+{}".format(dw_width, dw_height, x_c, y_c))
    details_window.focus()
    imgs = []
    images_list = []
    coll_label = tk.Label(details_window, font=("Sans Serif", "14"), text="")
    text_var = tk.StringVar()
    coll_label['textvariable'] = text_var
    if "Alternate Art" in card:
        if "Alternate Art 2" in card:
            if alternate_sel.get() == 1:
                imgs.append(card["Alternate Art"])
                imgs.append(card["Alternate Art 2"])
                imgs.append(card["Art"])
            else:
                imgs.append(card["Art"])
                imgs.append(card["Alternate Art"])
                imgs.append(card["Alternate Art 2"])
        elif alternate_sel.get() == 1:
            imgs.append(card["Alternate Art"])
            imgs.append(card["Art"])
        else:
            imgs.append(card["Art"])
            imgs.append(card["Alternate Art"])
    else:
        imgs.append(card["Art"])
    for index, single_img in enumerate(imgs):
        image = Image.open(io.BytesIO(image_data_from_url(single_img))).resize((600, 750))
        img = ImageTk.PhotoImage(image)
        if index == 0:
            panel = tk.Label(details_window, image=img)
            panel.grid(row=0, column=0)
        images_list.append(img)
    if len(imgs) > 1:
        switch_button = tk.Button(details_window, text="Switch art",
                                  command=lambda: handle_switch_arts(0, images_list, panel, switch_button))
        switch_button.grid(row=1, column=0)
    add_coll_button = tk.Button(details_window, text="Add to collection",
                                command=lambda: manage_collection(card, 0, text_var))
    add_coll_button.grid(row=2, column=0)
    if card["Card ID"] in coll_data:
        text_var.set(coll_data[card["Card ID"]])
    else:
        text_var.set("0")
    coll_label.grid(row=3, column=0)
    remove_coll_button = tk.Button(details_window, text="Remove from collection",
                                   command=lambda: manage_collection(card, 1, text_var))
    remove_coll_button.grid(row=4, column=0)
    root.mainloop()


def manage_collection(card, op, text_var):
    card_id = card["Card ID"]
    if op == 0:
        if card["Card ID"] in coll_data:
            coll_data[card_id] += 1
            text_var.set(coll_data[card_id])
            if card_id not in collection_list:
                collection_list.insert(999, card_id)
            update_collection()
            repopulate_listbox(None)
        else:
            coll_data[card_id] = 1
            text_var.set(coll_data[card_id])
            if card_id not in collection_list:
                collection_list.insert(999, card_id)
            update_collection()
            repopulate_listbox(None)
    else:
        if card_id in coll_data:
            coll_data[card_id] -= 1
            text_var.set(coll_data[card_id])
            if coll_data[card_id] <= 0:
                del coll_data[card_id]
                collection_list.remove(card_id)
            update_collection()
            repopulate_listbox(None)


def handle_refresh():
    search_entry.delete(0, len(search_entry.get()))
    alternate_sel.set(0)
    enable_cost_sel.set(0)
    w1.set(0)
    w2.set(0)
    rarity_sel.set("All")
    color_sel.set("All")
    type_sel.set("All")
    card_cat_sel.set("All")
    product_sel.set("All")
    repopulate_listbox(None)


def handle_clear(event):
    search_entry.delete(0, len(search_entry.get()))


def leader_in_deck(decklist):
    for card_id in decklist:
        if get_card_from_card_id(card_id)["Card Category"] == "leader":
            return get_card_from_card_id(card_id)
    return None


def get_sel_deck_size():
    return sum(list(decks_data[deck_sel.get()].values())[1:])


def add_to_deck(card_to_add):
    deck_leader = leader_in_deck(decks_data[deck_sel.get()])
    card_id = card_to_add["Card ID"]

    if card_to_add["Card Category"] == "leader":
        if deck_leader is None:
            decks_data[deck_sel.get()][card_id] = "L"
            update_saved_decks()
        else:
            messagebox.showerror("ERROR", "This deck already has a Leader")
            return
    elif deck_leader is not None:
        if get_sel_deck_size() > 51:
            messagebox.showerror("ERROR", "This deck is already full (50+1 cards)")
        else:
            try:
                if decks_data[deck_sel.get()][card_id] < 4 and card_to_add["Color"][0] in " ".join(
                        deck_leader["Color"]):
                    decks_data[deck_sel.get()][card_id] += 1
                    update_saved_decks()
                else:
                    if get_sel_deck_size() < 50:
                        messagebox.showerror("ERROR", "There are already 4 copies of this card in the deck")

            except KeyError as e:
                if card_to_add["Color"][0] in " ".join(deck_leader["Color"]):
                    decks_data[deck_sel.get()][card_id] = 1
                    update_saved_decks()
                else:
                    messagebox.showerror("ERROR", "This deck is of a different color than the selected card")
    else:
        messagebox.showerror("ERROR", "This deck doesn't yet have a Leader, please add one")


def handle_add_card_to_deck():
    if len(listbox.curselection()) != 0:
        if deck_sel.get() != "":
            card_to_add = get_current_card_from_listbox()
            add_to_deck(card_to_add)
        else:
            messagebox.showerror("ERROR", "Please select a deck")
    else:
        messagebox.showerror("ERROR", "Please select a card")


def handle_view_deck():
    if deck_sel.get() != "":
        print("deck visualization " + deck_sel.get())
        deck_window = tk.Toplevel()
        deck_window.title("Deck data - " + deck_sel.get())
        deck_window.resizable(True, True)
        dw_height = 1130
        dw_width = 1580
        screen_h = root.winfo_screenheight()
        screen_w = root.winfo_screenwidth()
        x_c = int((screen_w / 2) - (dw_width / 2))
        y_c = int((screen_h / 2) - (dw_height / 2))
        deck_window.geometry("{}x{}+{}+{}".format(dw_width, dw_height, x_c, y_c))
        deck_window.focus()
        curr_column = 0
        curr_row = 0
        images = []
        for card_id, num in decks_data[deck_sel.get()].items():
            curr_card = get_card_from_card_id(card_id)
            img_url = curr_card["Art"]
            image = Image.open(io.BytesIO(image_data_from_url(img_url))).resize((250, 300))
            img = ImageTk.PhotoImage(image)
            images.append(img)
            label_img = tk.Label(deck_window, image=images[len(images) - 1])
            label_img.grid(row=curr_row, column=curr_column)
            if curr_card["Rarity"] == "Leader":
                times = str(num)
            else:
                times = "x" + str(num)
            tk.Button(deck_window, text=card_id + " / " + times, font=("Sans Serif", "14"),
                      command=lambda cid=card_id: handle_view_card_details(curr_card)).grid(
                row=curr_row + 1, column=curr_column, padx=15, pady=15)
            if curr_column / 5 == 1:
                curr_row += 2
                curr_column = 0
            else:
                curr_column += 1
        root.mainloop()
    else:
        messagebox.showerror("ERROR", "Please select a deck")


def update_collection():
    with open(JSON_COLL, 'w') as f:
        json.dump(coll_data, f, indent=4)
        print("JSON decks output successfully written in the file " + JSON_COLL + ".")


def update_saved_decks():
    with open(JSON_DECKS, 'w') as f:
        json.dump(decks_data, f, indent=4)
        print("JSON decks output successfully written in the file " + JSON_DECKS + ".")


def handle_create_deck():
    deck_name = new_deck_entry.get()
    new_deck_entry.delete(0, len(new_deck_entry.get()))
    if deck_name != "":
        if len(decks_data) == 0:
            decks_list[0] = deck_name
        else:
            decks_list.append(deck_name)
        menu = deck_sel_om.children["menu"]
        menu.delete(0, "end")
        for value in decks_list:
            menu.add_command(label=value, command=lambda v=value: deck_sel.set(v))
            if value not in list(decks_data.keys()):
                decks_data[value] = {}
        deck_sel_om.config(width=len(max(decks_list, key=len)) * 1)
        update_saved_decks()
    elif deck_name == "":
        messagebox.showerror("ERROR", "Please insert a valid deck name")


root = tk.Tk()
root.title("OPTCG Card Database")
root.eval('tk::PlaceWindow . center')

root.resizable(False, False)

w_height = 800
w_width = 1900
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

x_coord = int((screen_width / 2) - (w_width / 2))
y_coord = int((screen_height / 2) - (w_height / 2))
root.geometry("{}x{}+{}+{}".format(w_width, w_height, x_coord, y_coord))

filters_frame = tk.Frame(root, width=200, height=200)
filters_frame.grid(row=0, column=0, padx=10, pady=5)
list_frame = tk.Frame(root, width=150, height=200)
list_frame.grid(row=0, column=1, padx=15, pady=25)
right_frame = tk.Frame(root, width=55, height=200)
right_frame.grid(row=0, column=2, padx=10, pady=20)

title = tk.Label(list_frame, font=("Sans Serif", "14"), text="Card list - ")
title_var = tk.StringVar()
title['textvariable'] = title_var
title.grid(row=1, column=1)
tk.Button(list_frame, font=("Sans Serif", "14"), text="Reload JSON", command=handle_json_reload).grid(row=1, column=2)

listbox = tk.Listbox(list_frame, height=30, width=60, highlightthickness=1, font=("Sans Serif", "14"),
                     selectmode="SINGLE")
listbox.bind("<Double-1>", handle_view_card_details)
listbox.grid(row=2, column=0, columnspan=3)

tk.Button(right_frame, text="View card details", font=("Sans Serif", "14"),
          command=lambda: handle_view_card_details(None)).grid(row=0,
                                                               column=0,
                                                               pady=20)

tk.Button(right_frame, text="Add card to deck", font=("Sans Serif", "14"), command=handle_add_card_to_deck).grid(row=1,
                                                                                                                 column=0,
                                                                                                                 pady=5)

deck_sel = tk.StringVar()
deck_sel.set("")
tk.Label(right_frame, text="Select deck", font=("Sans Serif", "14")).grid(row=2, column=0, pady=5)
deck_sel_om = tk.OptionMenu(right_frame, deck_sel, *decks_list)
deck_sel_om.grid(row=3, column=0, pady=5)
deck_sel_om.config(width=len(max(decks_list, key=len)) * 1)

tk.Button(right_frame, text="View deck", font=("Sans Serif", "14"), command=handle_view_deck).grid(row=4,
                                                                                                   column=0,
                                                                                                   pady=10)

tk.Label(right_frame, font=("Sans Serif", "14"), text="Deck name").grid(row=5, column=0, pady=15)
new_deck_entry = tk.Entry(right_frame, fg="black", bg="white", width=30, font=("Sans Serif", "14"), bd=4)
new_deck_entry.grid(row=6, column=0)
tk.Button(right_frame, text="Create new deck", font=("Sans Serif", "14"), command=handle_create_deck).grid(row=7,
                                                                                                           column=0,
                                                                                                           pady=15)

search_entry = tk.Entry(filters_frame, fg="black", bg="white", width=30, font=("Sans Serif", "14"), bd=4)
search_entry.bind("<Return>", repopulate_listbox)
search_entry.grid(row=3, column=1, padx=40)
tk.Button(filters_frame, text="Search", font=("Sans Serif", "14"), command=lambda: repopulate_listbox(None)).grid(row=3,
                                                                                                                  column=2)

tk.Button(filters_frame, text="Reset", font=("Sans Serif", "14"), padx=-10, command=handle_refresh).grid(row=3,
                                                                                                         column=3)

label = tk.Label(filters_frame, text=" ")
label.grid(row=4, column=1)

first_populate_listbox()

color_sel = tk.StringVar()
color_sel.set("All")
tk.Label(filters_frame, text="Color", font=("Sans Serif", "14"), pady=20).grid(row=5, column=1)

rarity_sel = tk.StringVar()
rarity_sel.set("All")
tk.Label(filters_frame, text="Rarity", font=("Sans Serif", "14"), pady=20).grid(row=6, column=1)

type_sel = tk.StringVar()
type_sel.set("All")
tk.Label(filters_frame, text="Type", font=("Sans Serif", "14"), pady=20).grid(row=7, column=1)

card_cat_sel = tk.StringVar()
card_cat_sel.set("All")
tk.Label(filters_frame, text="Card category", font=("Sans Serif", "14"), pady=20).grid(row=8, column=1)

product_sel = tk.StringVar()
product_sel.set("All")
tk.Label(filters_frame, text="Set", font=("Sans Serif", "14"), pady=20).grid(row=9, column=1)

dropdown = tk.OptionMenu(filters_frame, color_sel, *colors, command=repopulate_listbox)
dropdown.grid(row=5, column=2)
dropdown.config(width=len(max(colors, key=len)) * 1)
dropdown = tk.OptionMenu(filters_frame, rarity_sel, *rarities, command=repopulate_listbox)
dropdown.grid(row=6, column=2)
dropdown.config(width=len(max(rarities, key=len)) * 1)
dropdown = tk.OptionMenu(filters_frame, type_sel, *types, command=repopulate_listbox)
dropdown.grid(row=7, column=2)
dropdown.config(width=len(max(types, key=len)) * 1)
dropdown = tk.OptionMenu(filters_frame, card_cat_sel, *card_cats, command=repopulate_listbox)
dropdown.grid(row=8, column=2)
dropdown.config(width=len(max(card_cats, key=len)) * 1)
dropdown = tk.OptionMenu(filters_frame, product_sel, *products, command=repopulate_listbox)
dropdown.grid(row=9, column=2)
dropdown.config(width=len(max(products, key=len)) * 1)

enable_cost_sel = tk.IntVar()
tk.Checkbutton(filters_frame, text='Enable cost filter', variable=enable_cost_sel, onvalue=1, offvalue=0).grid(row=10,
                                                                                                               column=1)
enable_cost_sel.set(0)

alternate_sel = tk.IntVar()
tk.Checkbutton(filters_frame, text='Only alternate arts AND op-', variable=alternate_sel, onvalue=1, offvalue=0).grid(row=10,
                                                                                                              column=2)
alternate_sel.set(0)

tk.Label(filters_frame, text="Min card cost", font=("Sans Serif", "14"), pady=20).grid(row=11, column=1)
w1 = tk.Scale(filters_frame, from_=0, to=10)
w1.grid(row=12, column=1)
tk.Label(filters_frame, text="Max card cost", font=("Sans Serif", "14"), pady=20).grid(row=11, column=2)
w2 = tk.Scale(filters_frame, from_=0, to=10)
w2.set(10)
w2.grid(row=12, column=2)

root.mainloop()
