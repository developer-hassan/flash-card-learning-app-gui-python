# Import required libraries to access their functionalities
import tkinter as tk
import pandas as pd
import random

# Constant set for the background color
BACKGROUND_COLOR = "#B1DDC6"

# Some global variables to be modified within the program
random_word = None
timer = None
words_data = None

# ---------------------------- EXTRACT DATA ------------------------------- #

# Try to use the words which are unknown yet from the csv file
try:
    words_data = pd.read_csv("./data/words_to_learn.csv")
# If the file does not exists (its the first run of program)
except FileNotFoundError:
    # Keep the whole list of words as initial input of data
    words_data = pd.read_csv("./data/french_words.csv")
except pd.errors.EmptyDataError:
    words_data = []
finally:
    # Convert the dataframe to dictionary
    try:
        words_data = words_data.to_dict(orient="records")
    except AttributeError:
        pass


# ---------------------------- Cards Functionality ------------------------------- #

def remove_word():
    """
    Removes the known words from the global dictionary and display the next card.
    """
    if len(words_data) == 0:
        return
    words_data.remove(random_word)
    next_card()


def next_card():
    """ 
    Picks up random word from the words that are unkown yet and display the word card.
    Shows the English translation of that word after three seconds.
    """
    # If all the current words become known
    if len(words_data) == 0:
        # Display the success message to the user and return
        success_message()
        return

    global random_word, timer
    if timer:
        window.after_cancel(timer)

    random_word = random.choice(words_data)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_word["French"], fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    """
    Flips the card to its back side to see the english translation of current card.
    """
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=random_word["English"])


def success_message():
    """
    Generates the success message to the user if there are no more words to learn in the words dictionary.
    """
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(card_title, text="You are all caught up!", fill="black")
    canvas.itemconfig(card_word, text="Success!", fill="black")
    canvas.create_text(
        400, 400, text="Note: Remove 'words_to_learn.csv' to begin again!")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_image = tk.PhotoImage(file="./images/card_front.png")
card_back_image = tk.PhotoImage(file="./images/card_back.png")

canvas = tk.Canvas(width=800, height=526,
                   bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(
    400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(
    400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = tk.PhotoImage(file="./images/wrong.png")
wrong_button = tk.Button(
    image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_image = tk.PhotoImage(file="./images/right.png")
right_button = tk.Button(
    image=right_image, highlightthickness=0, command=remove_word)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()

# After the closure of program, new csv file will be created with the updated words to be learned
if len(words_data) > 0:
    pd.DataFrame(words_data).to_csv("./data/words_to_learn.csv", index=False)
