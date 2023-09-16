from tkinter import *
from tkinter import messagebox
import random
from pyperclip import copy
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_dict = {website: {"Username": username, "Password": password}}

    if len(website_entry.get()) == 0 or len(username_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:

        try:
            with open("passwords.json", mode="r") as passwords:
                data = json.load(passwords)
                data.update(new_dict)

        except FileNotFoundError:
            with open("passwords.json", "w") as passwords:
                json.dump(new_dict, passwords, indent=4)

        except json.decoder.JSONDecodeError:
            with open("passwords.json", "w") as passwords:
                json.dump(new_dict, passwords, indent=4)

        else:
            with open("passwords.json", "w") as passwords:
                json.dump(data, passwords, indent=4)

        finally:
            website_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- SEARCHING FOR PASSWORDS ------------------------------- #


def search():

    try:
        with open("passwords.json", mode="r") as passwords:
            data = json.load(passwords)
            username = data[website_entry.get()]["Username"]
            password = data[website_entry.get()]["Password"]
            messagebox.showinfo(title=f"{website_entry.get()}", message=f"Username: {username}\nPassword: {password}")
            copy(password)

    except KeyError:
        messagebox.showerror(title="Error", message="Website not found.")

    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Error", message="Website not found.")

    finally:
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)

logo = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:",)
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky=EW)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky=EW)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky=EW)

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, columnspan=2, sticky=EW)

pass_generator_button = Button(text="Generate Password", command=generate_password)
pass_generator_button.grid(column=2, row=3, sticky=EW)

add_button = Button(text="Add", width=50, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
