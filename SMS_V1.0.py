import urllib.request
import urllib.parse

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

resp =  sendSMS('apikey', '447123456789',
    'Jims Autos', 'This is your message')
print (resp)


import tkinter as tk
import urllib.request
import urllib.parse

def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

class SMS_Sender(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SMS Sender")
        self.geometry("300x200")

        self.apikey = tk.StringVar()
        self.numbers = tk.StringVar()
        self.sender = tk.StringVar()
        self.message = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Phone Number:").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.numbers).grid(row=0, column=1)

        tk.Label(self, text="Message:").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.message).grid(row=1, column=1)

        tk.Label(self, text="API Key:").grid(row=2, column=0)
        tk.Entry(self, textvariable=self.apikey).grid(row=2, column=1)

        tk.Label(self, text="Sender:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.sender).grid(row=3, column=1)

        tk.Button(self, text="Send", command=self.on_send).grid(row=4, column=0)
        tk.Button(self, text="Stop", command=self.on_stop).grid(row=4, column=1)
        tk.Button(self, text="Close", command=self.on_close).grid(row=4, column=2)

    def on_send(self):
        apikey = self.apikey.get()
        numbers = self.numbers.get()
        sender = self.sender.get()


import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse


root = tk.Tk()
root.title("SMS Sender")
root.geometry("400x300")
root.configure(bg = "white")


def is_valid_number(number):
    if len(number) != 10:
        return False
if number[:3] in ["800", "888", "877", "866"]:
    messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
return False
return True

def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
'message' : message, 'sender': sender})
data = data.encode('utf-8')
request = urllib.request.Request("https://api.txtlocal.com/send/?")
f = urllib.request.urlopen(request, data)
fr = f.read()
return(fr)


phone_label = tk.Label(root, text = "Phone Number:", bg = "black", fg = "white")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()


message_label = tk.Label(root, text = "SMS Message:", bg = "black", fg = "white")
message_label.pack()
message_entry = tk.Text(root, height = 5, width = 30)
message_entry.pack()


apikey_label = tk.Label(root, text = "API Key:", bg = "black", fg = "white")
apikey_label.pack()
apikey_entry = tk.Entry(root)
apikey_entry.pack()
def on_send():
    number = "+1" + phone_entry.get()
if not is_valid_number(number[1:]):
    return
message = message_entry.get("1.0", "end") or "This is a random gibberish message that almost makes sense."
apikey = apikey_entry.get()
if not apikey:
    messagebox.showerror("API Key Required", "Please enter a valid API key.")
return
resp = sendSMS(apikey, number, 'SMS Sender', message)
messagebox.showinfo("SMS Sent", resp)
send_button = tk.Button(root, text = "Send", command = on_send)
send_button.pack()
def on_stop():
pass
stop_button = tk.Button(root, text = "Stop", command = on_stop)
stop_button.pack()
Close