# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 22:21:09 2023

@author: robrt
"""
import requests
from tkinter import *
from tkinter import ttk


root = Tk()
root.title("Rapid SMS")

# Variable to hold the number of messages to send
number_of_messages = IntVar(value=1)

# Update the send_sms function to include the validation for number of messages
def send_sms():
    number = phone_number_entry.get()
    message = message_entry.get("1.0", END)
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return
    if not validate_messages(number_of_messages.get()):
        return

# Function to send SMS

    # Get the number of messages to send from the menu
    messages_to_send = number_of_messages.get()
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
            
            # Function to validate number of messages
def validate_messages(messages):
    if messages > 10:
        messagebox.showerror("Invalid Number of Messages", "Cannot send more than 10 messages.")
        return False
    return True


# Number of Messages label and menu
number_of_messages_label = Label(root, text="Number of Messages:")
number_of_messages_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
number_of_messages = IntVar()
number_of_messages_menu = OptionMenu(root, number_of_messages, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
number_of_messages_menu.grid(row=1, column=1, padx=10, pady=10)

# Message to display at bottom of GUI
test_software_label = Label(root, text="This is test software only")
test_software_label.grid(row=5, column=1, padx=10, pady=10)



# Phone Number label and entry
phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=10, pady=10)

# Number of Messages label and menu
number_of_messages_label = Label(root, text="Number of Messages:")
number_of_messages_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
number_of_messages = IntVar()
number_of_messages_menu = OptionMenu(root, number_of_messages, 1, 2, 3, 4, 5)
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


root.mainloop()