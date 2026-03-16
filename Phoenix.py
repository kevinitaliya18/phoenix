# import pyttsx3
# import speech_recognition as sr
# from datetime import date
# import time
# import webbrowser
# import datetime
# from pynput.keyboard import Key, Controller
# import pyautogui
# import sys
# import os
# from os import listdir
# from os.path import isfile, join
# import smtplib
# import wikipedia
# import subprocess
# import app
# from threading import Thread
# import pyperclip  # Added for clipboard operations
# import subprocess  # Added for system control commands

# shutdown_scheduled = False
# today = date.today()
# r = sr.Recognizer()
# keyboard = Controller()
# engine = pyttsx3.init("sapi5")
# engine.setProperty('rate', 180)
# engine.setProperty("voice", engine.getProperty("voices")[1].id)

# file_exp_status = False
# files = []
# path = ""
# is_awake = True
# voice_typing_mode = False  # Added for voice typing mode
# voice_command_mode = False  # Added for voice command mode

# def reply(message):
#     print(message)


# def reply(audio):
#     app.ChatBot.addAppMsg(audio)
#     print(audio)
#     engine.say(audio)
#     engine.runAndWait()


# def wish():
#     hour = int(datetime.datetime.now().hour)

#     if hour >= 0 and hour < 12:
#         reply("Good Morning!")
#     elif hour >= 12 and hour < 18:
#         reply("Good Afternoon!")
#     else:
#         reply("Good Evening!")

#     reply("I am Phoenix, How May I Help You?")


# with sr.Microphone() as source:
#     r.energy_threshold = 500
#     r.dynamic_energy_threshold = False


# def record_audio():
#     with sr.Microphone() as source:
#         r.pause_threshold = 0.8
#         voice_data = ""
#         audio = r.listen(source, phrase_time_limit=5)

#         try:
#             voice_data = r.recognize_google(audio)
#         except sr.RequestError:
#             reply("Sorry My Service Is Down. Please Check Your Internet Connection.")
#         except sr.UnknownValueError:
#             print("Cannot Recognize.")
#             pass
#         return voice_data.lower()


# # Added function for voice typing mode
# def voice_typing():
#     reply("Voice typing activated. Speak to type. Say 'stop typing' to exit.")
#     while voice_typing_mode:
#         text = record_audio()
#         if "stop typing" in text:
#             reply("Voice typing stopped.")
#             break
#         pyautogui.write(text + " ")
#         time.sleep(0.5)


# def respond(voice_data):
#     global file_exp_status, files, is_awake, path, voice_typing_mode, voice_command_mode
#     print(voice_data)
#     voice_data = voice_data.replace("phoenix", "")
#     app.eel.addUserMsg(voice_data)

#     if not is_awake:
#         if "wake up" in voice_data:
#             is_awake = True
#             wish()

#     elif "hello" in voice_data:
#         wish()

#     elif "what is your name" in voice_data:
#         reply("My Name Is Phoenix!")

#     elif "date" in voice_data:
#         reply(today.strftime("%B %d, %Y"))

#     elif "time" in voice_data:
#         reply(str(datetime.datetime.now()).split(" ")[1].split(".")[0])

#     elif "search" in voice_data:
#         query = voice_data.split("search")[1].strip()
#         reply(f"Searching for {query}")
#         url = f"https://google.com/search?q={query}"
#         try:
#             webbrowser.get().open(url)
#             reply("This Is What I Found Sir On Google.")
#         except:
#             reply("Please Check Your Internet.")

#     elif "location" in voice_data:
#         reply("Which Place Are You Looking For?")
#         temp_audio = record_audio()
#         app.eel.addUserMsg(temp_audio)
#         reply("Locating...")
#         url = f"https://google.nl/maps/place/{temp_audio}/&amp;"
#         try:
#             webbrowser.get().open(url)
#             reply("This Is What I Found Sir On Google.")
#         except:
#             reply("Please Check Your Internet.")

#     elif "bye" in voice_data or "by" in voice_data:
#         reply("Good Bye Sir! Have A Nice Day.")
#         is_awake = False

    

# # Inside the respond function (insert within command checks):

#     # Power Controls
#     elif "shutdown the pc" in voice_data:
#         shutdown_scheduled = True
#         reply("Shutting down in 10 seconds. Say 'cancel shutdown' to abort.")
#         for i in range(10, 0, -1):
#             if not shutdown_scheduled:
#                 reply("Shutdown cancelled.")
#                 break
#             time.sleep(1)
#         if shutdown_scheduled:
#             os.system("shutdown /s /t 1")

#     elif "cancel shutdown" in voice_data:
#         shutdown_scheduled = False
#         os.system("shutdown /a")
#         reply("Shutdown aborted.")

#     elif "restart computer" in voice_data:
#         os.system("shutdown /r /t 1")
#         reply("Restarting computer.")

#     elif "lock computer" in voice_data:
#         os.system("rundll32.exe user32.dll,LockWorkStation")
#         reply("Computer locked.")

#     # Volume Controls
#     elif "mute" in voice_data:
#         pyautogui.press("volumemute")
#         reply("Muted.")

#     elif "unmute" in voice_data:
#         pyautogui.press("volumemute")
#         reply("Unmuted.")

#     elif "volume up" in voice_data:
#         pyautogui.press("volumeup")
#         reply("Volume increased.")

#     elif "volume down" in voice_data:
#         pyautogui.press("volumedown")
#         reply("Volume decreased.")

#     elif "volume max" in voice_data:
#         for _ in range(50):
#             pyautogui.press("volumeup")
#         reply("Volume set to maximum.")

#     # Window Management
#     elif "maximize window" in voice_data:
#         pyautogui.hotkey("win", "up")
#         reply("Window maximized.")

#     elif "minimize window" in voice_data:
#         pyautogui.hotkey("win", "down")
#         reply("Window minimized.")

#     elif "show desktop" in voice_data:
#         pyautogui.hotkey("win", "d")
#         reply("Showing desktop.")

#     elif "switch window" in voice_data:
#         pyautogui.keyDown("alt")
#         pyautogui.press("tab")
#         pyautogui.keyUp("alt")
#         reply("Switched window.")

#     # System Tools
#     elif "open task manager" in voice_data:
#         pyautogui.hotkey("ctrl", "shift", "esc")
#         reply("Task manager opened.")

#     elif "take screenshot" in voice_data:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         screenshot_path = os.path.join(os.getcwd(), f"screenshot_{timestamp}.png")
#         pyautogui.screenshot(screenshot_path)
#         reply("Screenshot taken and saved.")

#     elif "list files" in voice_data:
#         counter = 0
#         path = os.getcwd()
#         files = listdir(path)
#         filestr = ""
#         for f in files:
#             counter += 1
#             filestr += str(counter) + ":  " + f + "<br>"
#         file_exp_status = True
#         reply("These Are The Files In Your Current Directory.")
#         app.ChatBot.addAppMsg(filestr)

#     # Voice Typing
#     elif "start typing" in voice_data:
#         voice_typing_mode = True
#         reply("Voice typing mode on. Speak and I'll type for you.")
#         t = Thread(target=voice_typing)
#         t.start()

#     elif "stop typing" in voice_data:
#         voice_typing_mode = False
#         reply("Voice typing mode off.")


#     # Emergency cancel
#     elif "cancel" in voice_data:
#         if "typing" in voice_data:
#             voice_typing_mode = False
#             reply("Voice typing cancelled.")
#         elif "shutdown" in voice_data:
#             shutdown_scheduled = False
#             os.system("shutdown /a")
#             reply("Shutdown cancelled.")

#     # 1. Voice Command Mode (On/Off)
#     elif "voice command mode" in voice_data:
#         if "on" in voice_data:
#             voice_command_mode = True
#             reply("Voice command mode activated.")
#         elif "off" in voice_data:
#             voice_command_mode = False
#             reply("Voice command mode deactivated.")

#     # 2. Open (App_Name/File_Name) - Already implemented
#     elif "open" in voice_data and not file_exp_status:
#         app_name = voice_data.replace("open", "").strip()
#         try:
#             os.startfile(app_name)
#             reply(f"Opened {app_name}.")
#         except Exception:
#             reply(f"Failed to open {app_name}. Please check the name or file.")

#     # 3. Exit (App_Name/File_Name)
#     elif "exit" in voice_data and not ("terminate" in voice_data):
#         app_name = voice_data.replace("exit", "").strip()
#         try:
#             # Using taskkill to close an application
#             os.system(f"taskkill /f /im {app_name}.exe")
#             reply(f"Closed {app_name}.")
#         except Exception:
#             reply(f"Failed to close {app_name}.")

#     # 4. Window Maximise (App_Name/File_Name)
#     elif "maximise window" in voice_data:
#         pyautogui.hotkey("alt", "space")
#         pyautogui.press("x")
#         reply("Window maximized.")

#     # 5. Window Minimise (App_Name/File_Name)
#     elif "minimise window" in voice_data:
#         pyautogui.hotkey("alt", "space")
#         pyautogui.press("n")
#         reply("Window minimized.")

#     # 7. Edit
#     elif "edit" in voice_data:
#         # This could mean different things in different contexts
#         # For example, it could select text for editing
#         pyautogui.hotkey("ctrl", "a")
#         reply("Ready to edit.")

#     # 8. Insert
#     elif "insert" in voice_data and not ("tab" in voice_data or "whitespace" in voice_data):
#         reply("What would you like to insert?")
#         text_to_insert = record_audio()
#         app.eel.addUserMsg(text_to_insert)
#         pyautogui.write(text_to_insert)
#         reply(f"Inserted: {text_to_insert}")

#     # 9. Insert Tab
#     elif "insert tab" in voice_data:
#         keyboard.press(Key.tab)
#         keyboard.release(Key.tab)
#         reply("Tab inserted.")

#     # 10. Insert Whitespace
#     elif "insert whitespace" in voice_data:
#         keyboard.press(Key.space)
#         keyboard.release(Key.space)
#         reply("Whitespace inserted.")

#     # 11. Go To (Word_Name)
#     elif "go to" in voice_data and not ("start" in voice_data or "end" in voice_data):
#         word = voice_data.replace("go to", "").strip()
#         # First select all text to search within
#         pyautogui.hotkey("ctrl", "a")
#         # Copy it to use find functionality
#         pyautogui.hotkey("ctrl", "c")
#         # Now search for the word
#         pyautogui.hotkey("ctrl", "f")
#         pyautogui.write(word)
#         pyautogui.press("enter")
#         reply(f"Navigated to {word}.")

#     # 12. Go After Word (Word_Name)
#     elif "go after word" in voice_data:
#         word = voice_data.replace("go after word", "").strip()
#         # Similar to above but move cursor after finding
#         pyautogui.hotkey("ctrl", "f")
#         pyautogui.write(word)
#         pyautogui.press("enter")
#         # Move right to position after the word
#         for _ in range(len(word)):
#             pyautogui.press("right")
#         reply(f"Positioned after {word}.")

#     # 13. Go To Start Of Paragraph
#     elif "go to start of paragraph" in voice_data:
#         pyautogui.hotkey("ctrl", "up")
#         reply("Moved to start of paragraph.")

#     # 14. Go To Start Of Document
#     elif "go to start of document" in voice_data:
#         pyautogui.hotkey("ctrl", "home")
#         reply("Moved to start of document.")

#     # 15. Go To End Of Sentence
#     elif "go to end of sentence" in voice_data:
#         # This is approximate - look for period and move after it
#         pyautogui.hotkey("ctrl", "f")
#         pyautogui.write(".")
#         pyautogui.press("enter")
#         pyautogui.press("right")
#         reply("Moved to end of sentence.")

#     # 16. Select Word (Word_Name)
#     elif "select word" in voice_data:
#         word = voice_data.replace("select word", "").strip()
#         pyautogui.hotkey("ctrl", "f")
#         pyautogui.write(word)
#         pyautogui.press("enter")
#         # Select the word by holding shift and pressing right
#         pyautogui.keyDown("shift")
#         for _ in range(len(word)):
#             pyautogui.press("right")
#         pyautogui.keyUp("shift")
#         reply(f"Selected {word}.")

#     # 17. Select
#     elif voice_data.strip() == "select":
#         # Select the current word
#         pyautogui.hotkey("ctrl", "shift", "right")
#         reply("Selection made.")

#     # 18. Clear
#     elif "clear" in voice_data:
#         pyautogui.hotkey("ctrl", "a")
#         pyautogui.press("delete")
#         reply("Cleared.")

#     # 19. Cut
#     elif "cut" in voice_data:
#         pyautogui.hotkey("ctrl", "x")
#         reply("Cut.")

#     # 20. Paste
#     elif "paste" in voice_data:
#         with keyboard.pressed(Key.ctrl):
#             keyboard.press("v")
#             keyboard.release("v")
#         reply("Pasted.")

#     # 21. Delete
#     elif "delete" in voice_data:
#         pyautogui.press("delete")
#         reply("Deleted.")

#     # 22. Backspace
#     elif "backspace" in voice_data:
#         pyautogui.press("backspace")
#         reply("Backspace pressed.")

#     # 23. Caps Word
#     elif "caps word" in voice_data:
#         # First select the word
#         pyautogui.hotkey("ctrl", "shift", "right")
#         # Copy it
#         pyautogui.hotkey("ctrl", "c")
#         # Get the text and capitalize first letter
#         clipboard_text = pyperclip.paste()
#         pyautogui.press("delete")
#         pyautogui.write(clipboard_text.capitalize())
#         reply("Capitalized word.")

#     # 24. All Caps Word
#     elif "all caps word" in voice_data:
#         # Select word
#         pyautogui.hotkey("ctrl", "shift", "right")
#         # Copy it
#         pyautogui.hotkey("ctrl", "c")
#         # Delete it
#         pyautogui.press("delete")
#         # Type it in uppercase
#         clipboard_text = pyperclip.paste().upper()
#         pyautogui.write(clipboard_text)
#         reply("Word in all caps.")

#     # 25. No Caps Word
#     elif "no caps word" in voice_data:
#         # Select word
#         pyautogui.hotkey("ctrl", "shift", "right")
#         # Copy it
#         pyautogui.hotkey("ctrl", "c")
#         # Delete it
#         pyautogui.press("delete")
#         # Type it in lowercase
#         clipboard_text = pyperclip.paste().lower()
#         pyautogui.write(clipboard_text)
#         reply("Word in lowercase.")

#     # 26. Press (Key_Name)
#     elif "press" in voice_data:
#         key_name = voice_data.replace("press", "").strip()
#         pyautogui.press(key_name)
#         reply(f"Pressed {key_name}.")

#     # 27. Enter
#     elif voice_data.strip() == "enter":
#         pyautogui.press("enter")
#         reply("Enter pressed.")

#     # 28. Page Up
#     elif "page up" in voice_data:
#         pyautogui.press("pageup")
#         reply("Page up.")

#     # 29. Page Down
#     elif "page down" in voice_data:
#         pyautogui.press("pagedown")
#         reply("Page down.")

#     # 30. Home
#     elif voice_data.strip() == "home":
#         pyautogui.press("home")
#         reply("Moved to start of line.")

#     # 31. End
#     elif voice_data.strip() == "end":
#         pyautogui.press("end")
#         reply("Moved to end of line.")

#     # 32. Tab
#     elif voice_data.strip() == "tab":
#         pyautogui.press("tab")
#         reply("Tab pressed.")

#     # 33. File
#     elif voice_data.strip() == "file":
#         pyautogui.hotkey("alt", "f")
#         reply("File menu opened.")

#     # 34. Start
#     elif voice_data.strip() == "start":
#         pyautogui.press("win")
#         reply("Start menu opened.")

#     # 35. View
#     elif voice_data.strip() == "view":
#         pyautogui.hotkey("alt", "v")
#         reply("View menu opened.")

#     # 36. Recycle Bin
#     elif "recycle bin" in voice_data:
#         os.startfile("shell:RecycleBinFolder")
#         reply("Recycle bin opened.")

#     # 37. Computer
#     elif voice_data.strip() == "computer":
#         os.startfile("shell:MyComputerFolder")
#         reply("Computer opened.")

#     # 38. Show Desktop
#     elif "show desktop" in voice_data:
#         pyautogui.hotkey("win", "d")
#         reply("Desktop shown.")

#     # 39. Copy
#     elif "copy" in voice_data:
#         with keyboard.pressed(Key.ctrl):
#             keyboard.press("c")
#             keyboard.release("c")
#         reply("Copied.")

#     # 40. Scroll Up
#     elif "scroll up" in voice_data:
#         pyautogui.scroll(10)
#         reply("Scrolled up.")

#     # 41. Scroll Down
#     elif "scroll down" in voice_data:
#         pyautogui.scroll(-10)
#         reply("Scrolled down.")

#     # Handle file explorer status
#     elif file_exp_status:
#         counter = 0
#         if "open" in voice_data:
#             if isfile(join(path, files[int(voice_data.split(" ")[-1]) - 1])):
#                 os.startfile(path + files[int(voice_data.split(" ")[-1]) - 1])
#                 file_exp_status = False
#             else:
#                 try:
#                     path = path + files[int(voice_data.split(" ")[-1]) - 1] + "//"
#                     files = listdir(path)
#                     filestr = ""
#                     for f in files:
#                         counter += 1
#                         filestr += str(counter) + ":  " + f + "<br>"
#                     reply("Opened Successfully.")
#                     app.ChatBot.addAppMsg(filestr)
#                 except:
#                     reply("You Do Not Have Permission To Access This Folder.")

#         if "back" in voice_data:
#             filestr = ""
#             if path == "C://":
#                 reply("Sorry, This Is The Root Directory.")
#             else:
#                 a = path.split("//")[:-2]
#                 path = "//".join(a)
#                 path += "//"
#                 files = listdir(path)
#                 for f in files:
#                     counter += 1
#                     filestr += str(counter) + ":  " + f + "<br>"
#                 reply("ok")
#                 app.ChatBot.addAppMsg(filestr)

#     elif "list" in voice_data:
#         counter = 0
#         path = "C://"
#         files = listdir(path)
#         filestr = ""
#         for f in files:
#             counter += 1
#             filestr += str(counter) + ":  " + f + "<br>"
#         file_exp_status = True
#         reply("These Are The Files In Your Root Directory.")
#         app.ChatBot.addAppMsg(filestr)

#     else:
#         reply("I Am Not Functioned To Do This!")


# t1 = Thread(target=app.ChatBot.start)
# t1.start()

# while not app.ChatBot.started:
#     time.sleep(0.5)

# wish()
# voice_data = None
# while True:
#     if app.ChatBot.isUserInput():
#         voice_data = app.ChatBot.popUserInput()
#     else:
#         voice_data = record_audio()

#     if "phoenix" in voice_data:
#         try:
#             respond(voice_data)
#         except SystemExit:
#             reply("Exit Successful.")
#             break
#         except Exception as e:
#             print(f"EXCEPTION: {e}")
#             break

import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import subprocess
import app
from threading import Thread
import pyperclip  # Added for clipboard operations
import subprocess  # Added for system control commands
import re  # Added for better keyword matching

shutdown_scheduled = False
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init("sapi5")
engine.setProperty('rate', 180)
engine.setProperty("voice", engine.getProperty("voices")[1].id)

file_exp_status = False
files = []
path = ""
is_awake = True
voice_typing_mode = False  # Added for voice typing mode
voice_command_mode = False  # Added for voice command mode

# Common application name mappings
app_name_mappings = {
    # Browsers
    "chrome": "chrome",
    "google chrome": "chrome",
    "firefox": "firefox",
    "mozilla firefox": "firefox",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "brave": "brave",
    
    # Code Editors/IDEs
    "vs code": "code",
    "visual studio code": "code",
    "vscode": "code",
    "pycharm": "pycharm",
    "intellij": "idea",
    "intellij idea": "idea",
    "sublime text": "sublime_text",
    "sublime": "sublime_text",
    "atom": "atom",
    "notepad++": "notepad++",
    "npp": "notepad++",
    
    # Microsoft Office
    "word": "winword",
    "microsoft word": "winword",
    "excel": "excel",
    "microsoft excel": "excel",
    "powerpoint": "powerpnt",
    "microsoft powerpoint": "powerpnt",
    "outlook": "outlook",
    "microsoft outlook": "outlook",
    "onenote": "onenote",
    "microsoft onenote": "onenote",
    
    # Communication Apps
    "discord": "Discord",
    "slack": "slack",
    "teams": "teams",
    "microsoft teams": "teams",
    "zoom": "Zoom",
    "skype": "Skype",
    "telegram": "Telegram",
    "whatsapp": "WhatsApp",
    
    # Media Players
    "spotify": "Spotify",
    "vlc": "vlc",
    "vlc media player": "vlc",
    "windows media player": "wmplayer",
    "music player": "wmplayer",
    "video player": "vlc",
    
    # System Tools
    "task manager": "Taskmgr",
    "control panel": "control",
    "settings": "ms-settings:",
    "file explorer": "explorer",
    "explorer": "explorer",
    "calculator": "calc",
    "notepad": "notepad",
    "paint": "mspaint",
    "command prompt": "cmd",
    "cmd": "cmd",
    "powershell": "powershell",
    "terminal": "cmd",
    
    # Games
    "steam": "steam",
    "epic games": "EpicGamesLauncher",
    "minecraft": "Minecraft",
    "fortnite": "Fortnite",
    
    # Others
    "adobe reader": "AcroRd32",
    "acrobat reader": "AcroRd32",
    "pdf reader": "AcroRd32",
    "photoshop": "Photoshop",
    "adobe photoshop": "Photoshop",
    "illustrator": "Illustrator",
    "adobe illustrator": "Illustrator"
}

def reply(message):
    print(message)


def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        reply("Good Morning!")
    elif hour >= 12 and hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")

    reply("I am Phoenix, How May I Help You?")


with sr.Microphone() as source:
    r.energy_threshold = 500
    r.dynamic_energy_threshold = False


def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ""
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply("Sorry My Service Is Down. Please Check Your Internet Connection.")
        except sr.UnknownValueError:
            print("Cannot Recognize.")
            pass
        return voice_data.lower()


# Added function for voice typing mode
def voice_typing():
    reply("Voice typing activated. Speak to type. Say 'stop typing' to exit.")
    while voice_typing_mode:
        text = record_audio()
        if "stop typing" in text:
            reply("Voice typing stopped.")
            break
        pyautogui.write(text + " ")
        time.sleep(0.5)


def get_app_name(spoken_name):
    """Convert spoken app name to actual executable name"""
    spoken_name = spoken_name.lower().strip()
    
    # Check direct mapping
    if spoken_name in app_name_mappings:
        return app_name_mappings[spoken_name]
    
    # Check partial matches
    for key, value in app_name_mappings.items():
        if key in spoken_name or spoken_name in key:
            return value
    
    # If no mapping found, return the original (might still work)
    return spoken_name


def check_keywords(voice_data, keywords):
    """Check if any of the keywords are present in voice_data"""
    voice_data = voice_data.lower()
    for keyword in keywords:
        if keyword in voice_data:
            return True
    return False


def respond(voice_data):
    global file_exp_status, files, is_awake, path, voice_typing_mode, voice_command_mode
    print(voice_data)
    
    # Remove "phoenix" from the command for cleaner processing
    voice_data = voice_data.replace("phoenix", "").strip()
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if check_keywords(voice_data, ["wake up", "wakeup", "hello phoenix", "hey phoenix"]):
            is_awake = True
            wish()

    # Basic greetings and info
    elif check_keywords(voice_data, ["hello", "hi", "hey"]):
        wish()

    elif check_keywords(voice_data, ["what is your name", "your name", "who are you"]):
        reply("My Name Is Phoenix!")

    elif check_keywords(voice_data, ["date", "today's date", "what is the date"]):
        reply(today.strftime("%B %d, %Y"))

    elif check_keywords(voice_data, ["time", "current time", "what time is it"]):
        reply(str(datetime.datetime.now()).split(" ")[1].split(".")[0])

    # Search functionality
    elif check_keywords(voice_data, ["search for", "google search", "search"]):
        # Extract search query
        query = re.sub(r'(search for|google search|search)', '', voice_data, flags=re.IGNORECASE).strip()
        if not query:
            reply("What would you like me to search for?")
            query = record_audio()
            app.eel.addUserMsg(query)
        
        reply(f"Searching for {query}")
        url = f"https://google.com/search?q={query}"
        try:
            webbrowser.get().open(url)
            reply("This Is What I Found Sir On Google.")
        except:
            reply("Please Check Your Internet.")

    # Location search
    elif check_keywords(voice_data, ["location", "find location", "where is", "map of"]):
        if "where is" in voice_data:
            place = re.sub(r'where is', '', voice_data, flags=re.IGNORECASE).strip()
        elif "map of" in voice_data:
            place = re.sub(r'map of', '', voice_data, flags=re.IGNORECASE).strip()
        else:
            reply("Which Place Are You Looking For?")
            place = record_audio()
            app.eel.addUserMsg(place)
        
        reply(f"Locating {place}...")
        url = f"https://google.nl/maps/place/{place}/&amp;"
        try:
            webbrowser.get().open(url)
            reply("This Is What I Found Sir On Google.")
        except:
            reply("Please Check Your Internet.")

    # Voice typing activation - handles multiple phrasings
    elif check_keywords(voice_data, ["start typing", "begin typing", "activate typing", "enable typing", 
                                     "start voice typing", "begin voice typing", "activate voice typing", 
                                     "enable voice typing", "typing mode"]):
        voice_typing_mode = True
        reply("Voice typing mode on. Speak and I'll type for you.")
        t = Thread(target=voice_typing)
        t.start()

    # Open applications/files - handles multiple phrasings
    elif check_keywords(voice_data, ["open ", "launch ", "start ", "run "]) and not file_exp_status:
        # Extract the app name
        app_name = voice_data.lower()
        for word in ["open ", "launch ", "start ", "run "]:
            if word in app_name:
                app_name = app_name.split(word)[-1].strip()
                break
        
        # Clean up common phrases
        app_name = re.sub(r'(please|would you|can you|could you|pls)', '', app_name, flags=re.IGNORECASE).strip()
        
        # Get the actual executable name
        executable = get_app_name(app_name)
        
        try:
            os.startfile(executable)
            reply(f"Opened {app_name}.")
        except Exception as e:
            # Try with .exe extension
            try:
                os.startfile(executable + ".exe")
                reply(f"Opened {app_name}.")
            except Exception:
                # Try searching in common paths
                common_paths = [
                    os.path.expandvars(r"%ProgramFiles%"),
                    os.path.expandvars(r"%ProgramFiles(x86)%"),
                    os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
                    os.path.expandvars(r"%APPDATA%"),
                    "C:\\Windows\\System32"
                ]
                
                found = False
                for base_path in common_paths:
                    for root, dirs, files in os.walk(base_path):
                        for file in files:
                            if file.lower().startswith(executable.lower()) and file.lower().endswith('.exe'):
                                os.startfile(os.path.join(root, file))
                                reply(f"Opened {app_name}.")
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                
                if not found:
                    reply(f"Failed to open {app_name}. Please check if it's installed.")

    # Exit/Close applications - handles multiple phrasings
    elif check_keywords(voice_data, ["close ", "exit ", "terminate ", "quit ", "stop "]) and not ("shutdown" in voice_data):
        # Extract the app name
        app_name = voice_data.lower()
        for word in ["close ", "exit ", "terminate ", "quit ", "stop "]:
            if word in app_name:
                app_name = app_name.split(word)[-1].strip()
                break
        
        # Clean up common phrases
        app_name = re.sub(r'(please|would you|can you|could you|pls)', '', app_name, flags=re.IGNORECASE).strip()
        
        # Get the actual executable name
        executable = get_app_name(app_name)
        
        try:
            # Using taskkill to close an application
            os.system(f"taskkill /f /im {executable}.exe 2>nul")
            reply(f"Closed {app_name}.")
        except Exception:
            reply(f"Failed to close {app_name}. Make sure it's running.")

    # Shutdown PC - with multiple phrasings
    elif check_keywords(voice_data, ["shutdown", "shut down", "turn off", "power off"]):
        global shutdown_scheduled
        shutdown_scheduled = True
        reply("Shutting down in 10 seconds. Say 'cancel shutdown' to abort.")
        for i in range(10, 0, -1):
            if not shutdown_scheduled:
                reply("Shutdown cancelled.")
                break
            time.sleep(1)
        if shutdown_scheduled:
            os.system("shutdown /s /t 1")

    elif check_keywords(voice_data, ["cancel shutdown", "abort shutdown", "stop shutdown"]):
        shutdown_scheduled = False
        os.system("shutdown /a")
        reply("Shutdown aborted.")

    # Restart computer
    elif check_keywords(voice_data, ["restart", "reboot"]):
        os.system("shutdown /r /t 1")
        reply("Restarting computer.")

    # Lock computer
    elif check_keywords(voice_data, ["lock", "lock computer", "lock pc"]):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        reply("Computer locked.")

    # Volume Controls - with multiple phrasings
    elif check_keywords(voice_data, ["mute", "silence"]):
        pyautogui.press("volumemute")
        reply("Muted.")

    elif check_keywords(voice_data, ["unmute", "unmute sound"]):
        pyautogui.press("volumemute")
        reply("Unmuted.")

    elif check_keywords(voice_data, ["volume up", "increase volume", "turn up volume"]):
        pyautogui.press("volumeup")
        reply("Volume increased.")

    elif check_keywords(voice_data, ["volume down", "decrease volume", "turn down volume"]):
        pyautogui.press("volumedown")
        reply("Volume decreased.")

    elif check_keywords(voice_data, ["volume max", "maximum volume", "full volume", "volume 100"]):
        for _ in range(50):
            pyautogui.press("volumeup")
        reply("Volume set to maximum.")

    # Window Management
    elif check_keywords(voice_data, ["maximize", "full screen"]):
        pyautogui.hotkey("win", "up")
        reply("Window maximized.")

    elif check_keywords(voice_data, ["minimize", "hide window"]):
        pyautogui.hotkey("win", "down")
        reply("Window minimized.")

    elif check_keywords(voice_data, ["show desktop", "hide all windows", "desktop"]):
        pyautogui.hotkey("win", "d")
        reply("Showing desktop.")

    elif check_keywords(voice_data, ["switch window", "next window", "switch app"]):
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        pyautogui.keyUp("alt")
        reply("Switched window.")

    # System Tools
    elif check_keywords(voice_data, ["open task manager", "task manager", "launch task manager"]):
        pyautogui.hotkey("ctrl", "shift", "esc")
        reply("Task manager opened.")

    elif check_keywords(voice_data, ["take screenshot", "screenshot", "capture screen"]):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(os.getcwd(), f"screenshot_{timestamp}.png")
        pyautogui.screenshot(screenshot_path)
        reply("Screenshot taken and saved.")

    elif check_keywords(voice_data, ["list files", "show files", "files in directory"]):
        counter = 0
        path = os.getcwd()
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            filestr += str(counter) + ":  " + f + "<br>"
        file_exp_status = True
        reply("These Are The Files In Your Current Directory.")
        app.ChatBot.addAppMsg(filestr)

    # Stop typing
    elif check_keywords(voice_data, ["stop typing", "end typing", "disable typing", "deactivate typing"]):
        voice_typing_mode = False
        reply("Voice typing mode off.")

    # Emergency cancel
    elif check_keywords(voice_data, ["cancel", "abort", "stop"]):
        if voice_typing_mode:
            voice_typing_mode = False
            reply("Voice typing cancelled.")
        elif shutdown_scheduled:
            shutdown_scheduled = False
            os.system("shutdown /a")
            reply("Shutdown cancelled.")

    # Voice Command Mode
    elif check_keywords(voice_data, ["voice command mode", "command mode"]):
        if any(word in voice_data for word in ["on", "enable", "activate", "start"]):
            voice_command_mode = True
            reply("Voice command mode activated.")
        elif any(word in voice_data for word in ["off", "disable", "deactivate", "stop"]):
            voice_command_mode = False
            reply("Voice command mode deactivated.")

    # Edit commands
    elif "edit" in voice_data:
        pyautogui.hotkey("ctrl", "a")
        reply("Ready to edit.")

    # Insert text
    elif check_keywords(voice_data, ["insert", "type"]):
        if not ("tab" in voice_data or "whitespace" in voice_data or "space" in voice_data):
            reply("What would you like to insert?")
            text_to_insert = record_audio()
            app.eel.addUserMsg(text_to_insert)
            pyautogui.write(text_to_insert)
            reply(f"Inserted: {text_to_insert}")

    # Insert Tab
    elif check_keywords(voice_data, ["insert tab", "tab key"]):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        reply("Tab inserted.")

    # Insert Whitespace/Space
    elif check_keywords(voice_data, ["insert whitespace", "insert space", "space key"]):
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        reply("Whitespace inserted.")

    # Go To functionality
    elif check_keywords(voice_data, ["go to", "navigate to", "find"]) and not check_keywords(voice_data, ["start", "end"]):
        word = re.sub(r'(go to|navigate to|find)', '', voice_data, flags=re.IGNORECASE).strip()
        if word:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")
            pyautogui.hotkey("ctrl", "f")
            pyautogui.write(word)
            pyautogui.press("enter")
            reply(f"Navigated to {word}.")

    # Go After Word
    elif "go after word" in voice_data:
        word = voice_data.replace("go after word", "").strip()
        pyautogui.hotkey("ctrl", "f")
        pyautogui.write(word)
        pyautogui.press("enter")
        for _ in range(len(word)):
            pyautogui.press("right")
        reply(f"Positioned after {word}.")

    # Navigation commands
    elif check_keywords(voice_data, ["go to start of paragraph", "paragraph start"]):
        pyautogui.hotkey("ctrl", "up")
        reply("Moved to start of paragraph.")

    elif check_keywords(voice_data, ["go to start of document", "document start", "top of document"]):
        pyautogui.hotkey("ctrl", "home")
        reply("Moved to start of document.")

    elif check_keywords(voice_data, ["go to end of sentence", "sentence end"]):
        pyautogui.hotkey("ctrl", "f")
        pyautogui.write(".")
        pyautogui.press("enter")
        pyautogui.press("right")
        reply("Moved to end of sentence.")

    # Select Word
    elif "select word" in voice_data:
        word = voice_data.replace("select word", "").strip()
        pyautogui.hotkey("ctrl", "f")
        pyautogui.write(word)
        pyautogui.press("enter")
        pyautogui.keyDown("shift")
        for _ in range(len(word)):
            pyautogui.press("right")
        pyautogui.keyUp("shift")
        reply(f"Selected {word}.")

    # Basic select
    elif voice_data.strip() == "select":
        pyautogui.hotkey("ctrl", "shift", "right")
        reply("Selection made.")

    # Clear/Delete All
    elif check_keywords(voice_data, ["clear", "clear all", "delete all"]):
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        reply("Cleared.")

    # Cut
    elif check_keywords(voice_data, ["cut"]):
        pyautogui.hotkey("ctrl", "x")
        reply("Cut.")

    # Paste
    elif check_keywords(voice_data, ["paste"]):
        with keyboard.pressed(Key.ctrl):
            keyboard.press("v")
            keyboard.release("v")
        reply("Pasted.")

    # Copy
    elif check_keywords(voice_data, ["copy"]):
        with keyboard.pressed(Key.ctrl):
            keyboard.press("c")
            keyboard.release("c")
        reply("Copied.")

    # Delete
    elif check_keywords(voice_data, ["delete"]):
        pyautogui.press("delete")
        reply("Deleted.")

    # Backspace
    elif check_keywords(voice_data, ["backspace"]):
        pyautogui.press("backspace")
        reply("Backspace pressed.")

    # Text formatting
    elif "caps word" in voice_data and not "all caps" in voice_data:
        pyautogui.hotkey("ctrl", "shift", "right")
        pyautogui.hotkey("ctrl", "c")
        clipboard_text = pyperclip.paste()
        pyautogui.press("delete")
        pyautogui.write(clipboard_text.capitalize())
        reply("Capitalized word.")

    elif check_keywords(voice_data, ["all caps", "uppercase"]):
        pyautogui.hotkey("ctrl", "shift", "right")
        pyautogui.hotkey("ctrl", "c")
        pyautogui.press("delete")
        clipboard_text = pyperclip.paste().upper()
        pyautogui.write(clipboard_text)
        reply("Word in all caps.")

    elif check_keywords(voice_data, ["no caps", "lowercase"]):
        pyautogui.hotkey("ctrl", "shift", "right")
        pyautogui.hotkey("ctrl", "c")
        pyautogui.press("delete")
        clipboard_text = pyperclip.paste().lower()
        pyautogui.write(clipboard_text)
        reply("Word in lowercase.")

    # Key presses
    elif "press" in voice_data:
        key_name = voice_data.replace("press", "").strip()
        pyautogui.press(key_name)
        reply(f"Pressed {key_name}.")

    # Single key commands
    elif voice_data.strip() in ["enter", "return"]:
        pyautogui.press("enter")
        reply("Enter pressed.")

    elif check_keywords(voice_data, ["page up"]):
        pyautogui.press("pageup")
        reply("Page up.")

    elif check_keywords(voice_data, ["page down"]):
        pyautogui.press("pagedown")
        reply("Page down.")

    elif voice_data.strip() == "home":
        pyautogui.press("home")
        reply("Moved to start of line.")

    elif voice_data.strip() == "end":
        pyautogui.press("end")
        reply("Moved to end of line.")

    elif voice_data.strip() in ["tab", "tab key"]:
        pyautogui.press("tab")
        reply("Tab pressed.")

    # Menu commands
    elif voice_data.strip() == "file":
        pyautogui.hotkey("alt", "f")
        reply("File menu opened.")

    elif voice_data.strip() == "start":
        pyautogui.press("win")
        reply("Start menu opened.")

    elif voice_data.strip() == "view":
        pyautogui.hotkey("alt", "v")
        reply("View menu opened.")

    # System folders
    elif check_keywords(voice_data, ["recycle bin", "recycle"]):
        os.startfile("shell:RecycleBinFolder")
        reply("Recycle bin opened.")

    elif check_keywords(voice_data, ["computer", "this pc", "my computer"]):
        os.startfile("shell:MyComputerFolder")
        reply("Computer opened.")

    # Scrolling
    elif check_keywords(voice_data, ["scroll up"]):
        pyautogui.scroll(10)
        reply("Scrolled up.")

    elif check_keywords(voice_data, ["scroll down"]):
        pyautogui.scroll(-10)
        reply("Scrolled down.")

    # File explorer navigation
    elif file_exp_status:
        counter = 0
        if "open" in voice_data:
            if isfile(join(path, files[int(voice_data.split(" ")[-1]) - 1])):
                os.startfile(path + files[int(voice_data.split(" ")[-1]) - 1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(" ")[-1]) - 1] + "//"
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter += 1
                        filestr += str(counter) + ":  " + f + "<br>"
                    reply("Opened Successfully.")
                    app.ChatBot.addAppMsg(filestr)
                except:
                    reply("You Do Not Have Permission To Access This Folder.")

        if "back" in voice_data:
            filestr = ""
            if path == "C://":
                reply("Sorry, This Is The Root Directory.")
            else:
                a = path.split("//")[:-2]
                path = "//".join(a)
                path += "//"
                files = listdir(path)
                for f in files:
                    counter += 1
                    filestr += str(counter) + ":  " + f + "<br>"
                reply("ok")
                app.ChatBot.addAppMsg(filestr)

    # List files in root directory
    elif check_keywords(voice_data, ["list", "show all files", "list directory"]):
        counter = 0
        path = "C://"
        files = listdir(path)
        filestr = ""
        for f in files:
            counter += 1
            filestr += str(counter) + ":  " + f + "<br>"
        file_exp_status = True
        reply("These Are The Files In Your Root Directory.")
        app.ChatBot.addAppMsg(filestr)

    # Goodbye
    elif check_keywords(voice_data, ["bye", "goodbye", "see you", "exit", "quit"]):
        reply("Good Bye Sir! Have A Nice Day.")
        is_awake = False

    else:
        reply("I Am Not Functioned To Do This!")


t1 = Thread(target=app.ChatBot.start)
t1.start()

while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
    else:
        voice_data = record_audio()

    if "phoenix" in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successful.")
            break
        except Exception as e:
            print(f"EXCEPTION: {e}")
            break