# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 13:03:43 2023

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
import requests
import json
from tkinter.constants import END




version = "2.0 W/Scout"
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
        message_entry.insert(END, anti_crime_messages_english[i % len(anti_crime_messages_english)])
        message = message_entry.get("1.0", END)

        if test_mode.get() == 1:
            # This API MUST have _test at the end, before the end quote.
            api_key = "e2083c182717842a1d4e7dacb2d374aiMXNRAqXQc1ex0kff_test"
        else:
            # This is the regular API WItHOUT the _test at the end.
            api_key = "e2083c182717842a1d4e7dacb2d374af80c46AqXQc1ex0kff"

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
    messagebox.showinfo("Relentless SMS", "All messages have been sent. Good job, man. ")


    # Get account balance
url = "https://textbelt.com/quota/e2083c1827178a2MXNRAqXQc1ex0kff"
response = requests.get(url)
balance = response.json().get("quotaRemaining", 0)


# Account balance label. Normally grey, the actual remaining number will change to RED
# when the balance drops below 100 credits.
# Account balance label
account_balance_label = Label(root, text="Remaining in Account:", fg='gray', font=("Segoe UI", 10))
account_balance_label.grid(row=1, column=1, padx=40, pady=0, sticky="W")

# Account balance label in red (number remaining)
if balance <= 100:
    number_balance_label = Label(root, text=f"{balance}", fg='red', font=("Segoe UI", 10))
else:
    number_balance_label = Label(root, text=f"{balance}", fg='gray', font=("Segoe UI", 10))
number_balance_label.grid(row=1, column=1, padx=185, pady=0, sticky="W")
 
#================================= NORMAL WORKING CODE ========================
# #Account Balance label
# account_balance_label = Label(root, text="Remaining in Account: ", fg='gray', font=("Segoe UI", 10))
# account_balance_label.grid(row=1, column=1, padx=40, pady=0, sticky="W")

# #Account balance label in red (number remaining)
# number_balance_label = Label(root, text=f"{balance}", fg='gray', font=("Segoe UI", 10))
# number_balance_label.grid(row=1, column=1, padx=185, pady=0, sticky="W")
#================================= NORMAL WORKING CODE END ====================



# root.after(1000, update_balance) # call the function every 1000 milliseconds

# def update_balance():
#     url = "https://textbelt.com/quota/e2083c182717842a1d4e7dacb2d374af80c51a2bX46eqMf8iMXNRAqXQc1ex0kff"
#     response = requests.get(url)
#     balance = response.json().get("quotaRemaining", 0)
#     account_balance_label["text"] = f"Remaining in Account: {balance}"
#     root.after(1000, update_balance) # call the function every 1000 milliseconds (1 second)



# =========================== ALL THE GUI =====================================

# Phone Number label and entry
phone_number_label = Label(root, text="Target Number:", font=("Segoe UI", 10))
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
test_mode_label = Label(root, text="", fg='green', font=("Segoe UI", 10))
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
    messagebox.showinfo("Oopsies: Image file not found. That's ok. ")



# Center the window on the screen on launch. ==================================
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1000
height = 600
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))



# # For the language dropdown
# language_var = StringVar(root)
# language_var.set("Select Language")
# language_dropdown = ttk.OptionMenu(root, language_var, "Select Language", "English", "Chinese", "Hindi", "Russian", "North Korean", "Nigerian")
# language_dropdown.grid(row=6, column=0, padx=3, pady=3, sticky=W)


language_var = StringVar(root)
language_var.set("Select Outgoing Language")

def change_message(*args):
    global selected_language
    selected_language = language_var.get()

    if selected_language == "English":
        messages = anti_crime_messages_english
    elif selected_language == "Chinese":
        messages = anti_crime_messages_chinese
    elif selected_language == "Hindi":
        messages = anti_crime_messages_hindi
    elif selected_language == "Russian":
        messages = anti_crime_messages_russian  
    elif selected_language == "North Korean":
        messages = anti_crime_messages_northkorean
    elif selected_language == "Nigerian":
        messages = anti_crime_messages_nigerian
    else:
        messages = anti_crime_messages_international


#============================ ANtI CRIME MESSAGES ============================

anti_crime_messages_english = [
"Engaging in criminal behavior is a disgrace to society.",
"Criminal acts are done by the weak.",
"Engaging in illegal activities reflects poorly on one's character.",
"Your actions are a stain on society and will have lasting effects.",
"Criminal behavior destroys trust and stability within a community.",
"Honesty and integrity are the cornerstones of a healthy society.",
"Criminals are not respected in society and are looked down upon.",
"You should be ashamed of yourself for trying to cheat people.",
"You need to stop.",
"Committing crimes is a disgraceful act.",
"You are not above the law and will be held accountable.",
"Justice will be served to those who engage in criminal behavior.",
"The law-abiding citizens deserve to live in a safe and secure community.",
"Being a criminal is a sign of failure, not success.",
"Your actions are damaging the community and putting others at risk.",
"It's never too late to turn your life around and make positive changes.",
"Criminal behavior is unacceptable and will not be tolerated." ,
"Being a criminal will only bring you pain and regret.",
"Crime will not solve your problems, only create more.",
"Criminal activity is never justified and always leads to harm.",
"Your criminal behavior is a threat to the safety and security of others.",
"The road to success is built on hard work and determination, not illegal shortcuts.",
"Engaging in crime only perpetuates negative cycles and ruins lives.",
"Crime only benefits those in power, never the ones committing the acts.",
"A life of crime is never fulfilling or satisfying.",
"The only way to achieve true success is through lawful means.",
"Criminals are easily caught and punished by the law.",
"Stealing is a sign of cowardice and lack of ambition.",
"Living a life of crime leads to a life of poverty.",
"Criminals are not respected in society and are looked down upon.",
"The consequences of criminal behavior far outweigh the temporary gains.",
"Living an honest life brings peace and dignity.",
"The thrill of breaking the law is not worth the price you'll pay."]


anti_crime_messages_chinese = [
"犯罪行为是对社会的耻辱。",
"罪犯行为是软弱者所为。",
"从事非法活动是对个人品格的不利影响。",
"诚信和正直是健康社会的基石。",
"试图欺骗别人是令人羞愧的。",
"你需要停止。",
"犯罪是可耻的行为。",
"你并不凌驾于法律之上，将会被追究责任。",
"对从事犯罪行为的人将会伸张正义。",
"守法的公民应该生活在一个安全的社区。",
"成为罪犯是失败的标志，而不是成功。",
"你的行为损害了社区并使他人面临风险。",
"改变生活并进行积极的改变永远不晚。",
"真正的力量在于遵守规则并做正确的事。",
"成为罪犯只会给你带来痛苦和后悔。",
"犯罪不会解决你的问题，只会造成更多问题。",
"你的行为是对社会的玷污，并会产生持久的影响。",
"犯罪行为绝不能被证明是正当的，总是导致伤害。",
"你的犯罪行为对他人的安全和安全构成了威胁。",
"通往成功的道路是建立在努力工作和决心上，而不是非法的捷径。"]



anti_crime_messages_hindi = [
"अपराधी व्यवहार करना समाज के लिए शर्मनाक है।",
"अपराधी क्रियाएं कमजोरों द्वारा की जाती हैं।",
"गैरकानूनी गतिविधियों में हिस्सा लेना व्यक्ति की व्यवस्था पर अशुभ प्रभाव डालता है।",
"ईमानदारी और सम्पत्ति एक स्वस्थ समाज के मूल स्तंभ हैं।",
"लोगों को धोखा देने का प्रयास करते हुए आपको अपने आप के लिए शर्मिंदा होना चाहिए।",
"तुम्हें रुकना चाहिए।",
"अपराधों को करना शर्मनाक क्रिया है।",
"तुम्हें कानून से ऊपर नहीं होना चाहिए और जिम्मेदार होने वाले होंगे।",
"अपराधी व्यवहार करने वालों को न्याय मिलेगा।",
"अपराधी व्यवहार करना समाज के लिए बर्दाश्त है।",
"अपराधी क्रियाएं कमजोरों द्वारा की जाती हैं।",
"अवैध गतिविधियों में हस्तक्षेप करना व्यक्ति के विवेक पर कुख्यात होता है।",
"ईमानदारी और सत्यनिष्ठा स्वस्थ समाज के मूल धारणाएं हैं।",
"लोगों को धोखे देने की कोशिश करने के लिए तुम्हें शर्मिंदगी होनी चाहिए।",
"तुम्हें रुकने की आवश्यकता है।",
"अपराधों की आपत्ति एक बर्दाश्त क्रिया है।",
"तुम कानून से ऊपर नहीं हो और जवाबदेही के लिए होगे।",
"अपराधी व्यवहार करने वालों को न्याय मिलेगा।"]

anti_crime_messages_russian = [
"Участие в преступной деятельности - позор обществу.",
"Преступные действия совершаются слабыми людьми.",
"Участие в незаконных действиях плохо сказывается на характере человека.",
"Честность и интегритет - это основа здорового общества.",
"Преступники не уважаются в обществе и смотрятся свысока.",
"Вам стыдно за то, что вы пытаетесь обмануть людей.",
"Тебе нужно остановиться.",
"Совершение преступлений - позорный поступок.",
"Вы не выше закона и будете отвечать за свои действия.",
"Правосудие будет выступлено в отношении тех, кто участвует в преступной деятельности.",
"Законопослушные граждане заслуживают жить в безопасном и надежном обществе.",
"Быть преступником - это знак поражения, а не успеха."]


anti_crime_messages_northkorean = [
"범죄 행위에 참여하는 것은 사회에 부끄러움을 안겨줍니다.",
"범죄 행위는 약한 사람들에 의해 일어납니다.",
"불법 행위에 참여하는 것은 그의 성격에 나쁜 영향을 미칩니다.",
"정직과 정직성은 건강한 사회의 기초가 됩니다.",
"사람들을 꾸짖기 위해 자신에게 부끄러워해야 합니다.",
"당신은 중지해야 합니다.",
"범죄를 저지르는 것은 부끄러운 행위입니다.",
"당신은 법을 위한 것이 아니며, 책임져야 합니다.",
"범죄 행위에 참여하는 사람에게 정의가 서집니다.",
"법을 준수하는 시민들은 안전하고 안정적인 지역에서 살 수 있어야 합니다.",
"범죄자가 실패의 징조이고, 성공의 징조가 아닙니다.",
"당신의 행동은 지역을 파괴하고 다른 사람들을 위험에 빠뜨립니다."]


anti_crime_messages_nigerian = [
"Tá áfẹ́wọ́ ni ibẹrẹ tó ṣe àjẹ́ ìkẹ́wé ni o ni òdè lórí àmì ìtọ́ka.",
"Àwọn ìkẹ́wé tó ń jẹ́ àfẹwọ ní ibẹrẹ.",
"Tá áfẹ́wọ́ ni ibẹrẹ tó ní ìkẹ́wé àìtọ́ tó ń pọ̀ gẹ́gẹ́ bí àkọlé.",
"Àṣẹ ìrànlọ́wọ́ àti inú irọ́lẹ̀ tọ́ka ni ògbón ìtọ́ka.",
"Ìbẹ̀rẹ yẹn o le gba àsìṣe láti dínà ìrẹ̀tẹ́.",
"Ìbẹ̀rẹ gbọ́dọ̀ jẹ́ dídá.",
"Ìkẹ́wé ni o ni òdè lórí àmì ìtọ́ka.",
"Ìbẹ̀rẹ kò ní ajọ ilẹ̀ tó yẹ yín ìgbà tó yín ní báyìí nlo.",
"Ìbẹ́rẹ tó ṣe àjẹ ìkẹ́wé ní o ni òdè lórí àmì ìtọ́ka.",
"Àwọn àjẹ́wọ tó ń gbọ́ ìtọ́ka tó ní aiyépọ̀ ìtọ́ka tó ń yẹ yín.",
"Ìjẹ́wọ ni o ni òdè lórí àmì ìtọ́ka ni o ni wọn ni òun lọ lẹ́yìn.",
"Àwọn ìtọ́rọ ìbẹ̀rẹ ní o ṣe pèsè ìtọ́ka àti ní o ni wọn pè láti òrùn àwọn."]



anti_crime_messages_international = [
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


language_var.trace("w", change_message)

language_dropdown = ttk.OptionMenu(root, language_var, "Select Language", "English", "Chinese", "Hindi", "Russian", "North Korean", "Nigerian")
language_dropdown.grid(row=6, column=0, padx=3, pady=3, sticky=W)

# ==================== https://www.scout.tel/phone-number-lookup ==============

# from tkinter import *
# import requests
# import json
# from tkinter.constants import END

# root = Tk()

# Phone number entry
# phone_number_entry = Entry(root, font=("Segoe UI", 10))
# phone_number_entry.grid(row=0, column=0, padx=5, pady=5, sticky=W)

def get_advanced_number_lookup(number):
    headers = {
        'x-rapidapi-host': "icehook-systems-icehook-systems-default.p.rapidapi.com",
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"
    }

    url = "https://icehook-systems-icehook-systems-default.p.rapidapi.com/number/lookup/" + number
    response = requests.request("GET", url, headers=headers)
    response_json = json.loads(response.text)
    return response_json

def get_advanced_number_lookup_result():
    number = phone_number_entry.get()
    result = get_advanced_number_lookup(number)
    advanced_number_lookup_entry.config(state='normal')
    advanced_number_lookup_entry.delete(0, END)
    advanced_number_lookup_entry.insert(0, result)

# Lookup button
lookup_button = Button(root, text="Lookup", font=("Segoe UI", 10), command=get_advanced_number_lookup_result)
lookup_button.grid(row=6, column=1, padx=5, pady=5, sticky=W)

# message_entry = Text(root, height=5, width=30, font=("Segoe UI", 10), wrap=WORD)
# message_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky=W)

# # Advanced number lookup entry
advanced_number_lookup_entry = Entry(root, height=5, width=30, font=("Segoe UI", 10), state='readonly', wrap=WORD)
advanced_number_lookup_entry.grid(row=3, column=5, padx=5, pady=5, sticky=W, columnspan=2)

# pause_button = Button(root, text="Pause", command=pause_script, font=("Segoe UI", 10))
# pause_button.grid(row=6, column=1, padx=3, pady=3, sticky=W)



root.mainloop()

# https://textbelt.com/purchase/?generateKey=1 will get you the API Key
# e2083c182717842a1d4e7dacb2d374af8RAqXQc1ex0kff
