import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5, maxHands=1) 
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

hand_detected = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    hand, img = detector.findHands(img)
    if hand and not hand_detected:
        fingers = detector.fingersUp(hand[0])
        totalFingers = fingers.count(1)
        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        hand_detected = True
        
        if totalFingers == 5:
            pyautogui.keyDown('right')
            pyautogui.keyUp('left')
        elif totalFingers == 0:
            pyautogui.keyDown('left')
            pyautogui.keyUp('right')
    else:
        if hand_detected:
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
            hand_detected = False
    
    cv2.imshow('Camera Feed', img)
    cv2.waitKey(1)

    if cv2.waitKey(1) == ord('q'): 
        break
        
cap.release()
cv2.destroyAllWindows()
