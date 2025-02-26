import pyautogui
import time
import keyboard

def detect_drag_and_click():
    state = False 

    while True:
        if keyboard.is_pressed('u') and not state:
            state = True
            print("Started holding and clicking (Press 'q' to stop).")
            time.sleep(0.5) 
        
        if keyboard.is_pressed('q') and state:
            state = False
            print("Stopped holding and clicking (Press 'u' to start).")
            time.sleep(0.5) 
        
        if state:
            pyautogui.click()

try:
    detect_drag_and_click()
except Exception as e:
    print(f"An error occurred: {e}")
