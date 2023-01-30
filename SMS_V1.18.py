# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 23:46:08 2023

@author: robrt
"""

from tkinter import *
from tkinter import ttk
import requests

root = Tk()
root.title("Rapid SMS")

# Variable to hold the number of messages to send
number_of_messages = IntVar(value=1)

# Function to validate phone number
def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    if number.startswith("+1800") or number.startswith("+1888"):
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
            "X-API-Key": "a799857430d8e5b458245f53ec160d88abff3e2cniqFM7ZmyiuGqTNW5mmFKUxWy_test"
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
        
        

# Phone Number label and entry
phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=10, pady=10)

# Send and close buttons
send_button = Button(root, text="Send", command=send_sms)
send_button.grid(row=4, column=0, padx=10, pady=10)



#create a quit button
quit_button = Button(root, text="Quit", command=root.quit)
quit_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=108)

close_button = Button(root, text="Close", command=root.destroy)
close_button.grid(row=4, column=1, padx=10, pady=10)

test_label = Label(root, text="RESTRICTED This is test software only", fg='gray')
test_label.grid(row=5, column=1, padx=10, pady=10)

root.mainloop()

