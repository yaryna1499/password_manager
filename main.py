from tkinter import *
from tkinter import messagebox
import re
import random
import pyperclip
import json
from PIL import Image, ImageTk


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                    [random.choice(symbols) for _ in range(nr_symbols)] + \
                    [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)
    entry_password.insert(0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    valid = validation(website, email, password)

    if valid is True:

        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
                entry_website.delete(0, END)
                entry_password.delete(0, END)



def validation(website, email, password):
    # Website
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please, don`t leave any field empty.")
        return False

    # Email
    elif not re.match("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email):
        messagebox.showinfo(title="Oops!", message="Please, enter the valid email.")
        return False

    # Password
    elif len(password) < 8:
        messagebox.showinfo(title="Oops!", message="Password should be 8 or more characters length!")
        return False

    else:
        return True


def search():
    website = entry_website.get()
    try:
        with open("data.json", "r") as data_file:
            data_dict = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="Not found!")
    else:
        for (key, value) in data_dict.items() :
            if key == website:
                messagebox.showinfo(title=f"{website}", message=f"Email: {data_dict[website]['email']}\n"
                                                                f"Password: {data_dict[website]['password']}")
    finally:
        entry_website.delete(0, END)
        entry_password.delete(0, END)





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, background="#F2EBE9")

canvas = Canvas(width=200, height=200, bg="#F2EBE9", highlightthickness=0)
logo_img = ImageTk.PhotoImage(file="logo5.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels

label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

label_email = Label(text="Email/Username:")
label_email.grid(column=0, row=2)

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

# Entries

entry_website = Entry(width=35)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_email = Entry(width=35)
entry_email.grid(column=1, row=2)
entry_email.insert(0, string="test@gmail.com")

entry_password = Entry(width=35, show="*")
entry_password.grid(column=1, row=3)


# Checkbutton
def show_password():
    if checked_state.get():
        entry_password["show"] = ""
    else:
        entry_password["show"] = "*"


checked_state = BooleanVar(value=False)
show_pass_checkbox = Checkbutton(text="Show password", onvalue=True, offvalue=False,
                                 variable=checked_state, command=show_password)
show_pass_checkbox.grid(column=4, row=3)

# Buttons

generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(column=2, row=3)

add_button = Button(text="Add", width=33, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1)

window.mainloop()
