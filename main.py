import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Funkcja do liczenia wyprostowanych palcow
def count_fingers(hand_landmarks, handedness, palm_side):
    fingers = [False] * 5
    tips = [4, 8, 12, 16, 20]  # Landmarki koncowek palcow

    # Kciuk
    thumb_tip = hand_landmarks.landmark[tips[0]]
    thumb_ip = hand_landmarks.landmark[3]
    thumb_mcp = hand_landmarks.landmark[2]

    if palm_side == "Inner":
        if handedness == "Right":
            fingers[0] = thumb_tip.x > thumb_ip.x and abs(thumb_tip.y - thumb_ip.y) < 0.2
        else:  # Lewa dlon
            fingers[0] = thumb_tip.x < thumb_ip.x and abs(thumb_tip.y - thumb_ip.y) < 0.2
    else:  # Zewnetrzna strona dloni
        if handedness == "Right":
            fingers[0] = thumb_tip.x < thumb_ip.x and abs(thumb_tip.y - thumb_ip.y) < 0.2
        else:  # Lewa dlon
            fingers[0] = thumb_tip.x > thumb_ip.x and abs(thumb_tip.y - thumb_ip.y) < 0.2

    # Pozostale palce (porownanie osi y z zagieciami)
    for i in range(1, 5):
        fingers[i] = hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y

    return fingers.count(True)

# Funkcja do rozpoznawania strony dloni
def detect_palm_side(hand_landmarks, handedness):
    # Uzywamy najnizszego punktu kciuka (mcp) w stosunku do nadgarstka (wrist)
    thumb_base = hand_landmarks.landmark[2]  # Podstawa kciuka (MCP)
    wrist = hand_landmarks.landmark[0]

    if handedness == "Right":
        # Jezeli podstawa kciuka jest po prawej stronie nadgarstka, to strona wewnetrzna
        return "Inner" if thumb_base.x > wrist.x else "Outer"
    else:  # Lewa dlon
        # Jezeli podstawa kciuka jest po lewej stronie nadgarstka, to strona wewnetrzna
        return "Inner" if thumb_base.x < wrist.x else "Outer"

def main():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.7, 
                        min_tracking_confidence=0.7,
                        max_num_hands=2) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Konwersja obrazu na RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            # Konwersja z powrotem na BGR do wyswietlania
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks and results.multi_handedness:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Pobieranie informacji o dloni (lewa/prawa z perspektywy uzytkownika)
                    handedness = results.multi_handedness[idx].classification[0].label
                    if handedness == "Left":
                        handedness = "Right"  # Zamiana dla poprawnej interpretacji kamery
                    else:
                        handedness = "Left"

                    # Rozpoznawanie strony dloni
                    palm_side = detect_palm_side(hand_landmarks, handedness)

                    # Liczenie wyprostowanych palcow
                    num_fingers = count_fingers(hand_landmarks, handedness, palm_side)

                    # Rysowanie landmarkow
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Wyswietlanie informacji
                    label = f"{handedness}, {palm_side}, {num_fingers} fingers"
                    h, w, _ = image.shape
                    cx = int(hand_landmarks.landmark[9].x * w)
                    cy = int(hand_landmarks.landmark[9].y * h)
                    cv2.putText(image, label, (cx - 100, cy - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Hand Tracking', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
