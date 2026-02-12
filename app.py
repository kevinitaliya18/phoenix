import eel
import os
from queue import Queue

class ChatBot:
    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        ChatBot.close()
        os._exit(0)  # Force exit the application

    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print(msg)

    @staticmethod
    def close():
        ChatBot.started = False

    @staticmethod
    def addUserMsg(msg):
        eel.addUserMsg(msg)

    @staticmethod
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    @staticmethod
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r"\web", allowed_extensions=[".js", ".html"])
        
        try:
            # Try multiple ports if default is busy
            ports = [27005, 27006, 27007, 8080]
            for port in ports:
                try:
                    eel.start(
                        "index.html",
                        mode="chrome",
                        host="localhost",
                        port=port,
                        block=False,
                        size=(350, 480),
                        position=(10, 100),
                        disable_cache=True,
                        close_callback=ChatBot.close_callback,
                    )
                    ChatBot.started = True
                    print(f"Server started on port {port}")
                    break
                except Exception as e:
                    print(f"Port {port} in use, trying next...")
                    continue
            
            # Main loop
            while ChatBot.started:
                try:
                    eel.sleep(1.0)  # Reduced sleep time for more responsive shutdown
                except (KeyboardInterrupt, SystemExit):
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

        except Exception as e:
            print(f"Failed to start server: {e}")
        finally:
            ChatBot.close()