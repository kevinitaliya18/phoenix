import cv2
import mediapipe as mp
import pyautogui
import math
import time
import sys
import os

# Check for display environment (for pyautogui)
if sys.platform.startswith('linux') and 'DISPLAY' not in os.environ:
    print("Error: No display found. Please run this script in a graphical environment.")
    sys.exit(1)

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)
prev_x, prev_y = 0, 0
smoothening = 5
drag_mode = False
click_cooldown = 0
scroll_cooldown = 0

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    # Thumb
    fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0]-1].x else 0)
    # 4 fingers
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i]-2].y else 0)
    return fingers

while True:
    success, frame = cap.read()
    if not success:
        continue
        
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # Cooldown timers
    if click_cooldown > 0:
        click_cooldown -= 1
    if scroll_cooldown > 0:
        scroll_cooldown -= 1

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        lm = hand_landmarks.landmark

        # Tip coordinates
        x_index, y_index = int(lm[8].x * w), int(lm[8].y * h)
        x_middle, y_middle = int(lm[12].x * w), int(lm[12].y * h)
        x_ring, y_ring = int(lm[16].x * w), int(lm[16].y * h)
        x_thumb, y_thumb = int(lm[4].x * w), int(lm[4].y * h)
        x_pinky, y_pinky = int(lm[20].x * w), int(lm[20].y * h)
        palm_base = (int(lm[0].x * w), int(lm[0].y * h))

        # Move Cursor
        screen_x = int(lm[8].x * screen_w)
        screen_y = int(lm[8].y * screen_h)
        cur_x = prev_x + (screen_x - prev_x) / smoothening
        cur_y = prev_y + (screen_y - prev_y) / smoothening
        pyautogui.moveTo(cur_x, cur_y)
        prev_x, prev_y = cur_x, cur_y

        fingers = fingers_up(hand_landmarks)

        # Left Click: All fingers up except index finger down
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            if click_cooldown == 0:
                pyautogui.click()
                click_cooldown = 20  # ~0.3 seconds cooldown
                cv2.putText(frame, "Left Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Right Click: All fingers up except middle finger down
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
            if click_cooldown == 0:
                pyautogui.rightClick()
                click_cooldown = 20
                cv2.putText(frame, "Right Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Double Click: Index and middle fingers down, others up
        elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
            if click_cooldown == 0:
                pyautogui.doubleClick()
                click_cooldown = 30  # Longer cooldown for double click
                cv2.putText(frame, "Double Click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Scroll Up: All fingers closed (fist) - increased speed (80)
        elif sum(fingers) == 0:
            if scroll_cooldown == 0:
                pyautogui.scroll(80)  # Increased scroll speed
                scroll_cooldown = 8  # Reduced cooldown for faster scrolling
                cv2.putText(frame, "Scroll Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Scroll Down: All fingers open (palm open)
        elif sum(fingers) == 5:
            if scroll_cooldown == 0:
                pyautogui.scroll(-40)
                scroll_cooldown = 10
                cv2.putText(frame, "Scroll Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Drag & Drop: Pinch (Index + Thumb)
        if distance((x_index, y_index), (x_thumb, y_thumb)) < 40:
            if not drag_mode:
                pyautogui.mouseDown()
                drag_mode = True
                cv2.putText(frame, "Drag Mode", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if drag_mode:
                pyautogui.mouseUp()
                drag_mode = False

    # Display mode information
    if drag_mode:
        cv2.putText(frame, "Drag Mode Active", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Enhanced Virtual Mouse", frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
if drag_mode:
    pyautogui.mouseUp()
cap.release()
cv2.destroyAllWindows()