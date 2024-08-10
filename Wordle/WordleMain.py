from WordleEngine import Main
import keyboard
from os import system
from time import sleep

while True:
    sleep(4)
    system('cls')
    print(
        """
    
    Press y/Y to start.
    
    """
    )
    if keyboard.read_key().lower() != "y":
        exit(code=1)
    system('cls')
    keyboard.press("backspace")
    Main()
