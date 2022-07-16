import csv
from tkinter import *
from random import *
import pandas

current_card = {}
BACKGROUND_COLOR = "#B1DDC6"

try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df_old = pandas.read_csv("data/flash-card-th-da.csv")
    data = df_old.to_dict(orient="records")
else:
    data = df.to_dict(orient="records")


def remove_card():
    global data
    data.remove(current_card)
    new_df = pandas.DataFrame.from_dict(data)
    new_df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(data)
    canvas.itemconfig(card_title, text="Thailandsk", fill="black")
    canvas.itemconfig(card_word, text=current_card['Thai'], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Dansk", fill="white")
    canvas.itemconfig(card_word, text=current_card['Danish'], fill="white")
    canvas.itemconfig(canvas_image, image=card_back)


window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR, width=800, height=526)

flip_timer = window.after(3000, func=flip_card)

# --- Card front --- #
canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

# --- Language --- #
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))

# --- Word --- #
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# --- Yes button --- #
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, border=0, command=remove_card)
right_button.grid(row=1, column=0)

# --- No button --- #
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0, command=next_card)
wrong_button.grid(row=1, column=1)

next_card()

window.mainloop()
