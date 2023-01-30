# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 12:24:22 2023

@author: robrt
"""

from tkinter import *
from tkinter import ttk
import requests
import re
# import phonenumbers

root = Tk()
root.title("Relentless SMS")

# Variable to hold the number of messages to send
number_of_messages = IntVar(value=1)

def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    toll_free_pattern = "^\+1(800|888|877|866|855|844)[0-9]{7}$"
    if re.match(toll_free_pattern, number):
        messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
        return False
    return True


# Function to send SMS
def send_sms():
    number = phone_number_entry.get()
    message = message_entry.get("1.0", END)
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return

    # Get the number of messages to send from the menu
    messages_to_send = number_of_messages.get()
    
    # Create the progress bar widget
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=5, column=1, padx=10, pady=10)
    progress_bar["maximum"] = messages_to_send
    progress_bar["value"] = 0



        
# increment the progress bar value
# progress_bar["value"] += 1
# progress_bar.update()


# Phone Number label and entry
phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=10, pady=10)

# Number of Messages label and menu
number_of_messages_label = Label(root, text="Number of Messages (Max 100):")
number_of_messages_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
number_of_messages = IntVar()
number_of_messages_menu = OptionMenu(root, number_of_messages, *range(1,101))
number_of_messages_menu.grid(row=1, column=1, padx=10, pady=10)

# Message label and entry
message_label = Label(root, text="Message:")
message_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

message_entry = Text(root, height=10, width=40)
message_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)


# Send and close buttons
send_button = Button(root, text="Send", command=send_sms)
send_button.grid(row=4, column=0, padx=10, pady=10)

close_button = Button(root, text="Close", command=root.destroy)
close_button.grid(row=4, column=1, padx=10, pady=10)

test_label = Label(root, text="RESTRICTED INTERNAL CLASSIFIED USE ONLY", fg='gray')
test_label.grid(row=5, column=1, padx=10, pady=10)


# Center the window on the screen on launch.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 500
height = 380
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))

root.mainloop()