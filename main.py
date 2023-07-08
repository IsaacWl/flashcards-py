from tkinter import *
import pandas
import os
import random
# --------------- CONSTANTS ----------------
BACKGROUND_COLOR = "#B1DDC6"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# --------------- GLOBAL VARIABLES ------------
to_learn = {}
random_word = {}

# try read file if exist else read original
try:
    data = pandas.read_csv(f"{DIR_PATH}/data/to_learn.csv")
except:
    original_data = pandas.read_csv(f"{DIR_PATH}/data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global random_word, flip_timer
    window.after_cancel(flip_timer)
    random_word = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(canvas_title, text="French", fill="#999999")
    canvas.itemconfig(canvas_word, text=random_word["French"], fill="#999999")
    flip_timer = window.after(4000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(canvas_title, text="English", fill="#ffffff")
    canvas.itemconfig(canvas_word, text=random_word["English"], fill="#ffffff")


def is_known():
    to_learn.remove(random_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv(f"{DIR_PATH}/data/to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Studies")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(4000, func=flip_card)

canvas = Canvas(width=800, height=526)

card_front = PhotoImage(file=f"{DIR_PATH}/images/card_front.png")
card_back = PhotoImage(file=f"{DIR_PATH}/images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=card_front)


canvas_title = canvas.create_text((400, 150), text="", font=(
    "Arial", 48, "italic")
)
canvas_word = canvas.create_text(
    400, 263, text="", font=("Arial", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

unknown_image = PhotoImage(file=f"{DIR_PATH}/images/wrong.png")
unknown_button = Button(image=unknown_image,
                        highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_image = PhotoImage(file=f"{DIR_PATH}/images/right.png")
known_button = Button(
    image=known_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
