from tkinter import *
import requests

root = Tk()
root.title("Rapid SMS")

def validate_number(number):
    # add +1 for international dialing
    number = "+1" + number
    # check if the phone number is a toll-free number
    if number.startswith("+1800") or number.startswith("+1888"):
        messagebox.showerror("Invalid Number", "Cannot send SMS to toll free numbers.")
        return False
    return True

def send_sms():
    # get the phone number and message from the input fields
    number = phone_number_entry.get()
    message = message_entry.get("1.0", END)
    # validate the phone number
    if not validate_number(number):
        print("Invalid phone number. Please enter a valid number.")
        return
    #new api url- textbelt is where it's at...
    url = "https://textbelt.com/text"
    #payload
    payload = {"number": number, "message": message}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        #new api key
          "X-API-Key": "a799857430d8e5b458245f53ec160d88abff3e2cniqFM7ZmyiuGqTNW5mmFKUxWy_test"
          #"X-API-Key": "textbelt"
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f'Error: {response.text}')
    except requests.exceptions.ConnectionError as e:
        print(f'Error: {e}')

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

close_button = Button(root, text="Close", command=root.destroy)
close_button.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()

# https://textbelt.com/purchase/ for credits
# MAIN API a799857430d8e5b458245f53ec160d88abff3e2cniqFM7ZmyiuGqTNW5mmFKUxWy