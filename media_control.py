import cv2
import mediapipe as mp
import pyautogui
import time
import warnings

# Suppress specific deprecation warning
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated.")

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

# Threshold to distinguish gestures
gesture_threshold = 0.2
start_init = False
prev_gesture = -1

def count_fingers(hand_landmarks):
    cnt = 0
    thresh = (hand_landmarks.landmark[0].y - hand_landmarks.landmark[9].y) / 2

    if (hand_landmarks.landmark[5].y - hand_landmarks.landmark[8].y) > thresh:
        cnt += 1
    if (hand_landmarks.landmark[9].y - hand_landmarks.landmark[12].y) > thresh:
        cnt += 1
    if (hand_landmarks.landmark[13].y - hand_landmarks.landmark[16].y) > thresh:
        cnt += 1
    if (hand_landmarks.landmark[17].y - hand_landmarks.landmark[20].y) > thresh:
        cnt += 1

    if (hand_landmarks.landmark[5].x - hand_landmarks.landmark[4].x) > 0.1:
        cnt += 1

    return cnt

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_count = count_fingers(hand_landmarks)

            if finger_count != prev_gesture:
                if not start_init:
                    start_init = True
                    start_time = time.time()
                elif time.time() - start_time > gesture_threshold:
                    # Map finger counts to specific media controls
                    if finger_count == 1:
                        pyautogui.press("right")
                    elif finger_count == 2:
                        pyautogui.press("left")
                    elif finger_count == 3:
                        pyautogui.press("up")
                    elif finger_count == 4:
                        pyautogui.press("down")
                    elif finger_count == 5:
                        pyautogui.press("space")
                    
                    prev_gesture = finger_count
                    start_init = False

            mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Media Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
