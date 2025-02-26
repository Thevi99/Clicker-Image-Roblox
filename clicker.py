import cv2
import numpy as np
import pyautogui
import time
import keyboard

template = cv2.imread('shake_button1.png', cv2.IMREAD_UNCHANGED)
template_Eng = cv2.imread('shake_button.png', cv2.IMREAD_UNCHANGED)

def detect_drag_and_click():
    state = False 

    while True:
        if keyboard.is_pressed('u'):
            state = True
            print("Started detection (Press 'q' to stop).")
            time.sleep(0.5)

        if keyboard.is_pressed('q'):
            state = False
            print("Stopped detection (Press 'u' to start).")
            time.sleep(0.5)

        if not state:
            time.sleep(0.1)
            continue

        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template_Eng_gray = cv2.cvtColor(template_Eng, cv2.COLOR_BGR2GRAY)

        result1 = cv2.matchTemplate(frame, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(result1)

        result2 = cv2.matchTemplate(frame, template_Eng_gray, cv2.TM_CCOEFF_NORMED)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(result2)

        if max_val1 > 0.8 or max_val2 > 0.8:
            if max_val1 > max_val2:
                x, y = max_loc1
                w, h = template.shape[1], template.shape[0]
            else:
                x, y = max_loc2
                w, h = template_Eng.shape[1], template_Eng.shape[0]

            end_x, end_y = x + w // 2, y + h // 2
            print(f"Detected at: ({end_x}, {end_y})")

            start_x, start_y = pyautogui.position()

            steps = 50
            for i in range(steps + 1):
                intermediate_x = start_x + (end_x - start_x) * i / steps
                intermediate_y = start_y + (end_y - start_y) * i / steps
                pyautogui.moveTo(intermediate_x, intermediate_y)
                time.sleep(0.01)

            print(f"Target Location (with offset): ({end_x}, {end_y})")

            pyautogui.moveTo(end_x, end_y)
            time.sleep(0.2) 
            pyautogui.click()
            print(f"Clicked at: ({end_x}, {end_y})")

        time.sleep(0.1)

try:
    detect_drag_and_click()
except Exception as e:
    print(f"An error occurred: {e}")
