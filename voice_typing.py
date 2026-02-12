import speech_recognition as sr
import pyautogui
import threading
import time

class VoiceTypingController:
    def __init__(self):
        self.active = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.thread = None

    def start(self):
        """Start voice typing in a background thread"""
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self._voice_typing_loop, daemon=True)
            self.thread.start()
            return "Voice typing started. Speak to type."
        return "Voice typing is already active"

    def stop(self):
        """Stop voice typing"""
        if self.active:
            self.active = False
            if self.thread:
                self.thread.join(timeout=1)
            return "Voice typing stopped"
        return "Voice typing is not active"

    def _voice_typing_loop(self):
        """Main voice typing processing loop"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.active:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    pyautogui.write(text + " ", interval=0.05)  # Add space after each utterance
                    
                except sr.WaitTimeoutError:
                    continue  # No speech detected, continue listening
                except sr.UnknownValueError:
                    continue  # Speech was unintelligible
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    self.active = False
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    self.active = False

# Global instance for Phoenix integration
voice_typing = VoiceTypingController()

if __name__ == "__main__":
    # Test mode when run directly
    print("Voice Typing Module - Test Mode")
    print("Commands: start, stop, exit")
    
    while True:
        cmd = input("> ").lower()
        if cmd == "start":
            print(voice_typing.start())
        elif cmd == "stop":
            print(voice_typing.stop())
        elif cmd == "exit":
            voice_typing.stop()
            break
        else:
            print("Invalid command")


        