# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 13:19:27 2023

@author: robrt
"""

from tkinter import *
from tkinter import ttk
import requests
import re
from tkinter import messagebox

root = Tk()
root.title("Relentless SMS")

# Set the theme for the GUI
style = ttk.Style()
style.theme_use('clam')

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

    for i in range(messages_to_send):
        #new api url- textbelt is where it's at...
        url = "https://textbelt.com/text"
        #payload
        payload = {"number": number, "message": message}
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            #new api key
            #   "X-API-Key": "a799857430d8e5b458245f53ec160d88abff3e2cniqFM7ZmyiuGqTNW5mmFKUxWy"
            # TEST KEY 
            "X-API-Key": "1910cb718cb6650e125cfe3ca6ac5356c3da13cede9dy6oCJRNVOODO1BvdAR0ks_test"
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


# Phone Number
# increment the progress bar value
progress_bar["value"] += 1
progress_bar.update()

# do some other task
time.sleep(0.1)

# check if the progress bar has reached its maximum value
if progress_bar["value"] >= progress_bar["maximum"]:
    # if yes, close the progress bar
    progress_bar.destroy()
    print("Task completed!")
