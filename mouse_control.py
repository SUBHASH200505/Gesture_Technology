import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Function to move the mouse
def move_mouse(x, y, frame_width, frame_height):
    screen_x = int(x * pyautogui.size().width / frame_width)
    screen_y = int(y * pyautogui.size().height / frame_height)
    pyautogui.moveTo(screen_x, screen_y)

# Function to calculate the Euclidean distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Get the index finger tip landmark
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_finger_x = index_finger_tip.x * frame.shape[1]
        index_finger_y = index_finger_tip.y * frame.shape[0]

        # Move the mouse based on index finger tip position
        move_mouse(index_finger_x, index_finger_y, frame.shape[1], frame.shape[0])

        # Get the thumb tip landmark
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_x = thumb_tip.x * frame.shape[1]
        thumb_y = thumb_tip.y * frame.shape[0]

        # Get the middle finger tip landmark (for right-click)
        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_finger_x = middle_finger_tip.x * frame.shape[1]
        middle_finger_y = middle_finger_tip.y * frame.shape[0]

        # Calculate the distance between thumb and index finger
        thumb_index_distance = calculate_distance(thumb_x, thumb_y, index_finger_x, index_finger_y)

        # Calculate the distance between index finger and middle finger (optional for right click)
        index_middle_distance = calculate_distance(index_finger_x, index_finger_y, middle_finger_x, middle_finger_y)

        # Set thresholds for clicking
        click_threshold = 40  # Adjust this threshold as needed

        # Perform left click if thumb and index finger are close
        if thumb_index_distance < click_threshold:
            pyautogui.click(button='left')

        # Perform right click if index and middle finger are close (you can change this gesture)
        if index_middle_distance < click_threshold:
            pyautogui.click(button='right')

        # Draw the hand landmarks
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display the webcam feed
    cv2.imshow("Mouse Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
