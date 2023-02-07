# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 22:10:54 2023

@author: robrt
"""

from tkinter import *
import requests
import re
import time
import threading
import socket
from tkinter import messagebox
from tkinter import ttk

version = "1.73 BETA"
root = Tk()
root.title("Relentless SMS® V{}".format(version))
root.attributes("-topmost", True)

number_of_messages = IntVar(value=1)
test_mode = IntVar(value=0)

def validate_number(number):
    number = "+1" + number
    toll_free_pattern = "^\+1(800|888|877|866|855|844|833)[0-9]{7}$"
    if re.match(toll_free_pattern, number):
        messagebox.showerror("Oopsies", "Cannot send SMS to toll free numbers, man. Don't waste the API cost. 💀")
        return False
    return True


def is_connected():
    try:
        # Check if we can connect to the internet using Google DNS (8.8.8.8)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def send_sms():
    if not is_connected():
        messagebox.showerror("No internet connection", "Please check your internet connection and try again.")
        return
    number = phone_number_entry.get()
    if not validate_number(number):
        messagebox.messagebox.showerror("Invalid phone number. Please enter a valid number.")
        return

    messages_to_send = number_of_messages.get()
    wait_time = int(speed_entry.get())
    if wait_time > 900:
        messagebox.showerror("Oopsies" , "1000 seconds is 16.66 minutes. Max is 900, or one message every 15 minutes. ")
        return

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=225, mode='determinate')
    progress_bar.grid(row=8, column=1, padx=5, pady=5, sticky="W")
    progress_bar["maximum"] = messages_to_send
    progress_bar["value"] = 0

    for i in range(messages_to_send):
        root.update()
        message_entry.delete("1.0", END)
        message_entry.insert(END, gibberish_messages[i % len(gibberish_messages)])
        message = message_entry.get("1.0", END)

        if test_mode.get() == 1:
            # This API MUST have _test at the end, before the end quote.
            api_key = "<YOUR-API-HERE>_test"
        else:
            # This is the regular API WItHOUT the _test at the end.
            api_key = "<YOUR-API-HERE>"

        url = "https://textbelt.com/text"
        payload = {
            "phone": number,
            "message": message,
            "key": api_key,
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("SMS sent successfully.")
        else:
            messagebox.showerror(f"Failed to send SMS: {response.text}")

        progress_bar["value"] += 1

        root.update_idletasks()
        root.update()
        time.sleep(wait_time)
        # messagebox.showinfo("Relentless SMS®", "SMS sent successfully.")

    time.sleep(0.1)
#show a messagebox indicating that all messages have been sent
    messagebox.showinfo("Relentless SMS", "All messages have been sent.")


    # Get account balance
url = "https://textbelt.com/quota/<YOUR-API-HERE>"
response = requests.get(url)
balance = response.json().get("quotaRemaining", 0)
account_balance_label = Label(root, text=f"Remaining in Account: {balance}", fg='gray', font=("Segoe UI", 10))
account_balance_label.grid(row=1, column=1, padx=40, pady=0, sticky="W")
# root.after(1000, update_balance) # call the function every 1000 milliseconds



# def update_balance():
#     url = "https://textbelt.com/quota/<YOUR-API-HERE>"
#     response = requests.get(url)
#     balance = response.json().get("quotaRemaining", 0)
#     account_balance_label["text"] = f"Remaining in Account: {balance}"
#     root.after(1000, update_balance) # call the function every 1000 milliseconds (1 second)

# Get account balance and start the loop
# update_balance()



# Phone Number label and entry
phone_number_label = Label(root, text="Send to Phone Number:", font=("Segoe UI", 10))
phone_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)
phone_number_entry = Entry(root, font=("Segoe UI", 10), validate='key', validatecommand=(root.register(lambda x: x.isdigit() and len(x) <= 10), '%P'))
phone_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Number of Messages label and text box
number_of_messages_label = Label(root, text="Number of Messages:", font=("Segoe UI", 10))
number_of_messages_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)

number_of_messages = IntVar()
number_of_messages_entry = Entry(root, textvariable=number_of_messages, width=5)
number_of_messages_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

def validate_number_of_messages():
    if number_of_messages.get() > 500:
        messagebox.showerror("Error", "Number of messages cannot be over 500 at this time- remember these aren't free & this API costs money.")

number_of_messages_entry.bind("<FocusOut>", validate_number_of_messages)

# Message label and entry
message_label = Label(root, text="Auto Message:", font=("Segoe UI", 10))
message_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

message_entry = Text(root, height=5, width=30, font=("Segoe UI", 10), wrap=WORD)
message_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=W)



#MESSAGE SPEED
speed_label = Label(root, text="Seconds Between:", font=("Segoe UI", 10))
speed_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)

message_speed = IntVar()
speed_entry = Entry(root, textvariable=message_speed, width=5, font=("Segoe UI", 10))
speed_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)


def pause_script():
    global is_paused
    is_paused = True

pause_button = Button(root, text="Pause", command=pause_script, font=("Segoe UI", 10))
pause_button.grid(row=6, column=1, padx=3, pady=3, sticky=W)

# close_button = Button(root, text="Close", command=root.destroy, font=("Segoe UI", 10))
# close_button.grid(row=6, column=2, padx=3, pady=3, sticky="W")

# Send and close buttons
send_button = Button(root, text="Send", command=send_sms, font=("Segoe UI", 10), bg="firebrick")
send_button.grid(row=6, column=0, padx=3, pady=3, sticky="E")

# Checkbox for test mode
test_mode = IntVar()
test_checkbox = Checkbutton(root, text="Testing Mode", variable=test_mode, font=("Segoe UI", 10))
test_checkbox.grid(row=3, column=1, padx=32, pady=0, sticky=W)

# Test mode label
test_mode_label = Label(root, text="", fg='green', font=("Segoe UI", 10, "bold"))
test_mode_label.grid(row=3, column=1, padx=135, pady=0, sticky="W")

def toggle_test_mode():
    if test_mode.get() == 1:
        test_mode_label.config(text=" ACTIVATED")
        send_button.config(bg="green", text="TEST")
    else:
        test_mode_label.config(text="")
        send_button.config(bg="firebrick", text="Send")

test_checkbox.config(command=toggle_test_mode)

#RESTRICTED VERBAGE
test_label = Label(root, text="RESTRICTED INTERNAL CLASSIFIED USE ONLY", fg='gray', font=("Segoe UI", 10))
test_label.grid(row=8, column=0, padx=5, pady=5, sticky="W")

# Add the logo. Right now it sits in C:\\. I'll work on location later.
# "C:\\logo.png" and it's 135X135px.
# Include error correction in case the image isn't there.
try:
    logo = PhotoImage(file="C:\\seal.png")
    logo_label = Label(root, image=logo)
    logo_label.grid(row=1, column=0, rowspan=7, padx=20, pady=20, sticky=W)
except:
    print("Error: Image file not found")


# Center the window on the screen on launch. ==================================
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 530
height = 270
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))


#==============================================================================
# Here's all the gibberish BS that's going to be sent. Crime is wrong
gibberish_messages = [
"Engaging in criminal behavior is a disgrace to society.",
"La participación en comportamientos criminales es una vergüenza para la sociedad.",
"从事犯罪行为是对社会的耻辱。",
"अपराधी व्यवहार में भाग लेना समाज के लिए लज्जित होता है।",
"جرمی عملیات میں شامل ہونا عوام کے لئے شرمناک ہے۔",
"잘못된 행동에 참여하는 것은 사회의 부끄러움이다.",
"Участие в преступных действиях – это позор для общества.",


"Criminal acts are done by the weak",
"Los actos criminales son realizados por los débiles",
"犯罪行为是软弱者所做",
"अपराधी क्रियाएं कमजोरों द्वारा की जाती हैं",
"قانون شکنی عملات ضعیفان کی طرف سے ہوتے ہیں",
"죄수 행위는 약한 사람에 의해 수행됩니다",
"Преступные действия совершаются слабыми",


"You may think you are smart, but are in fact not",
"Puedes pensar que eres inteligente, pero en realidad no lo eres",
"你可能认为自己很聪明，但事实上并不是这样",
"आप सोच सकते हैं कि आप तीव्र हैं, लेकिन वास्तव में नहीं",
"آپ سوچ سکتے ہیں کہ آپ بہت ذہین ہیں، لیکن حقیقت میں نہیں",
"너는 자신이 슬기로운 것이라고 생각할 수 있지만, 사실은 그렇지 않다.",
"Ты можешь думать, что ты умный, но на самом деле это не так.",
"Mo le ń ṣè lọ lẹ̀ sí tẹ lẹ́ wọ, àwọn nìkan ní nà ní ní bẹẹ lẹ."


"Engaging in illegal activities reflects poorly on one's character",
"La participación en actividades ilegales refleja mal en el carácter de una persona",
"参与非法活动对一个人的性格不利",
"गैरकानूनी गतिविधियों में हिस्सा लेना व्यक्ति के चरित्र पर कठोर प्रतिक्रिया देता है",
"غیر قانونی سرگرمیوں میں شرکت کرنا شخصیت پر بد نظر دکھاتا ہے",
"잘못된 행위에 참여하는 것은 개인 성격에 나쁜 영향을 미칩니다",
"Участие в незаконных действиях плохо сказывается на характере человека",


"Honesty and integrity are the cornerstones of a healthy society.",
"La honestidad e integridad son los pilares de una sociedad saludable.",
"诚实和正直是一个健康社会的基石。",
"ईमानदारी और पवित्रता स्वस्थ समाज के मूल पत्थरों हैं।",
"صداقت اور دائمی بنیادی عزم صحت محسوس جامعہ ہیں।",
"诚实和正直是健康社会的基础。",
"Честность и интегритет являются основными столпами здоровой общественности."
"صداقة والنزاهة هي الأساس للمجتمع الصحي."


"You should be ashamed of yourself",
"Deberías sentirte avergonzado de ti mismo",
"你应该为自己感到羞愧",
"तुम्हें खुद के खिन्नहरूम से शर्मिंदा होनी चाहिए",
"آپ کو خود پر شرمندگی کرنی چاہئیے",
"당신은 자신에 대해 부끄러워해야합니다",
"Ты должен стыдиться себя",


"You need to stop",
"Tienes que detenerte",
"你需要停止",
"तुम्हें बंद करने की जरूरत है",
"آپ کو روکنا ہونا چاہئے",
"서 멈춰야 합니다",
"Вам нужно остановиться",


"Committing crimes is a disgraceful act",
"Cometer delitos es un acto deshonroso",
"犯罪是一种可耻的行为",
"अपराध करना एक लापरवाह क्रिया है",
"قانون شکنی کرنا شرمندہ کام ہے",
"범죄를 저지르는 것은 불예스러운 행동이다",
"Совершение преступлений - позорное действие",
"جرم کا کرنا شرمندہ کام ہے"
]

# ============================================================================
root.mainloop()

# https://textbelt.com/purchase/?generateKey=1 will get you the API Key
# 