from tkinter import *
from tkinter import messagebox
import re
import random
import pyperclip


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

    valid = validation(website, email, password)

    if valid == True:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"The info you entered\nEmail:{email}\npassword:{password}"
                                               f"\n Is it ok?")
        if is_ok:
            data_file = open("passwd.txt", "a")
            data_file.write(f"{website}|{email}|{password}\n")
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            data_file.close()


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


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=2, row=1)

# Labels

label_website = Label(text="Website:")
label_website.grid(column=1, row=2)

label_email = Label(text="Email/Username:")
label_email.grid(column=1, row=3)

label_password = Label(text="Password:")
label_password.grid(column=1, row=4)

# Entries

entry_website = Entry(width=35)
entry_website.grid(column=2, row=2, columnspan=2)
entry_website.focus()

entry_email = Entry(width=35)
entry_email.grid(column=2, row=3, columnspan=2)
entry_email.insert(0, string="test@gmail.com")

entry_password = Entry(width=24, show="*")
entry_password.grid(column=2, row=4)


# Checkbutton
def show_password():
    if checked_state.get():
        entry_password["show"] = ""
    else:
        entry_password["show"] = "*"


checked_state = BooleanVar(value=False)
show_pass_checkbox = Checkbutton(text="Show password", onvalue=True, offvalue=False,
                                 variable=checked_state, command=show_password)
show_pass_checkbox.grid(column=4, row=4)

# Buttons

generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(column=3, row=4)

add_button = Button(text="Add", width=33, command=save_data)
add_button.grid(column=2, row=5, columnspan=2)

window.mainloop()
