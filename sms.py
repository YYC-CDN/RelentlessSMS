# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
from tkinter import messagebox
import requests

class SMS_Sender:
    def __init__(self, master):
        self.master = master
        master.title("SMS Sender")
        self.api_key = tk.StringVar()
        self.phone_number = tk.StringVar()
        self.message = tk.StringVar()
        self.sent_message_count = 0

# Phone Number
self.phone_number_label = tk.Label(master, text="Phone Number:")
self.phone_number_label.grid(row=0, column=0, padx=5, pady=5)
self.phone_number_entry = tk.Entry(master, textvariable=self.phone_number)
self.phone_number_entry.grid(row=0, column=1, padx=5, pady=5)

# API Key
self.api_key_label = tk.Label(master, text="API Key:")
self.api_key_label.grid(row=1, column=0, padx=5, pady=5)
self.api_key_entry = tk.Entry(master, textvariable=self.api_key)
self.api_key_entry.grid(row=1, column=1, padx=5, pady=5)

# Message
self.message_label = tk.Label(master, text="Message:")
self.message_label.grid(row=2, column=0, padx=5, pady=5)
self.message_entry = tk.Entry(master, textvariable=self.message)
self.message_entry.grid(row=2, column=1, padx=5, pady=5)

# Progress Bar
self.progress = tk.ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
self.progress.grid(row=3, column=1, padx=5, pady=5)

# Send Button
self.send_button = tk.Button(master, text="Send", command=self.send_sms)
self.send_button.grid(row=4, column=0, padx=5, pady=5)

# Stop Button
self.stop_button = tk.Button(master, text="Stop", command=self.stop_sending, state=tk.DISABLED)
self.stop_button.grid(row=4, column=1, padx=5, pady=5)

# Close Button
self.close_button = tk.Button(master, text="Close", command=self.master.destroy)
self.close_button.grid(row=4, column=2, padx=5, pady=5)

def validate_phone_number(self, number):
        if number[:3] in ["800", "888", "877", "866", "855", "844", "833", "822", "880", "881", "882", "883", "884", "885", "886", "887", "889"]:
            messagebox.showerror("Invalid Phone Number", "Toll free numbers are not supported.")
return False
return True

def send_sms(self):
        self.send_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.sms_status_label.config(text="Sending messages...")
        self.sms_status_label.update()
        self.phone_number = self.phone_number_entry.get()
        if self.validate_phone_number(self.phone_number):
            self.message = self.message_entry.get() or " ".join(random.sample(self.gibberish_words, 160))
self.api_key = self.api_key_entry.get()
     self.num_of_messages = int(self.num_of_messages_dropdown.get())
self.speed = self.speed_dropdown.get()
if self.speed == "Slow":
    self.speed = 60
elif self.speed == "Medium":
    self.speed = 30
else:
    self.speed = 1
sent_count = 0
for i in range(self.num_of_messages):
    if not self.stop_event.is_set():
        try:
            self.session.post("https://api.smsmode.com/sms/send", json={
                "message": self.message,
                "numero": self.phone_number,
                "key": self.api_key
            })
            sent_count += 1
            self.progress_bar["value"] = sent_count
            self.progress_bar.update()
            time.sleep(self.speed)
        except:
            messagebox.showerror("Error", "An error occurred while sending the message.")
            self.stop_sms()
            return
    else:
        self.stop_event.clear()
        self.sms_status_label.config(text="Messages stopped.")
        self.send_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        return
self.sms_status_label.config(text="Messages sent.")
self.send_button.config(state=NORMAL)
self.stop_button.config(state=DISABLED)


root = tk()
app = SMSMessenger(root)
root.mainloop()