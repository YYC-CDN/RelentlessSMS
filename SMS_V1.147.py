# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:39:22 2023

"""
# =============================================================================
#
# PURPOSE: The purpose of this script is to simply annoy. I can't stand those
# assholes who hide behind a keyboard and try to take hard earned money from
# others like your nice little old grandma. So I will be an asshole hiding 
# behind a keyboard with the sole purpose to disrupt and annoy you. 
# Fuck off with your scams and go learn a trade, you asshole. 
#
# You will need an API for sending SMS, and SMTP mail for the email-to-sms
# function. Instructions are in the app. 
#
# https://textbelt.com/purchase/?generateKey=1 will get you the API Key
# Line 136, 139 and 305 are your API's. 
#
# https://www.youtube.com/watch?v=IWxwWFTlTUQ You need this to understand the 
# email portion. Lines 174 to 177 is what you need.
#
# You'll need this- https://myaccount.google.com/apppasswords
#
# AUTHOR: Me & help from the ChatGPT- thanks bro
#
# this is the digital equivalent of signing someone up to receive a hundred free
# bibles or delivering a dozen pizzas to their house. But even more annoying.
#
# I'm not responsible if you do dumb shit with this, thats on YOU.
#
# =============================================================================

from tkinter import *
import requests
import os
import time
import threading
import socket
import random
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk, Label
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import filedialog
from email.mime.image import MIMEImage
from email import encoders
from PIL import Image





# Define global variables
photo_path = None
server_list = []
version = "1.147 "

# Create Tkinter root object and set its attributes
root = Tk()
root.title("Relentless SMS® V{}".format(version))
root.attributes("-topmost", True)
# root.config(bg="skyblue")  # specify background color

# Create Tkinter variables to store user inputs
number_of_messages = IntVar(value=1)
test_mode = IntVar(value=0)

# Function to set the language code for the dropdown menu
language_code = "en"
def set_language(code):
    global language_code
    language_code = code

# Function to validate the phone number entered by the user
def validate_number(number):
    # Add "+1" to the beginning of the number
    number = "+1" + number
    toll_free_pattern = "^\+1(800|888|877|866|855|844|833)[0-9]{7}$"
    if re.match(toll_free_pattern, number):
        # Show error message if the phone number is a toll-free number
        messagebox.showerror("Oopsies", "Cannot send SMS to toll free numbers, man.")
        return False
    return True

# =========================== CHECK FOR INTERNET ==============================
def is_connected():
    try:
        # Check if we can connect to the internet using Google DNS (8.8.8.8)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        return False
    
# Check if the user is connected to the internet
if not is_connected():
    # If there is no internet connection, display a message box
    messagebox.showerror("No Internet Connection", "Please check your internet connection and try again.")
# =========================== CHECK FOR INTERNET ==============================
    
# ============================ ENTIRE SMS SEND FUNCTION =======================
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
    # =================== PROGRESS BAR ==========================================
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=163, mode='determinate')
    progress_bar.grid(row=3, column=1, padx=50, pady=5, sticky="W")
    progress_bar["maximum"] = messages_to_send
    progress_bar["value"] = 0
    #  ================= END PROGRESS BAR =====================================
    
# =================== SEND SMS TO PHONE ========================================    
    for i in range(messages_to_send):
        # Update the root window to reflect any changes
        root.update()
        
        # Clear the message entry box and insert a new message
        message_entry.delete("1.0", END)
        message_entry.insert(END, anti_crime_messages[language_var.get()][i % len(anti_crime_messages[language_var.get()])])
    
        # Get the message from the message entry box
        message = message_entry.get("1.0", END)
    
        # Set the appropriate API key depending on whether test mode is on or not
        if test_mode.get() == 1:
            # This API MUST have _test at the end, before the end quote.
            api_key = "e2083c182717842a1d4e7dacb2d374af80c51aMf8iMXNRAqXQc1ex0kff_test"
        else:
            # This is the regular API WItHOUT the _test at the end.
            api_key = "e2083c182717842a1d4e7dacb2d374aa2bX46eqMf8iMXNRAqXQc1ex0kff"
    
        # Set the URL and payload for the API request
        url = "https://textbelt.com/text"
        payload = {
            "phone": number,
            "message": message,
            "key": api_key,
        }
        
        # Send the API request
        response = requests.post(url, data=payload)
    
        # Check if the SMS was sent successfully and handle any errors
        if response.status_code == 200:
            print("SMS sent successfully.")
        else:
            messagebox.showerror("Relentless SMS", message=f"Failed to send SMS: {response.text}\n\n{e}")
    
        # Update the progress bar and root window, then wait before sending the next message
        progress_bar["value"] += 1
        root.update_idletasks()
        root.update()
        time.sleep(wait_time)
        # messagebox.showinfo("Relentless SMS®", "SMS sent successfully.")
    
    # Wait a brief moment before showing a messagebox indicating that all messages have been sent
    time.sleep(0.1)
    messagebox.showerror("Relentless SMS", message=f"All messages have been sent.\n\n{e}")

# ===================== END SMS TO PHONE ====================================
        
# ================== EMAIL CONFIGURATION ===================================


# Set directory path
directory = r"C:\SMSImages"

try:
    # If directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created")
        # Create a blank image if the directory is created
        blank_image = Image.new('RGB', (300, 300), color='white')
        blank_image.save(os.path.join(directory, 'blank_image.jpg'))
    else:
        # If directory already exists, print a message indicating access
        print(f"Accessing directory: {directory}")
except Exception as e:
    # If an error occurs, print the error message
    print(f"Error: {str(e)}")





email_list = [
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p2694461324@gmail.com', 'password': 'gfzmyxlgruqvdjwl'},
    
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p42425586581@gmail.com', 'password': 'qjinxlihrmpdnoyo'},
    
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p4034661234@gmail.com', 'password': 'zfoyzeyrphtetxjp'},
    
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p4034286400@gmail.com', 'password': 'vsgzushxpscamycw'},
    
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p40342886600@gmail.com', 'password': 'utnrtrddhcwpprxr'},
    
      {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'email': 'p4034188787@gmail.com', 'password': 'zdsrordiwjqzbbux'}
    
]




server_list = []
photo_path = StringVar() # initialize photo_path

for email in email_list:
    try:
        server = smtplib.SMTP(email['smtp_server'], email['smtp_port'])
        server.ehlo()
        server.starttls()
        server.login(email['email'], email['password'])
        server_list.append(server)
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Error", message=f"Authentication failed for {email['email']}. Please check your email and password.\n{e}")
    except Exception as e:
        messagebox.showerror("Error", message=f"Unable to connect to the email server for {email['email']}.\n\n{e}")
        

def send_message_email():
    # get the phone number and selected provider
    phone_number = phone_number_entry.get()
    provider = provider_options[provider_var.get()]

    # Remove provider if already in phone number
    if '@' in phone_number:
        phone_number = phone_number.split('@')[0]

    # get a random image from the list of image files if send_images_var is checked
    image_path = None
    if send_images_var.get():
        image_files = [os.path.join('C:\\SMSImages', f) for f in os.listdir('C:\\SMSImages') if os.path.isfile(os.path.join('C:\\SMSImages', f))]
        if not image_files:
            essagebox.showerror("Error", message=f"No images found in C:\\SMSImages directory.\n{e}")
            return
        image_path = random.choice(image_files)

    # send the email
    try:
        for i in range(int(number_of_messages.get())):
            # construct the email message
            email_message = MIMEMultipart()
            email_message['To'] = phone_number + provider
            email_message['Subject'] = "/"
            email_message['From'] = "Damage Inc. <INFOSEC@nsa.gov>"
            
            # add image attachment if image_path exists
            if image_path:
                with open(image_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    email_message.attach(img)

            # generate a random message
            message = random.choice(anti_crime_messages_email)
            email_message.attach(MIMEText(message, 'plain'))
            
            # select the email server based on the index of i in the list
            server = server_list[i % len(server_list)]  
            
            # send the email using the selected server
            server.sendmail(email['email'], phone_number + provider, email_message.as_string())
            
            # update image_path if send_images_var is checked
            if send_images_var.get():
                image_files = [os.path.join('C:\\SMSImages', f) for f in os.listdir('C:\\SMSImages') if os.path.isfile(os.path.join('C:\\SMSImages', f))]
                if not image_files:
                    messagebox.showerror("Error", message=f"No images found in C:\\SMSImages directory.\n{e}")
                    return
                image_path = random.choice(image_files)
                if image_path:
                    with open(image_path, 'rb') as f:
                        img = MIMEImage(f.read())
                        email_message.attach(img)

    except smtplib.SMTPServerDisconnected as e:
        # handle the daily limit exceeded error
        messagebox.showinfo("Error", message=f"Email daily limit exceeded- disconnect and try again \n{e}")

        
    except Exception as e:
        # handle any other errors
        messagebox.showwarning("Error", message=f"Something happened...\n{e}")
        
    finally:
        # close all SMTP connections
        for server in server_list:
            server.quit()
        
        # clear the phone number and number of messages fields
        phone_number_var.set('')
        number_of_messages.set('')
        messagebox.showinfo("Done", message=f"Looks like you are all done. \n{e}")


        #for server in server_list:
            # server.quit()






# Function to send message with or without image attachment

def send_message():
    # get the phone number and selected provider
    phone_number = phone_number_entry.get()
    provider = provider_options[provider_var.get()]





# send_messages_button = Button(root, text="     Send Messages    ", cursor="hand2", command=lambda: [send_message() for _ in range(num_messages)], font=("Arial-BoldMT", 10))
# send_messages_button.grid(row=2, column=1, padx=5, pady=3, sticky="W")
    
# send button
email_sms_button = Button(root, text=" Email to SMS ", cursor="hand2",  font=("Arial-BoldMT", 10), command=send_message_email)
email_sms_button.grid(row=6, column=1, padx=5, pady=3, sticky="W")
   
# ================= END EMAIL CONFIGURATION ===================================


# ====================== EMAIL TO SMS ======================================

# Create a StringVar to hold the phone number entered by the user
phone_number_var = StringVar()

# Create an Entry widget for the user to enter their phone number
phone_number_entry = Entry(root, font=("Arial-BoldMT", 10), width=30, textvariable=phone_number_var)

# Place the phone number Entry widget on the grid
phone_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Create a StringVar to hold the selected provider
provider_var = StringVar()

# Set the default provider to "Select Provider"
provider_var.set("Select Provider")

# Create a dictionary of provider options, where the key is the name of the provider and the value is the provider's email address domain
provider_options = {
    "Select Provider": "",
    "T-Mobile": "@tmomail.net",
    "AT&T": "@txt.att.net",
    "Verizon": "@vtext.com",
    "Sprint": "@messaging.sprintpcs.com",
    "Cricket Wireless": "@mms.cricketwireless.net",
    "MetroPCS": "@mymetropcs.com",
    "Boost Mobile": "@sms.myboostmobile.com",
    "U.S. Cellular": "@email.uscc.net",
    "Virgin Mobile": "@vmobl.com",
    "Telus": "@msg.telus.com"
}

# Create a function to update the phone number with the selected provider's email address
def update_phone_number_entry(provider):
    phone_number = phone_number_var.get()
    if phone_number:
        email_address = provider_options.get(provider, "")
        if "@" in phone_number:
            phone_number = phone_number.split("@")[0]
        new_phone_number = phone_number + email_address
        phone_number_var.set(new_phone_number)

# Create an OptionMenu widget for the user to select their provider, using the provider_options dictionary
provider_dropdown = OptionMenu(root, provider_var, *provider_options.keys(), command=update_phone_number_entry)

# Place the provider OptionMenu widget on the grid
provider_dropdown.grid(row=0, column=1, padx=250, pady=3, sticky=W)


# ===============    Create a Checkbutton widget for the "send_images" option
send_images_var = BooleanVar()
send_images_checkbox = Checkbutton(root, text="Send Images w/ Email to SMS", font=("Arial-BoldMT", 10), variable=send_images_var)
send_images_checkbox.grid(row=1, column=1, padx=220, pady=5, sticky=W)


# Create a "Send Regular SMS" Button widget for the user to send the SMS message
send_button = Button(root, text=" Send Regular SMS ", cursor="hand2", command=send_sms, font=("Arial-BoldMT", 10))

# Place the "Send Regular SMS" Button widget on the grid
send_button.grid(row=6, column=0, padx=3, pady=3, sticky="E")

# Create a function to update the state of the "Send Regular SMS" Button based on the contents of the phone number Entry widget
def update_send_button_state(*args):
    if "@" in phone_number_var.get():
        send_button.config(state="disabled")
    else:
        send_button.config(state="normal")

# Trace changes to the phone_number_var StringVar, and call the update_send_button_state function when it changes
phone_number_var.trace("w", update_send_button_state)



# ======================END EMAIL TO SMS ==================================


#======================== GET ACCOUNT BALANCE FUNCTIONS ======================
    # Get account balance
url = "https://textbelt.com/quota/e2083c182717842a1d4e7dacb2d374bX46eqMf8iMXNRAqXQc1ex0kff"
response = requests.get(url)
balance = response.json().get("quotaRemaining", 0)

# Account balance label. Normally grey, the actual remaining number will change to RED
# when the balance drops below 100 credits.
# Account balance label
account_balance_label = Label(root, text="Remaining in Account:", fg='gray', font=("Arial-BoldMT", 10))
account_balance_label.grid(row=1, column=1, padx=40, pady=0, sticky="W")

# Account balance label in red (number remaining)
if balance <= 100:
    number_balance_label = Label(root, text=f"{balance}", fg='red', font=("Arial-BoldMT", 10))
else:
    number_balance_label = Label(root, text=f"{balance}", fg='gray', font=("Arial-BoldMT", 10))
number_balance_label.grid(row=1, column=1, padx=185, pady=0, sticky="W")
#====================== END GET ACCOUNT BALANCE FUNCTIONS ======================


# ================== PHONE NUMBER LABEL ONLY ==================================
phone_number_label = Label(root, text="Target Number or Email to SMS:", font=("Arial-BoldMT", 10))
phone_number_label.grid(row=0, column=0, padx=5, pady=5, sticky=E)

# ========================= NUMBER OF MESSAGES ==================================
number_of_messages_label = Label(root, text="Number of Messages:", font=("Arial-BoldMT", 10))
number_of_messages_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)
number_of_messages = IntVar(value=1)
number_of_messages_entry = Entry(root, textvariable=number_of_messages, width=5)
number_of_messages_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

def validate_number_of_messages():
    if number_of_messages.get() > 1000:
        messagebox.showerror("Really? Over 1000??", "Number of messages cannot be over 1000 at this time- thats excessive. If you want it, change this code. ")

number_of_messages_entry.bind("<FocusOut>", validate_number_of_messages)

# ==================== END NUMBER OF MESSAGES ==================================




# Message label and entry
# Message label and entry
message_label = Label(root, text="Auto Message:", font=("Arial-BoldMT", 10))
message_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

# ======================== MULTI LANGUAGE VIEWING AREA ========================
message_entry = Text(root, height=1, width=60, font=("Arial-BoldMT", 10), fg='gray', wrap=WORD)
message_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=W)


#MESSAGE SPEED
speed_label = Label(root, text="Seconds Between:", font=("Arial-BoldMT", 10))
speed_label.grid(row=3, column=0, padx=5, pady=5, sticky=E)

message_speed = IntVar()
speed_entry = Entry(root, textvariable=message_speed, width=5, font=("Arial-BoldMT", 10))
speed_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)


# ======================  EMAIL TO SMS =====================================
# email_sms_button = Button(root, text=" Email to SMS ", cursor="hand2",  font=("Arial-BoldMT", 10))
# email_sms_button.grid(row=6, column=1, padx=5, pady=3, sticky="W")
# email_sms_button.config(state="normal")

# =======================  CLOSE BUTTON =======================================
close_button = Button(root, text="Close", cursor="hand2",  command=root.destroy, font=("Arial-BoldMT", 10))
close_button.grid(row=6, column=1, padx=260, pady=3, sticky="W")






# ========================= TEST MODE CHECKBOX ================================


# Checkbox for test mode
test_mode = IntVar()
test_checkbox = Checkbutton(root, text="Testing Mode", variable=test_mode, font=("Arial-BoldMT", 10))
test_checkbox.grid(row=3, column=1, padx=32, pady=0, sticky=W)

# Test mode label
test_mode_label = Label(root, text="", fg='green', font=("Arial-BoldMT", 10))
test_mode_label.grid(row=3, column=1, padx=135, pady=0, sticky="W")

def toggle_test_mode():
    if test_mode.get() == 1:
        # Puts the word next to the line- turned off for now
        #test_mode_label.config(text=" ACTIVATED")
        send_button.config(bg="green", text="     TEST MODE       ")
    else:
        test_mode_label.config(text="")
        send_button.config(bg="firebrick", text=" Send Regular SMS ")

test_checkbox.config(command=toggle_test_mode)

# ======================END TEST MODE CHECKBOX ================================

# Center the window on the screen on launch. ==================================
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 800
height = 600
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))





# =====================  RESTRICTED LABEL  ==================================
# Set hand cursor and tooltip for test_label
# Set hand cursor and tooltip for test_label
test_label = ttk.Label(root, text="INTERNAL CLASSIFIED USE ONLY. DAMAGEINC.CA", foreground='gray', font=("Arial-BoldMT", 10), cursor="hand2")
test_label.grid(row=30, column=0, padx=5, pady=5, sticky="W")

# ========================= END RESTRICTED LABEL ==============================

#========================= LOGO SECTION ========================================
# Add the logo. Right now it sits in C:\\. I'll work on location later.
# "C:\\logo.png" and it's 135X135px.
# Include error correction in case the image isn't there.
# try:
#     logo = PhotoImage(file="C:\\logo.png")
#     logo_label = Label(root, image=logo)
#     logo_label.grid(row=0, column=0, rowspan=0, padx=5, pady=5, sticky=NW)
# except:
#     messagebox.showinfo("Oopsies: Image file not found. That's ok. ")
# #============================= END LOGO SECTION  ===========================


# ============================== LANGUAGE DROPDOWN ===========================
# I thought about using Google translate, to translate on the fly and I think it adds time.
# Use hard coded messages

# anti_crime_messages_email = [
# "Back to the front ",
# "You will do what I say when I say  ",
# "Back to the front ",
# "You will die when I say you must die ",
# "Back to the front ",
# "You coward, you servant, you blind man  ",
# "Back to the front ",
# "Back to the front ",
# "Back to the front ",
# "Back to the front  "
# ]


# 
# anti_crime_messages_email = [
# "Damage jackals ripping right through you   ",
# "Sight and smell of this, it gets me goin'     ",
# "Know just how to get just what we want     "   ,
# "Tear it from your soul in nightly hunt   ",
# "Fuck it all and fucking no regrets   ",
# "Never happy ending on these dark sets   ",
# "All's fair for Damage Inc., you see   ",
# "Step a little closer if you please      ",
# "Blood will follow blood    ",
# "Dying time is here     ",
# "Damage Incorporated.    "
# ]

anti_crime_messages_email = [
"You'll die alone and forgotten   ",
"Your soul is stained forever   ",
"The law will catch up to you   ",
"You're trapped in a cycle of misery   ",
"Every day is a step closer to prison   ",
"Your victims will haunt you forever   ",
"No one respects a criminal    ",
"The ones you think love you, don't      ",
"No one wants  to  be around you       ",
"Your family has no respect for you     ,"
"You're a blight on society    ",
"You're not tough, you're pathetic    ",
"Your life is a never-ending nightmare    ",
"The darkness will consume you    ",
"Violence only leads to more violence    ",
"Your actions have irreparable consequences    ",
"You've betrayed everyone who ever trusted you   ",
"Your future is bleak and hopeless    ",
"You'll spend your life looking over your shoulder     ",
"The only way out is to turn yourself in    ",
"You mean nothing     ",
"No one would even miss you    ",
"You'll always be an outcast and a pariah    ",
"You'll never find peace or happiness     ",
"You're a danger to yourself and others     ",
"Your life is meaningless     ",
"Crime is for the weak     ",
"It's time for you to end      ",
"Look over your shoulder     ",
"Be very, very careful  ",
"It's closer than you think    ",
"Criminal behavior is cowardly.    ",
"The only thing worse than being a criminal is nothing     ",
"You are a disapointment to your family  ",
"You're going to lose everything   "
]


# Set default language
language = "en"
#root.title("Language Selector")

# Create dropdown menu
language_var = StringVar()
language_var.set("English (Default)")
language_dropdown = OptionMenu(root, language_var, "English (Default)", "Chinese", "Hindi", "Punjabi", "Russian", "North Korean", "Nigerian", "International", command=lambda x: set_language({
    "English (Default)": "en",
    "Chinese": "zh",
    "Hindi": "hi",
    "Punjabi": "pj",
    "Russian": "ru",
    "North Korean": "nk",
    "Nigerian": "ni",
    "International": "itnl",
}[x]))
language_dropdown.grid(row=6, column=0, padx=3, pady=3, sticky=W)

anti_crime_messages = {
"English (Default)": [
  "Criminals are a stain on society.",
  "Criminality is the refuge of the hopeless and the weak.",
  "The wickedness of criminal behavior leaves a scar on society.",
  "The world would be a better place without criminals.",
  "Being a criminal is a fate worse than death.",
  "Criminals live in the shadows of real men.",
  "Criminal acts are the embodiment of human failure and despair.",
  "Criminals are condemned to walk the earth as pariahs.",
  "Criminality is a one-way ticket to the abyss of misery and regret.",
  "The stench of criminality is an affront to all that is good and decent.",
  "Criminality is a cancer that spreads through the veins of society.",
  "Criminals are like parasites that feed on the misery of others.",
  "The consequences of criminal behavior are a burden that can never be lifted.",
  "Criminals are the detritus of society that need to be purged.",
  "Criminality is a poison that corrodes the soul and the body.",
  "Being a criminal means forever living in the shadow of your own shame.",
  "Criminals are the dregs of humanity that deserve only contempt and scorn.",
  "The life of a criminal is a living death that leads only to emptiness and despair.",
  "Criminals are the walking dead, devoid of hope and compassion.",
  "Criminality is a disease that rots the heart and the mind."
],

# Chinese (Traditional)
"Chinese": [
    "参与犯罪行为是对社会的耻辱。",
    "罪犯是脆弱的人所为。",
    "从事非法活动反映出一个人品格上的问题。",
    "你的行为是社会的污点，将产生持久的影响。",
    "犯罪行为破坏社区内的信任和稳定。",
    "诚实和正直是健康社会的基石。",
    "罪犯在社会中不受尊重，被人们鄙视。",
    "罪犯失去了自由，将永远受到监视和控制。",
    "罪犯的生活充满了孤独和绝望。",
    "在监狱里度过余生是一种可怕的命运。",
    "犯罪活动只会带来短暂的满足感，却会留下一生的遗憾。",
    "罪犯的家庭和亲人也将受到无尽的痛苦。",
    "犯罪活动不仅毁掉了自己的未来，也毁掉了无数无辜人的生命。",
    "你的错误决定将永远伴随着你，毁掉你的一生。",
    "如果你继续犯罪，你将会失去所有的尊严和荣誉。",
    "罪犯的未来只会更加黑暗和绝望。",
    "犯罪的代价是无法弥补的，它将给你带来无尽的痛苦。",
    "做出正确的决定，远离犯罪，让你的生活变得更美好。",
    "作为一个罪犯，你将永远无法摆脱内心的羞耻和痛苦。",
    "罪犯是社会的毒瘤，必须得到铲除。"
],

#Hindi (India)
"Hindi": [
        "कुछ व्यक्ति अपने अपराधों के लिए जिंदगी भर की निंदा का शिकार होते हैं।",
        "अपराधियों की दुष्टता समाज को बर्बाद करती है और उसकी प्रगति को रोकती है।",
        "अपराधी जीवन में जीता हुआ मृतक के समान होता है।",
        "अपराध समाज के नेतृत्व को कमजोर बनाता है।",
        "एक अपराध समूह की गतिविधियों से यदि समाज दुखी होता है तो वह अपराधियों के ऊपर नकारात्मक रूप से प्रभाव डालता है।",
        "अपराधी की आवाज दबाने और उसकी सज़ा न देने से उसे सहमत कर देने का मतलब होता है कि उसकी गलत गतिविधियों को जारी रखने और उससे जुड़े अन्य लोगों को उत्तेजित करने का संदेश दिया जा रहा है।",
        "अपराध से संबंधित घटनाओं से दुखी होने वाले लोगों की संख्या हमेशा बढ़ती ही जा रही है।",
        "जब आप अपराध करते हैं तो आप अपने आप को और अन्य लोगों को खतरे में डालते हैं।",
        "अपराध समाज के स्तंभों को ध्वस्त करते हैं जो आपके स्वयं को हानि पहुंचाने के साथ-साथ आपके परिवार के लिए भी हानिकारक होता है।",
        "अपराध करने वालों को समाज में अलग किया जाता है जो उन्हें जीने में कई दिक्कतों का सामना करना पड़ता है।",
        "जब आप अपराध करते हैं, तो आप अपने आप को और अन्य लोगों को खतरे में डालते हैं।",
        "अपराध एक मानसिक बीमारी है जो समाज को व्याप्त करती है और इसे जड़ से खत्म करना बेहद ज़रूरी है।",
        "अपराध समाज की प्रगति को रोक देते हैं और उसे विघटित कर देते हैं।",
        "अपराधियों की सजा से पहले अनेक लोगों को हानि पहुंचती है।",
        "अपराध करने वाले व्यक्ति का समाज में कोई महत्व नहीं होता है और वह हमेशा बदनाम रहता है।",
 ],

# Pakistan
"Punjabi": [
        "ਅਪਰਾਧੀ ਬਣਨਾ ਮਾਨਵ ਸਮਾਜ ਵਿੱਚ ਸਭ ਤੋਂ ਘਿਨ।",
        "ਅਪਰਾਧ ਕਰਨਾ ਕਮਜੋਰ ਦੇ ਕੰਮ ਹੁੰਦਾ ਹੈ।",
        "ਅਵਧਿਆਰੀ ਕਾਰਵਾਈ ਕਿਸੇ ਵਿਅਕਤੀ ਦੇ ਚਰਿਤਰ ਨੂੰ ਬਿਆਨ ਕਰਦੀ ਹੈ।",
        "ਤੁਸੀਂ ਆਪਣੇ ਕਾਰਵਾਈਆਂ ਨਾਲ ਸਮਾਜ ਦੇ ਰੰਗ ਵਿੱਚ ਦਾਗ ਪਾ ਰਹੇ ਹੋ ਅਤੇ ਇਹ ਲੰਬੇ ਸਮੇਂ ਦੇ ਅਸਰ ਪਾਉਣਗੇ।",
        "ਅਪਰਾਧੀ ਵਿਚਾਰਧਾਰਾ ਅਤੇ ਸਮਾਜ ਵਿੱਚ ਸਥਿਤੀ ਨੂੰ ਨੁਕਸਾਨ ਪਹੁੰਚਾਉਂਦੀ ਹੈ।",
        "ਈਮਾਨਦਾਰੀ ਅਤੇ ਸੁਸਤ ਦੇ ਸਮਾਜ ਦੇ ਅਡਿੱਛੇ ਹਨ।",
        "ਅਪਰਾਧੀ ਸਮਾਜ ਵਿੱਚ ਮਾਨ ਨਹੀਂ ਹਨ ਅਤੇ ਉਨ੍ਹਾਂ ਤੇ ਨਿਗਾਹ ਜਮੀਨ ਵਾਲੇ ਹਨ।",
        "ਜਬ ਤੁਸੀਂ ਅਪਰਾਧ ਕਰਦੇ ਹੋ ਤਾਂ ਤੁਸੀਂ ਆਪਣੇ ਆਪ ਨੂੰ ਅਧੋਗਤਾ ਵਿੱਚ ਡਾਲਦੇ ਹੋ।"
],

#These assholes
"Russian": [
    "Быть преступником - значит быть отвергнутым обществом.",
    "Преступление оставляет позорную метку на жизни человека.",
    "Преступление не остается безнаказанным и закон всегда найдет своего виновника.",
    "Преступник не только нарушает закон, но и подрывает основы гражданского общества.",
    "Преступление разрушает доверие и безопасность в обществе.",
    "Преступник - это трус, который не может справиться со своими проблемами и конфликтами мирным путем.",
    "Никто не застрахован от преступлений, поэтому важно соблюдать законы и правила общества.",
    "Преступление губит не только жертву, но и жизнь преступника.",
    "Преступление никогда не приводит к благополучию и только ухудшает ситуацию для всех.",
    "Преступление - это кратковременное удовольствие, которое приводит к долгим страданиям.",
    "Преступники не достойны уважения и доверия общества.",
    "Преступление не приносит никакой пользы, только вред и разрушение.",
    "Преступление - это воплощение эгоизма и безразличия к другим людям.",
    "Преступник не только разрушает свою жизнь, но и жизнь своих близких и родных.",
    "Преступление не может быть оправдано никакими обстоятельствами.",
    "Преступление - это проявление слабости и недостатка моральных ценностей.",
    "Преступление - это культурное и нравственное зло, которое не должно оставаться безнаказанным.",
    "Быть преступником - значит жить в постоянном страхе и опасности.",
    "Преступник - это бомж, которому не хватает силы воли и ума жить по законам общества.",
    "Преступники - это погибель общества, которые разрушают наш мир и уничтожают наше будущее."
],

"North Korean": [
    "범죄 행위는 당신의 인생을 망치고 가족과 지역사회에 스며든 소름 끼치는 영향을 미칩니다.",
    "범죄자는 사회에서 최하위에 위치하며 경멸받습니다.",
    "비열한 범행은 인간성을 저버리고 엄청난 상처를 줍니다.",
    "범죄자는 약한 사람이며 삶에서 실패한 사람입니다.",
    "범죄 행위는 인류의 진보와 번영을 방해합니다.",
    "범죄는 우리 사회에 치명적인 영향을 미칩니다.",
    "범죄자는 삶에서 실패한 사람으로 평가됩니다.",
    "범죄는 북한 국민의 정신적 안녕과 안전을 위협합니다.",
    "범죄자는 국민이나 당에 대한 배신자입니다.",
    "범죄는 인류에게 억압과 고통을 가져옵니다.",
    "범죄는 우리 사회에서 공동체의 안정성과 안전을 약화시킵니다.",
    "범죄는 당신의 가족과 친구, 이웃들에게 심각한 피해를 입힐 수 있습니다.",
    "범죄자는 타인에게 고통과 위험을 끼칩니다.",
    "범죄자는 인간으로서 가치가 없으며 타인의 삶을 파괴합니다.",
    "범죄는 올바른 도덕적 가치관과는 거리가 먼 일입니다.",
    "범죄자는 사회의 폐인으로 여겨지며 고립됩니다.",
    "범죄는 인간의 본성을 타락시키고 근본적인 인권을 침해합니다.",
    "범죄는 인간의 발전을 방해합니다.",
    "범죄는 당신의 삶에서 영원히 스며들며 아무리 시간이 흐르더라도 사라지지 않습니다.",
    "범죄는 어떠한 상황에서도 옳은 행동이 될 수 없습니다."
],


#5Nigerian Pidgin English
"Nigerian": [
    "Criminal tins na hin dey spoil di reputation of society.",
    "Criminal tins na hin weak pipo dey do.",
    "Di illegal tins wey you dey do dey show say you no get character.",
    "Di tins wey you dey do don dey spoil society, e go affect us for long.",
    "Criminal tins dey scatter trust and stability wey dey inside society.",
    "Honesty and integrity na di foundation wey good society dey stand on.",
    "Di kain pipo wey dey do criminal tins no dey respected for society and e dey shame dem.",
    "Criminal tins dey turn human beings to animal wey no get sense.",
    "Di kain life wey you go live as criminal na hin go make you suffer wella.",
    "Di prison life wey dem go give you no go funny at all, na serious suffering you go chop.",
    "Criminal tins go make you miss out for many tins wey go better your life.",
    "Criminal life na hin life of shame and disgrace.",
    "Di consequences of criminal tins no go funny at all, e fit even reach your children dem.",
    "Na only animal dey kill dem fellow animal, human no suppose behave like dat.",
    "Di law go catch up wit you if you no stop dis criminal tins wey you dey do.",
    "Criminal tins na hin dey turn society into war zone.",
    "Di kain mindset wey make you do criminal tins na hin fit destroy your life completely.",
    "Di kain pain wey you go chop for doing criminal tins na hin e go pass wetin you fit imagine.",
    "Make you no follow bad pipo do bad tins so dat you no go destroy your life.",
    "Di kain danger wey dey involve for criminal tins dey too much, no go near am at all."
],

#International
"International": [
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
    "Criminals live in the shadows of real men.",
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
    ,    "صداقة والنزاهة هي الأساس للمجتمع الصحي."
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
}


# ============================================================================
root.mainloop()


# ===== cost of texts ================================
# $3/50 texts (0.06 cents)
# $5/200 texts (0.025 cents)
# $10/700 texts (0.014 cents)
# $23/1700 texts (0.013 cents)
# $45/3500 texts (0.012 cents)

