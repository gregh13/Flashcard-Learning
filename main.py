from tkinter import *
from tkinter import messagebox
import random
import json


FC1_COLOR = "#80B79F"
FC2_COLOR = "white"
ENGLISH = "English"

try:
    with open("thai_eng_revised.json") as dict_file:
        j_dict = json.load(dict_file)
except FileNotFoundError:
    with open("thai_eng.json") as dict_file:
        j_dict = json.load(dict_file)
    with open("thai_eng_revised.json", mode="w") as dict_file:
        json.dump(j_dict, dict_file, indent=4)

THAI_DICTIONARY = {}
for dict in j_dict:
    THAI_DICTIONARY[dict['Thai']] = dict['English']

# ENG_THAI_PRACTICE_DICTIONARY = {value:key for (key, value) in THAI_DICTIONARY.items()}

STUDY_WORD_SIZE = 70
ANSWER_WORD_SIZE = 60
LANGUAGE = "Thai"
DICTIONARY_MASTER = THAI_DICTIONARY
DICTIONARY = DICTIONARY_MASTER
DICTIONARY_LIST = (list(DICTIONARY))

# You can change the look/feel and content of the app. For example:
# STUDY_WORD_SIZE = 30
# ANSWER_WORD_SIZE = 30
# LANGUAGE = "Hungarian"
# DICTIONARY_MASTER = Hungarian_English_dict
# DICTIONARY = DICTIONARY_MASTER
# DICTIONARY_LIST = (list(DICTIONARY))

used_cards = []
revision_list = []


# ------------ Right or Wrong ------------ #
def successful():
    if flash_card_text.cget("text") == "Study Time!":
        pass
    else:
        flash_card_text.config(text="Great Job! 😁", font=("Courier", 40, "bold"))
        card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
        root.after(1000, new_card)


def revision():
    try:
        card = flash_card_text.cget("text")
        revision_list.append({card:DICTIONARY[card]})
    except KeyError:
        try:
            card = flash_card_text.cget("text")
            study_card = list(DICTIONARY.keys())[list(DICTIONARY.values()).index(card)]
            revision_list.append({study_card: DICTIONARY[study_card]})
        except ValueError:
            pass
        else:
            card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
            flash_card_text.config(text="Don't sweat it 💪", font=("Courier", 40, "bold"))
            root.after(1000, new_card)
    else:
        card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
        flash_card_text.config(text="Don't sweat it 💪", font=("Courier", 40, "bold"))
        root.after(1000, new_card)


# --------- Revision List Practice ------------ #
def change_dictionary():
    global DICTIONARY, DICTIONARY_LIST, used_cards
    if used_cards == 0:
        pass
    elif messagebox.askokcancel(title="Focused Practice",
                                message="Click 'OK' to change flashcards\nto just the ones you missed"
                                        "\n\nClick 'Cancel' to continue with the current set of cards"):
        new_dict = {}
        for item in revision_list:
            new_dict.update(item)
        DICTIONARY = new_dict
        DICTIONARY_LIST = (list(DICTIONARY))
        reset_cards()
        start_button.config(text="START", width=5, highlightthickness=0, command=start_game)
    else:
        pass


# -------------- Card Mechanics ------------ #
def start_game():
    if len(used_cards) == 0:
        def pick_card():
            card = random.choice(DICTIONARY_LIST)
            return card
        card = pick_card()
        used_cards.append(card)
        card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
        flash_card_text.config(text=card,  font=("Courier", STUDY_WORD_SIZE, "bold"), fg="white")
        start_button.config(text="'Needs Revision' Cards", width=22, command=change_dictionary)
        root.after(400, None)
    else:
        pass


def new_card():
    def pick_card():
        card = random.choice(DICTIONARY_LIST)
        return card

    if len(used_cards) >= len(DICTIONARY_LIST) and len(revision_list) == 0:
        messagebox.showinfo(title="Woohoo!", message="You're a superstar!\n\nThere are no more cards to review!!")
        reset_cards()
    elif len(used_cards) >= len(DICTIONARY_LIST):
        change_dictionary()
    else:
        card = pick_card()
        if card in used_cards:
            new_card()
        else:
            used_cards.append(card)
            card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
            flash_card_text.config(text=card,  font=("Courier", STUDY_WORD_SIZE, "bold"))
            canvas.itemconfig(flash_card_background, image=card_question_img)
            flash_card_text.config(bg=FC1_COLOR, fg="white")


def flip_to_answer():
    try:
        card = flash_card_text.cget("text")
        flash_card_text.config(text=DICTIONARY[card], font=("Courier", ANSWER_WORD_SIZE, "bold"))
        canvas.itemconfig(flash_card_background, image=card_answer_img)
        flash_card_text.config(bg=FC2_COLOR, fg="black")
    except KeyError:
        pass


def flip_back():
    try:
        card = flash_card_text.cget("text")
        study_card = list(DICTIONARY.keys())[list(DICTIONARY.values()).index(card)]
        canvas.itemconfig(flash_card_background, image=card_question_img)
        flash_card_text.config(bg=FC1_COLOR, fg="white", text=study_card, font=("Courier", STUDY_WORD_SIZE, "bold"))
    except ValueError:
        pass


def reset_cards():
    global used_cards, revision_list
    used_cards = []
    revision_list = []
    canvas.itemconfig(flash_card_background, image=card_question_img)
    flash_card_text.config(bg=FC1_COLOR, fg="white")
    card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
    start_button.config(text="START", width=5, highlightthickness=0, command=start_game)
    flash_card_text.config(text="Study Time!", font=("Courier", 60, "bold"))


def reset_cards_to_start():
    global used_cards, revision_list, DICTIONARY_LIST, DICTIONARY
    used_cards = []
    revision_list = []
    canvas.itemconfig(flash_card_background, image=card_question_img)
    flash_card_text.config(bg=FC1_COLOR, fg="white")
    DICTIONARY = DICTIONARY_MASTER
    DICTIONARY_LIST = (list(DICTIONARY))
    card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
    start_button.config(text="START", width=5, highlightthickness=0, command=start_game)
    flash_card_text.config(text="Study Time!", font=("Courier", 60, "bold"))


def delete_card():
    try:
        card = flash_card_text.cget("text")
        DICTIONARY_MASTER.pop(card)
        DICTIONARY_LIST.remove(card)
        used_cards.remove(card)
        try:
            with open("thai_eng_revised.json", mode="r") as file:
                obj = json.load(file)
                for i in range(len(obj)):
                    if obj[i]["Thai"] == card:
                        obj.pop(i)
                        break
        except:
            with open("thai_eng.json", mode="r") as file:
                obj = json.load(file)
                for i in range(len(obj)):
                    if obj[i]["Thai"] == card:
                        obj.pop(i)
                        break
        with open("thai_eng_revised.json", mode="w") as file:
            json.dump(obj, file, indent=4)
    except KeyError:
        try:
            card = flash_card_text.cget("text")
            study_card = list(DICTIONARY.keys())[list(DICTIONARY.values()).index(card)]
            DICTIONARY_MASTER.pop(study_card)
            DICTIONARY_LIST.remove(study_card)
            used_cards.remove(study_card)
            with open("thai_eng_revised.json", mode="r") as file:
                obj = json.load(file)
                for i in range(len(obj)):
                    if obj[i]["English"] == card:
                        obj.pop(i)
                        break
            with open("thai_eng_revised.json", mode="w") as file:
                json.dump(obj, file, indent=4)
        except ValueError:
            print("error")
        else:
            card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
            root.after(1, new_card)
    else:
        card_score.config(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}")
        root.after(1, new_card)


# -------------- UI Setup ------------ #
root = Tk()
root.title("Learn English!")
root.minsize(600, 400)
root.config(padx=75, pady=30)

card_question_img = PhotoImage(file="card_back.png")
card_answer_img = PhotoImage(file="card_front.png")

canvas = Canvas(width=550, height=362)
flash_card_background = canvas.create_image(275, 181, image=card_question_img)
canvas.grid(columnspan=5, column=0, row=2)

flash_card_text = Label(text="Study Time!", fg="white", bg=FC1_COLOR, font=("Courier", 60, "bold"), pady=15)
flash_card_text.grid(columnspan=5, column=0, row=2)

filler_row = Label()
filler_row.grid(column=2, row=3)
filler_row = Label()
filler_row.grid(column=2, row=1)
filler_row = Label(pady=8)
filler_row.grid(column=2, row=5)

card_score = Label(text=f"Card: {len(used_cards)}/{len(DICTIONARY)}", font=("Courier", 20, "bold"), pady=10)
card_score.grid(sticky="N", column=2, row=3)
flip_english_button = Button(text="** Flip to Answer **", width=15, highlightthickness=0, command=flip_to_answer)
flip_english_button.grid(column=2, row=6)
flip_thai_button = Button(text="Flip Back", width=8, highlightthickness=0, command=flip_back)
flip_thai_button.grid(column=2, row=5)
start_button = Button(text="START", width=5, highlightthickness=0, command=start_game)
start_button.grid(sticky="S", column=2, row=4)

reset_button = Button(text="Reset Current Card Set", width=15, highlightthickness=0, command=reset_cards)
reset_button.grid(columnspan=2, column=0, row=0)
reset_button = Button(text="Reset Everything", width=15, highlightthickness=0, command=reset_cards_to_start)
reset_button.grid(columnspan=2, column=3, row=0)
delete_card_button = Button(text="Delete Card Permanently", command=delete_card)
delete_card_button.grid(column=2, row=0)

red_x = PhotoImage(file="red_x.png")
fail_button = Button(image=red_x, bd=0, command=revision)
fail_button.grid(rowspan=4, column=1, row=3)

green_check = PhotoImage(file="greencheck.png")
success_button = Button(image=green_check, command=successful)
success_button.grid(rowspan=4, column=3, row=3)


root.mainloop()

