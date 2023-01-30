# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 23:48:26 2023

@author: robrt
"""

from tkinter import *
from tkinter import ttk
import requests
import os
import multiprocessing
from time import sleep
from PIL import Image, ImageTk


# define version variable
version = "1.39"

root = Tk()
root.title("Relentless SMS Attack Script Version: {}".format(version))

# Variable to hold the number of messages to send
number_of_messages = IntVar(value=1)

# Function to validate phone number


def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    toll_free_pattern = "^\+1(800|888|877|866|855|844)[0-9]{7}$"
    if re.match(toll_free_pattern, number):
        messagebox.showerror(
            "Invalid Number", "Cannot send SMS to toll free numbers.")
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

gibberish_messages = ["Quantum flux capacitors optimize data transmission efficiency by 37%.",
                      "Neural network algorithms harness dark data for predictive analytics.",
                      "Cloud-based blockchain platforms ensure secure data storage and retrieval.",
                      "Quantum flux capacitors optimize neural network performance for maximum data synapse propulsion.",
                      "AI-powered virtual assistants enhance customer service automation.",
                      "IoT-enabled smart sensors optimize industrial automation and efficiencyACTIVE.",
                      "Neural network algorithms optimize artificial intelligence processing power.",
                      "Hyperloop transportation systems revolutionize long-distance travel.",
                      "Futuristic virtual reality interfaces enhance user immersion.",
                      "Organic microchip technology improves computing efficiency.",
                      "Nanotechnology-based cybernetic enhancements enhance human capabilities.",
                      "Subatomic particle-based data storage improves data retention.",
                      "Neuro-linguistic programming improves natural language processing.",
                      "Quantum computing algorithms solve complex optimization problems.",
                      "Molecular biology-based computer systems revolutionize data processing."]


def send_sms():
    number = phone_number_entry.get()
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return

    # Get the number of messages to send from the menu
    messages_to_send = number_of_messages.get()
    selected_speed = message_speed.get()

    # Create the progress bar widget
    progress_bar = ttk.Progressbar(
        root, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=8, column=1, padx=5, pady=5, sticky="W")
    progress_bar["maximum"] = messages_to_send
    progress_bar["value"] = 0
    # progress_bar.grid(row=8, column=1, padx=5, pady=5, sticky="W")

    for i in range(messages_to_send):
        # clear the message_entry widget before each message sent
        message_entry.delete("1.0", END)
        # insert the current gibberish message
        message_entry.insert(
            END, gibberish_messages[i % len(gibberish_messages)])
        message = message_entry.get("1.0", END)
        #new api url- textbelt is where it's at...
        url = "https://textbelt.com/text"
        #payload
        payload = {"number": number, "message": message}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            #new api key
            "X-API-Key": "da3c194dd0b6060566940bc005dd78ff379626e1gOkre7vDcXpsX4GRwrjLasJOD"
        }
        try:
            response = requests.request(
                "POST", url, data=payload, headers=headers)
            if response.status_code == 200:
                print(response.text)
            else:
                print(f'Error: {response.text}')
        except requests.exceptions.ConnectionError as e:
            print(f'Error: {e}')

        # increment the progress bar value
        progress_bar["value"] += 1
        progress_bar.update()


# Phone Number label and entry
phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Number of Messages label and menu
number_of_messages_label = Label(root, text="Number of Messages (Max 100):")
number_of_messages_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
number_of_messages = IntVar()
number_of_messages_menu = OptionMenu(root, number_of_messages, *range(1, 101))
number_of_messages_menu.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# Message label and entry
message_label = Label(root, text="Message:")
message_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

message_entry = Text(root, height=5, width=30)
message_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=W)

# Speed label and menu
speed_label = Label(root, text="Speed:")
speed_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)
speed_menu = OptionMenu(root, message_speed, "fast", "medium", "slow")
speed_menu.grid(row=3, column=1, padx=5, pady=5, sticky=W)


# # Add text box for API key
# api_key_label = Label(root, text="API Key:")
# api_key_label.grid(row=4, column=0, padx=5, pady=5, sticky=E)
# api_key_entry = Entry(root)
# api_key_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

# # Add button to save API key
# save_api_button = Button(root, text="Save API", command=save_api_key)
# save_api_button.grid(row=4, column=1, padx=5, pady=5, sticky=E)

# Send and close buttons
send_button = Button(root, text="Send", command=send_sms)
send_button.grid(row=6, column=0, padx=3, pady=3, sticky="E")

close_button = Button(root, text="Close", command=root.destroy)
close_button.grid(row=6, column=1, padx=3, pady=3, sticky="W")

test_label = Label(
    root, text="RESTRICTED INTERNAL CLASSIFIED USE ONLY", fg='gray')
test_label.grid(row=8, column=0, padx=5, pady=5, sticky="W")

# create label widget to display version
# version_label = Label(root, text="Version: " + version)

#version_label = Label(root, text="Version: {}".format(version))
# version_label.grid(row=9, column=0, padx=5, pady=5, sticky="W")


# Add the logo. Right now it sits in C:\\. I'll work on location later.
logo = PhotoImage(file="C:\\seal.png")
logo_label = Label(root, image=logo)
logo_label.grid(row=1, column=0, rowspan=7, padx=20, pady=20, sticky=W)


# Center the window on the screen on launch.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 525
height = 275
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))

root.mainloop()

# https://textbelt.com/purchase/?generateKey=1 will get you the API Key
# and you can pay there also. Replace the API key up above with your own.