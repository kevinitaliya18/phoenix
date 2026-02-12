import os
import pyttsx3
import ctypes
import subprocess
import threading
import time

class SystemController:
    gc_mode = 0  # Class variable to track mode
    
    def __init__(self):
        SystemController.gc_mode = 1
        self.engine = pyttsx3.init()
        
    def start(self):
        try:
            self.speak("System control activated")
            while SystemController.gc_mode:
                time.sleep(0.1)
        except Exception as e:
            print(f"System control error: {e}")
        finally:
            SystemController.gc_mode = 0

    def speak(self, text):
        print(f"System Control: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def volume_up(self):
        """Increase system volume by 5%"""
        try:
            for _ in range(2):  # Increase in steps of 2 (about 5% each)
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)  # Volume Up key
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            self.speak("Volume increased")
        except Exception as e:
            self.speak(f"Failed to increase volume: {str(e)}")

    def volume_down(self):
        """Decrease system volume by 5%"""
        try:
            for _ in range(2):  # Decrease in steps of 2 (about 5% each)
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)  # Volume Down key
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            self.speak("Volume decreased")
        except Exception as e:
            self.speak(f"Failed to decrease volume: {str(e)}")

    def mute_volume(self):
        """Toggle mute status"""
        try:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)  # Volume Mute key
            ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
            self.speak("Volume toggled")
        except Exception as e:
            self.speak(f"Failed to mute volume: {str(e)}")

    def shutdown_pc(self):
        """Shutdown the computer"""
        try:
            self.speak("Shutting down computer in 5 seconds")
            time.sleep(5)
            os.system("shutdown /s /t 1")
        except Exception as e:
            self.speak(f"Failed to shutdown: {str(e)}")

    def restart_pc(self):
        """Restart the computer"""
        try:
            self.speak("Restarting computer in 5 seconds")
            time.sleep(5)
            os.system("shutdown /r /t 1")
        except Exception as e:
            self.speak(f"Failed to restart: {str(e)}")

    def abort_shutdown(self):
        """Cancel a pending shutdown"""
        try:
            os.system("shutdown /a")
            self.speak("Shutdown or restart cancelled")
        except Exception as e:
            self.speak(f"Failed to cancel shutdown: {str(e)}")

# Global mode flag for Phoenix integration
gc_mode = False
system_controller = None

def start():
    global gc_mode, system_controller
    gc_mode = True
    system_controller = SystemController()
    system_controller.start()