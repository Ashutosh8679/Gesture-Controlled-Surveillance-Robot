import cv2
import mediapipe as mp
import speech_recognition as sr
import threading
import socket

# Serial connection removed — using wireless connectivity instead.
# Placeholder: implement wireless send/initialization where needed.


ESP_IP = "192.168.4.1"   # AP mode default IP
ESP_PORT = 3333

# ---------------- HAND GESTURE SETUP ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def get_finger_list(landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for i in range(1, 5):
        if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def gesture_to_action(f):
    if f == [0,0,0,0,0]:
        return "STOP"
    if f == [1,1,1,1,1]:
        return "FORWARD"
    if f == [0,1,0,0,0]:
        return "LEFT"
    if f == [0,1,1,0,0]:
        return "RIGHT"
    if f == [1,0,0,0,0]:
        return "BACK"
    return "NONE"

# ---------------- ESP32 COMMUNICATION ----------------
def send_message(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(msg.encode(), (ESP_IP, ESP_PORT))
    s.close()


    

# ---------------- VOICE CONTROL THREAD ----------------
def voice_control():
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for voice command...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio).lower()
            print("You said:", text)

            if "forward" in text:
                send_message("F")
            elif "back" in text or "reverse" in text:
                send_message("B")
            elif "left" in text:
                send_message("L")
            elif "right" in text:
                send_message("R")
            elif "stop" in text:
                send_message("S")

        except:
            pass

# Start voice recognition in background
threading.Thread(target=voice_control, daemon=True).start()

# ---------------- HAND GESTURE LOOP ----------------
cap = cv2.VideoCapture(0)
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            finger_list = get_finger_list(hand.landmark)
            action = gesture_to_action(finger_list)

            cv2.putText(frame, action, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)

            print("Gesture:", finger_list, "| Action:", action)

            if action == "FORWARD": send_message("F")
            elif action == "BACK": send_message("B")
            elif action == "LEFT": send_message("L")
            elif action == "RIGHT": send_message("R")
            elif action == "STOP": send_message("S")

        cv2.imshow("Car Control - Gesture + Voice", frame)

        if cv2.waitKey(1) == 27:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()