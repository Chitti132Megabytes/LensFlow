import cv2
import mediapipe as mp
from gesture_recognizer import GestureRecognizer
from gesture_stabilizer import GestureStabilizer

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Utility for drawing landmarks
mp_draw = mp.solutions.drawing_utils
recognizer = GestureRecognizer()
stabilizer = GestureStabilizer()


def start_hand_detection():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Could not open webcam.")
        return

    print("✅ Hand Detection Started")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            break

        # Flip image for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = hands.process(rgb_frame)

        # Draw landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                
                gesture = recognizer.detect(hand_landmarks)

                confirmed_gesture = stabilizer.update(gesture)

                display_text = "Detecting..."

                if confirmed_gesture:
                    display_text = f"Confirmed: {confirmed_gesture}"

                cv2.putText(
                frame,
                display_text,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
                )

        cv2.imshow("LensFlow - Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_hand_detection()