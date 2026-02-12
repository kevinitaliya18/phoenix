import subprocess
import sys
import pyttsx3
import keyboard
from PIL import Image, ImageGrab
import pytesseract
import pyautogui
import pywinauto
from pywinauto import Application
import speech_recognition as sr
import time
import threading
import os
from datetime import datetime
from pywinauto import Desktop
from pywinauto.application import Application
from pywinauto.uia_defines import IUIA
from pywinauto.uia_element_info import UIAElementInfo
# For Getting focus element
import win32api
import win32gui
from pywinauto.uia_defines import IUIA
from pywinauto.uia_element_info import UIAElementInfo
from ctypes.wintypes import POINT
import logging

class DemoController:      
    gc_mode = 0  # Class variable to track mode
    
    def __init__(self):
        DemoController.gc_mode = 1
        self.nvda = NVDA()  # Create NVDA instance
        
    def start(self):
        try:
            self.nvda.speak("Demo system activated")
            # Run NVDA in a separate thread
            t = threading.Thread(target=self.nvda.run)
            t.daemon = True
            t.start()
            
            while DemoController.gc_mode:
                # Keep the controller running
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Demo system error: {e}")
        finally:
            DemoController.gc_mode = 0
            self.nvda.shutdown()

class NVDA:
    def __init__(self):
        self.keyboard_nav = self.KeyboardNavigator(self)
        self.cursor_nav = self.CursorNavigator(self)
        # System state
        self.running = True
        self.voice_command_mode = False
        self.current_focus = None
        

        # Start keyboardNavigator
        self.keyboard_thread = threading.Thread(target=self.keyboard_nav.listen_continuously)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()
        

    class KeyboardNavigator:
        def __init__(self, nvda):
            self.nvda = nvda
            self.last_c_press_time = 0  # Initialize the attribute here
            self.c_press_count = 0
            logging.basicConfig(
                level=logging.INFO,
                format='[%(asctime)s] %(message)s'
            )
            self.shortcuts = {
                'insert+h': lambda: self.nvda.show_help(),
                'insert+q': lambda: self.nvda.shutdown(),
                'insert+t': lambda: self.nvda.speak(f"Current time is {datetime.now().strftime('%H:%M')}"),
                'insert+d': lambda: self.nvda.speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"),
                'insert+space': lambda: self.nvda.read_current_focus(),
                'insert+s': lambda: self.nvda.toggle_voice_command_mode(),
                'insert+up': lambda: self.nvda.cursor_nav.move_relative(0, -10),
                'insert+down': lambda: self.nvda.cursor_nav.move_relative(0, 10),
                'insert+left': lambda: self.nvda.cursor_nav.move_relative(-10, 0),
                'insert+right': lambda: self.nvda.cursor_nav.move_relative(10, 0),
                'insert+c': lambda: self.nvda.cursor_nav.click(),
                # 'insert+c': self.handle_c_key,
                'insert+r': lambda: self.nvda.cursor_nav.right_click(),
                'insert+o': lambda: self.nvda.read_clipboard_image(),
                'insert+a': lambda: self.nvda.read_active_window(),
                'insert+f5': lambda: self.nvda.refresh_screen_reader(),
            }
        def log_key_press(self, event):
            """Log only the keys that are part of defined shortcuts"""
            for shortcut in self.shortcuts:
                keys = shortcut.split('+')
                if event.name in keys:
                    logging.info(f"Shortcut key pressed: {event.name}")
                    break  # Stop checking after first match


        def handle_c_key(self):
            """Handle both single and double C key presses"""
            try:
                current_time = time.time()
                time_diff = current_time - self.last_c_press_time
                
                if time_diff < 0.5:  # 500ms threshold for double press
                    self.nvda.cursor_nav.double_click()
                    self.nvda.speak("Double clicked")
                else:
                    self.nvda.cursor_nav.click()
                    # self.nvda.speak("Clicked")
                
                self.last_c_press_time = current_time
            except Exception as e:
                self.nvda.speak(f"Error handling click: {str(e)}")

        def listen_continuously(self):
            """Listen for keyboard shortcuts continuously"""
            try:
                # Remove all existing hotkeys
                keyboard.unhook_all()
                
                # Add all hotkeys
                for shortcut, action in self.shortcuts.items():
                    keyboard.add_hotkey(shortcut, action)
                
                keyboard.on_press(self.log_key_press)
                
                # Keep the thread alive
                while self.nvda.running:
                    time.sleep(0.1)
            except Exception as e:
                self.nvda.speak(f"Keyboard error: {str(e)}")
        
        def add_shortcut(self, shortcut, action):
            """Add a new keyboard shortcut"""
            def wrapped_action():
                print(f"Hotkey triggered: {shortcut}")  # Debug print
                try:
                    action()
                except Exception as e:
                    print(f"Error in hotkey: {e}")
            self.shortcuts[shortcut] = wrapped_action
            keyboard.add_hotkey(shortcut, wrapped_action)
        
        def remove_shortcut(self, shortcut):
            """Remove a keyboard shortcut"""
            if shortcut in self.shortcuts:
                keyboard.remove_hotkey(shortcut)
    
                del self.shortcuts[shortcut]
    
    class CursorNavigator:
        def __init__(self, nvda):
            self.nvda = nvda
            self.screen_width, self.screen_height = pyautogui.size()
            self.last_position = pyautogui.position()
        
        def get_current_position(self):
            """Get current mouse position"""
            self.last_position = pyautogui.position()
            return self.last_position
        
        def move_to(self, x, y):
            """Move cursor to specific coordinates"""
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))
            pyautogui.moveTo(x, y)
            self.last_position = (x, y)
            # self.nvda.speak(f"Moved to X {x}, Y {y}")
        
        def move_relative(self, dx, dy):
            """Move cursor relative to current position"""
            current_x, current_y = self.get_current_position()
            self.move_to(current_x + dx, current_y + dy)
        
        def click(self):
            """Perform a mouse click"""
            pyautogui.click()
            self.nvda.speak("Clicked")
        
        def double_click(self):
            """Perform a double click"""
            pyautogui.doubleClick()
            self.nvda.speak("Double clicked")
        
        def right_click(self):
            """Perform a right click"""
            pyautogui.rightClick()
            self.nvda.speak("Right clicked")
        
        def get_element_at_cursor(self):
            """Simulate getting element info at cursor"""
            x, y = self.get_current_position()
            try:
                app = Application(backend='uia').connect(active=True)
                element = app.window().from_point(x, y)
                name = element.element_info.name
                control_type = element.element_info.control_type
                return f"{control_type}: {name if name else 'Unnamed element'}"
            except:
                return f"Element at X {x}, Y {y}"
    
    
    
    # Methods in NVDA class

    def run(self):
        """Main interaction loop"""
        self.speak("NVDA system ready")
        while self.running:
            if self.voice_command_mode:
                self.voice_cmd.listen()
            time.sleep(0.1) 

    def speak(self,text):
        engine = pyttsx3.init()
        print(f"🔊 Speaking: {text}")
        engine.say(text)
        engine.runAndWait()   

    def show_help(self):
        """Display help information"""
        help_text = """
            NVDA System Help:
            Keyboard Shortcuts:
            - Insert+H: Show this help
            - Insert+Q: Quit NVDA
            - Insert+T: Speak current time
            - Insert+D: Speak current date
            - Insert+Space: Read current focus
            - Insert+S: Toggle voice command mode
            - Insert+Arrow Keys: Move cursor
            - Insert+C: Click
            - Insert+C+C: Double click
            - Insert+R: Right click
            - Insert+O: Read clipboard image text
            - Insert+A: Read active window info
            - Insert+F5: Refresh screen reader

            Voice Commands (when in voice mode):
            - "help", "time", "date", "stop", 
            - "click", "double click", "right click"
            - "move up/down/left/right"
            - "read window", "read clipboard"
            """
        self.speak(help_text)
    
    def shutdown(self):
        """Shutdown the NVDA system"""
        self.speak("Shutting down NVDA system")
        self.running = False
        keyboard.unhook_all()  # Clean up keyboard hooks
        if hasattr(self, 'keyboard_thread'):
            self.keyboard_thread.join(timeout=1)  # Wait for thread to finish
        sys.exit(0)


    def read_current_focus(self):
        if hasattr(self, 'focus_thread') and self.focus_thread.is_alive():
            self.speak("Focus reader is already running.")
            return

        self.speak("Starting focus reader.")

        def focus_loop():
            pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"
            engine = pyttsx3.init()
            def speak(text):
                print(f"🔊 Speaking: {text}")
                engine.say(text)
                engine.runAndWait()

            def find_first_named_child(element_info, depth=0, max_depth=3):
                if depth > max_depth:
                    return None
                try:
                    for child in element_info.children():
                        if child.name:
                            return child.name.strip()
                        deeper = find_first_named_child(child, depth + 1, max_depth)
                        if deeper:
                            return deeper
                except Exception:
                    return None
                return None

            def get_element_name(x, y):
                try:
                    pt = POINT(x, y)
                    iuia = IUIA()
                    element = iuia.iuia.ElementFromPoint(pt)
                    elem_info = UIAElementInfo(element)
                    name = elem_info.name or ""
                    if not name:
                        name = find_first_named_child(elem_info)
                    return name.strip() if name else ""
                except Exception:
                    return ""

            def get_window_title(x, y):
                try:
                    hwnd = win32gui.WindowFromPoint((x, y))
                    return win32gui.GetWindowText(hwnd).strip()
                except Exception:
                    return ""

            def ocr_region(x, y):
                try:
                    region = (x - 80, y - 40, 160, 80)
                    image = pyautogui.screenshot(region=region)
                    text = pytesseract.image_to_string(image).strip()
                    return text
                except Exception:
                    return ""

            last_spoken = ""
            while True:
                x, y = win32api.GetCursorPos()
                name = get_element_name(x, y)
                if not name:
                    name = get_window_title(x, y)
                if not name:
                    name = ocr_region(x, y)

                if name and name != last_spoken:
                    speak(name)
                    last_spoken = name
                time.sleep(1)

        # Launch in background thread
        self.focus_thread = threading.Thread(target=focus_loop, daemon=True)
        self.focus_thread.start()
    def read_clipboard_image(self):
        subprocess.run(["python", "i4.py"])

    # Enable Phoenix integration
gc_mode = False
nvda_instance = None

def start():
    global gc_mode, nvda_instance
    gc_mode = True
    nvda_instance = NVDA()
    nvda_instance.run()

if __name__ == "__main__":
    # Check for required dependencies
    try:
        nvda = NVDA()
        nvda.run()
    except ImportError as e:
        print(f"Error: Missing required package - {str(e)}")
        print("Please install all required packages:")
        print("pip install pyttsx3 keyboard pillow pytesseract pyautogui pywinauto speechrecognition")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing NVDA: {str(e)}")
        sys.exit(1)