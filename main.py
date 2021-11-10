import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller


k = Controller() 


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def switch(pos):
    # 0 = right, 1 = left
    if pos == 0:
        k.press(Key.cmd_l)
        k.press(Key.right)
        k.release(Key.cmd_l)
        k.release(Key.right)
    if pos == 1:
        k.press(Key.cmd_l)
        k.press(Key.left)
        k.release(Key.cmd_l)
        k.release(Key.left)


with mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3, max_num_hands=1) as hands:

    prev_position = 0.0
    counter = 0

    while cap.isOpened():
        ret, frame = cap.read()

        # Detections 
        if counter > 5:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                print(results.multi_hand_landmarks[0].landmark[0].x)

                curr_pos = results.multi_hand_landmarks[0].landmark[0].x
                
                if prev_position < 0.5 and curr_pos > 0.5:
                    print("\n\n\n\n\n\        SWITCH\n\n\n\n\n\n")
                    switch(0)
                    curr_pos = 0.5
                    counter = 0
                                
                if prev_position > 0.5 and curr_pos < 0.5:
                    print('\n\n\n\n\n\     BACK-SWITCH\n\n\n\n\n\n')
                    switch(1)
                    curr_pos = 0.5
                    counter = 0
                                
             
                prev_position = curr_pos

                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

            cv2.imshow('Image', image)

        counter += 1

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break 

cap.release()
cv2.destroyAllWindows()

