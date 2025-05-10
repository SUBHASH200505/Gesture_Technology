import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

# Define the screen resolution (adjust according to your screen size)
screen_width, screen_height = pyautogui.size()

# Define slide change thresholds
right_threshold = screen_width // 2
left_threshold = screen_width // 4

# Define initial hand position and rotation angle
prev_hand_pos = None
prev_rotation_angle = 0

# Define initial gesture as None
gesture = None

# Define keyboard shortcuts for controlling the presentation
presentation_keys = {
    'next_slide': 'right',
    'prev_slide': 'left',
    'start_presentation': 'space',
    'end_presentation': 'escape'
}

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Flip the frame horizontally for a more natural selfie-view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe Hands
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    # Check if any hands are detected
    if results.multi_hand_landmarks is not None:
        # Get the hand landmarks
        hand_landmarks = results.multi_hand_landmarks[0]

        # Calculate the center of the hand
        hand_center_x = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]) / 2
        hand_center_y = (hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0]) / 2

        # Calculate rotation angle
        if prev_hand_pos is not None:
            # Get wrist and middle finger landmarks
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Calculate vector components
            dx = middle_finger.x * frame.shape[1] - wrist.x * frame.shape[1]
            dy = middle_finger.y * frame.shape[0] - wrist.y * frame.shape[0]

            # Calculate rotation angle
            rotation_angle = math.degrees(math.atan2(dy, dx))

            # Normalize rotation angle to range [0, 360]
            rotation_angle = (rotation_angle + 360) % 360

            # Determine slide rotation based on rotation angle change
            rotation_threshold = 10  # Adjust this threshold as needed
            if rotation_angle - prev_rotation_angle > rotation_threshold:
                gesture = 'next_slide'
                pyautogui.press(presentation_keys['next_slide'])  # Rotate slide right
            elif rotation_angle - prev_rotation_angle < -rotation_threshold:
                gesture = 'prev_slide'
                pyautogui.press(presentation_keys['prev_slide'])  # Rotate slide left

            # Update previous rotation angle
            prev_rotation_angle = rotation_angle

        # Update previous hand position
        prev_hand_pos = (hand_center_x, hand_center_y)

        # Draw hand landmarks on the frame
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        # No hands detected, set gesture to None
        gesture = None

    # Print the recognized gesture
    print("Recognized Gesture:", gesture)

    # Display the frame
    cv2.imshow('Hand Gestures', frame)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
