# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 18:25:16 2023

@author: robrt
"""

from tkinter import *
from tkinter import ttk
import requests
from time import sleep
root = Tk()
root.title("Relentless SMS")

# Variable to hold the number of messages to send
number_of_messages = IntVar(value=1)

# Function to save the user's API key
def save_api_key():
    key = api_key_entry.get()
    api_key.set(key)
    api_key_entry.delete(0, END)
    print(f'API key saved: {key}')

# Function to validate phone number
def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    toll_free_pattern = "^\+1(800|888|877|866|855|844)[0-9]{7}$"
    if re.match(toll_free_pattern, number):
        messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
        return False
    return True

#only 160 characters allowed n the main text window.
    def check_length(event):
        message = message_entry.get(1.0, END)
        if len(message) > 160:
            message_entry.delete(161, END)
    
    message_entry.bind('<KeyRelease>', check_length)


# Variable to hold the speed of messages
message_speed = StringVar(value="medium")

# Function to send SMS
def send_sms():
    number = phone_number_entry.get()
    message = message_entry.get("1.0", END)
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return

    # Get the number of messages to send from the menu
    messages_to_send = number_of_messages.get()
    selected_speed = message_speed.get()

    # Create the progress bar widget
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=5, column=1, padx=5, pady=5)
    progress_bar["maximum"] = messages_to_send
    progress_bar["value"] = 0
    progress_bar.grid(row=5, column=1, padx=5, pady=5, sticky="W")

    for i in range(messages_to_send):
        #new api url- textbelt is where it's at...
        url = "https://textbelt.com/text"
        #payload
        payload = {"number": number, "message": message}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            #new api key
            "X-API-Key": api_key.get()
        }
        try:
            response = requests.request("POST", url, data=payload, headers=headers)
            if response.status_code == 200:
                print(response.text)
            else:
                print(f'Error: {response.text}')
        except requests.exceptions.ConnectionError as e:
            print(f'Error: {e}')
        
        # increment the progress bar value
        progress_bar["value"] += 1
        progress_bar.update()

        # Sleep for different amounts of time based on selected speed
        if selected_speed == "fast":
            sleep(5)
        elif selected_speed == "medium":
            sleep(30)
        else:
            sleep(60)


# Speed label and menu
speed_label = Label(root, text="Speed:")
speed_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)
speed_menu = OptionMenu(root, message_speed, "fast", "medium", "slow")
speed_menu.grid(row=3, column=1, padx=5, pady=5, sticky=W)
                
# Phone Number label and entry
phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Number of Messages label and menu
number_of_messages_label = Label(root, text="Number of Messages (Max 100):")
number_of_messages_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
number_of_messages = IntVar()
number_of_messages_menu = OptionMenu(root, number_of_messages, *range(1,101))
number_of_messages_menu.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# Message label and entry
message_label = Label(root, text="Message:")
message_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

message_entry = Text(root, height=5, width=30)
message_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=W)


# Send and close buttons
send_button = Button(root, text="Send", command=send_sms)
send_button.grid(row=4, column=0, padx=10, pady=10, sticky="E")

# Send and close buttons
save_api_ke_button = Button(root, text="SaveAPI", command=save_api_key())
save_api_ke_button.grid(row=6, column=0, padx=10, pady=10, sticky="EW")

close_button = Button(root, text="Close", command=root.destroy)
close_button.grid(row=4, column=1, padx=10, pady=10, sticky="W")

test_label = Label(root, text="RESTRICTED INTERNAL CLASSIFIED USE ONLY", fg='gray')
test_label.grid(row=8, column=0, padx=5, pady=5, sticky="W")

# Center the window on the screen on launch.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 525
height = 285
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))

root.mainloop()
