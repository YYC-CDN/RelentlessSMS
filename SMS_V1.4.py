# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:34:04 2023

@author: robrt
"""
import http.client
import requests
from tkinter import *

def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    if number.startswith("+1800") or number.startswith("+1888"):
        messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
        return False
    return True

# def is_valid_number(number):
#     if len(number) != 10:
#         return False
#     if number[:3] in ["800", "888", "877", "866"]:
#         messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
#         return False
#     return True


def send_sms():
    # get the phone number and message from the input fields
    number = phone_number_entry.get()
    message = message_entry.get("1.0", END)
    # validate the phone number
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return

url = "https://messagebird-sms-gateway.p.rapidapi.com/sms"

querystring = {"password":"Joyt1967","username":"MrBungle"}

payload = "dlr_url=http%3A%2F%2Fwww.example.com%2Fdlr-messagebird.php&type=flash&replacechars=checked&timestamp=201308020025&reference=268431687&destination=31600000001%2C31600000002&body=This%20is%20a%20gsm%207-bit%20test%20message.&sender=MessageBird"
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": "8f4ed3dbefmsh6c297754b87116fp1e0a0ajsndba965364040",
	"X-RapidAPI-Host": "messagebird-sms-gateway.p.rapidapi.com"
}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)


def stop_sending():
    # stop sending the messages
    pass

def close_script():
    # close the script
    root.destroy()

root = Tk()
root.title("Send SMS")

phone_number_label = Label(root, text="Phone Number:")
phone_number_label.grid(row=0, column=0, padx=10, pady=10)

phone_number_entry = Entry(root)
phone_number_entry.grid(row=0, column=1, padx=10, pady=10)

message_label = Label(root, text="Message:")
message_label.grid(row=1, column=0, padx=10, pady=10)

message_entry = Text(root, height=10, width=40)
message_entry.grid(row=1, column=1, padx=10, pady=10)

send_button = Button(root, text="Send", command=send_sms)
send_button.grid(row=2, column=0, padx=10, pady=10)

stop_button = Button(root, text="Stop", command=stop_sending)
stop_button.grid(row=2, column=1, padx=10, pady=10)

close_button = Button(root, text="Close", command=close_script)
close_button.grid(row=2, column=2, padx=10, pady=10)

root.mainloop()


