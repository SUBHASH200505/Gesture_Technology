import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]  # Volume range

# Initialize variables
volbar = 400
volper = 0
last_volume = volume.GetMasterVolumeLevel()  # Track the last volume level
camera_index = 0  # Default camera index

# Start video capture
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

print("Camera successfully accessed. Starting volume control...")

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to read from the camera.")
            break

        img = cv2.flip(img, 1)  # Flip image horizontally
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList:
            # Get positions of index finger tip and thumb tip
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
            x2, y2 = lmList[8][1], lmList[8][2]  # Index finger tip

            cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Calculate distance between fingers
            length = hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [30, 300], [volMin, volMax])
            volbar = np.interp(length, [30, 300], [400, 150])
            volper = np.interp(length, [30, 300], [0, 100])

            # Ensure volume level is within bounds
            vol = np.clip(vol, volMin, volMax)

            # Update volume only if there's a significant change
            if abs(vol - last_volume) > 0.5:  # Adjust threshold as needed
                volume.SetMasterVolumeLevel(vol, None)
                last_volume = vol

            # Display volume bar
            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

        cv2.imshow('Volume Control', img)

        # Exit on pressing the spacebar
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released.")
