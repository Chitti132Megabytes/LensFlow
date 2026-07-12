import mediapipe as mp


class GestureRecognizer:

    def __init__(self):
        self.mp_hands = mp.solutions.hands

    def finger_up(self, tip, pip, landmarks):
        return landmarks[tip].y < landmarks[pip].y

    def detect(self, hand_landmarks):

        landmarks = hand_landmarks.landmark

        index = self.finger_up(8, 6, landmarks)
        middle = self.finger_up(12, 10, landmarks)
        ring = self.finger_up(16, 14, landmarks)
        pinky = self.finger_up(20, 18, landmarks)

        if not index and not middle and not ring and not pinky:
            return "✊ Fist"

        if index and middle and ring and pinky:
            return "✋ Open Palm"

        # Peace Sign
        if index and middle and not ring and not pinky:
            return "✌️ Peace"
        
        return "Unknown"