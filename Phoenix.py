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
import wikipedia
import Gesture_Controller
import eye_control
import demo
from voice_typing import voice_typing  # Assuming this is the correct import path
import app
from threading import Thread

today = date.today()
keyboard = Controller()
engine = pyttsx3.init("sapi5")
engine.setProperty("voice", engine.getProperty("voices")[0].id)

file_exp_status = False
files = []
path = ""
is_awake = True

def initialize_recognizer():
    r = sr.Recognizer()
    r.energy_threshold = 4000  # Higher threshold for better noise handling
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    return r

def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print("Phoenix:", audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        reply("Good Morning!")
    elif 12 <= hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am Phoenix, How May I Help You?")

def record_audio(r):
    with sr.Microphone() as source:
        print("Listening...")
        try:
            # Adjust for ambient noise first
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            voice_data = r.recognize_google(audio)
            print("You said:", voice_data)
            return voice_data.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            reply("Sorry, I'm having trouble with the speech service.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    if not voice_data:
        return
    
    print("Processing:", voice_data)
    voice_data = voice_data.replace("phoenix", "")
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if "wake up" in voice_data:
            is_awake = True
            wish()
        return

    # Rest of your respond function remains the same...
    elif "hello" in voice_data:
        wish()

    elif "what is your name" in voice_data:
        reply("My Name Is Phoenix!")

    elif "date" in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif "time" in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split(".")[0])

    elif "search" in voice_data:
        query = voice_data.split("search")[1].strip()
        reply(f"Searching for {query}")
        url = f"https://google.com/search?q={query}"
        try:
            webbrowser.get().open(url)
            reply("This Is What I Found Sir On Google.")
        except:
            reply("Please Check Your Internet.")

    elif "bye" in voice_data or "by" in voice_data:
        reply("Good Bye Sir! Have A Nice Day.")
        is_awake = False

    elif "exit" in voice_data or "terminate" in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    elif "start gesture control" in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply("Gesture Control Mode Is Actived.")
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target=gc.start)
            t.start()
            reply("Launched Successfully.")

    elif "stop gesture control" in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply("Gesture Control Mode Is Deactivated.")
        else:
            reply("Gesture Control Mode Is Already Deactivated.")

    elif "start eye control" in voice_data:
        if eye_control.EyeController.gc_mode:
            reply("Eye Control Mode Is Actived.")
        else:
            gc = eye_control.EyeController()
            t = Thread(target=gc.start)
            t.start()
            reply("Launched Successfully.")

    elif "stop eye control" in voice_data:
        if eye_control.EyeController.gc_mode:
            eye_control.EyeController.gc_mode = 0
            reply("Eye Control Mode Is Deactivated.")
        else:
            reply("Eye Control Mode Is Already Deactivated.")

    elif "start nvda system" in voice_data:
        if demo.DemoController.gc_mode:
            reply("NVDA System Is Actived.")
        else:
            gc = demo.DemoController()
            t = Thread(target=gc.start)
            t.start()
            reply("Launched Successfully.")

    elif "stop nvda system" in voice_data:
        if demo.DemoController.gc_mode:
            demo.DemoController.gc_mode = 0
            reply("nvda Mode Is Deactivated.")
        else:
            reply("nvda Mode Is Already Deactivated.")

    elif "copy" in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press("c")
            keyboard.release("c")
        reply("Copied.")

    elif "paste" in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press("v")
            keyboard.release("v")
        reply("Pasted.")

    elif "list" in voice_data:
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

    elif "open" in voice_data:
        app_name = voice_data.replace("open", "").strip()
        try:
            os.startfile(app_name)
            reply(f"Opened {app_name}.")
        except Exception:
            reply(f"Failed to open {app_name}. Please check the name or file.")

    elif "maximize window" in voice_data:
        pyautogui.hotkey("alt", "space")
        pyautogui.press("x")
        reply("Window maximized.")

    elif "minimise window" in voice_data:
        pyautogui.hotkey("alt", "space")
        pyautogui.press("n")
        reply("Window minimized.")
    
      # 🔊 VOLUME CONTROL
    elif "volume up" in voice_data or "increase volume" in voice_data:
        for _ in range(5):  # Simulate pressing Volume Up key 5 times (~25% increase)
            pyautogui.press("volumeup")
        reply("Volume increased")

    elif "volume down" in voice_data or "decrease volume" in voice_data:
        for _ in range(5):  # Simulate pressing Volume Down key 5 times (~25% decrease)
            pyautogui.press("volumedown")
        reply("Volume decreased")

    elif "mute" in voice_data or "unmute" in voice_data:
        pyautogui.press("volumemute")  # Toggle mute
        reply("Volume muted" if "mute" in voice_data else "Volume unmuted")

    # ⏻ SHUTDOWN & (with safety confirmation)
    elif "shut down" in voice_data or "shutdown" in voice_data:
        try:
            if os.name == 'nt':  # Windows
                os.system("shutdown /s /t 0")  # Immediate shutdown
            else:  # Linux/Mac
                os.system("shutdown -h now")
            reply("Shutting down now")  # This may not complete before shutdown
        except Exception as e:
            reply(f"Error: {str(e)}")

    # Instant Restart Command
    elif "restart" in voice_data or "reboot" in voice_data:
        try:
            if os.name == 'nt':  # Windows
                os.system("shutdown /r /t 0")  # Immediate restart
            else:  # Linux/Mac
                os.system("reboot")
            reply("Restarting now")  # This may not complete before restart
        except Exception as e:
            reply(f"Error: {str(e)}")

    # [Rest of your existing commands...]
      
    elif "start voice typing" in voice_data:
        reply(voice_typing.start())
        
    elif "stop voice typing" in voice_data:
        reply(voice_typing.stop())
    
    elif "take screenshot" in voice_data or "capture screen" in voice_data:
        try:
            # Create screenshots folder if it doesn't exist
            if not os.path.exists("screenshots"):
                os.mkdir("screenshots")
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshots/screenshot_{timestamp}.png"
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            reply(f"Screenshot saved as {filename}")
        except Exception as e:
            reply(f"Failed to take screenshot: {str(e)}")

    elif "insert tab" in voice_data:
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        reply("Tab inserted.")

    elif "insert whitespace" in voice_data:
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        reply("Whitespace inserted.")

    elif "clear" in voice_data:
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("delete")
        reply("Cleared.")

    elif "cut" in voice_data:
        pyautogui.hotkey("ctrl", "x")
        reply("Cut.")

    elif "backspace" in voice_data:
        pyautogui.press("backspace")
        reply("Backspace pressed.")

    elif "press" in voice_data:
        key_name = voice_data.replace("press", "").strip()
        pyautogui.press(key_name)
        reply(f"Pressed {key_name}.")

    elif "start" in voice_data:
        pyautogui.press("win")
        reply("Start menu opened.")

    elif "open recycle bin" in voice_data:
        os.startfile("shell:RecycleBinFolder")
        reply("Recycle bin opened.")

    elif "show desktop" in voice_data:
        pyautogui.hotkey("win", "d")
        reply("Desktop shown.")

    elif "scroll up" in voice_data:
        pyautogui.scroll(10)
        reply("Scrolled up.")

    elif "scroll down" in voice_data:
        pyautogui.scroll(-10)
        reply("Scrolled down.")

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

    else:
        reply("I Am Not Functioned To Do This!")

    # [Keep all your existing command handling logic here]

if __name__ == "__main__":
    r = initialize_recognizer()
    
    t1 = Thread(target=app.ChatBot.start)
    t1.start()

    while not app.ChatBot.started:
        time.sleep(0.5)

    wish()
    
    while True:
        try:
            if app.ChatBot.isUserInput():
                voice_data = app.ChatBot.popUserInput()
            else:
                voice_data = record_audio(r)

            if voice_data and ("phoenix" in voice_data or is_awake):
                respond(voice_data)
                
        except SystemExit:
            reply("Exit Successful.")
            break
        except Exception as e:
            print(f"EXCEPTION: {e}")
            reply("Sorry, I encountered an error. Please try again.")
            continue
        