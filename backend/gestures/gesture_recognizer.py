import mediapipe as mp


class GestureRecognizer:

    def __init__(self):
        self.mp_hands = mp.solutions.hands

    def finger_up(self, tip, pip, landmarks):
        return landmarks[tip].y < landmarks[pip].y

    def thumb_up(self, landmarks):
        return landmarks[4].y < landmarks[3].y

    def is_fist(self, landmarks):

        index = self.finger_up(8, 6, landmarks)
        middle = self.finger_up(12, 10, landmarks)
        ring = self.finger_up(16, 14, landmarks)
        pinky = self.finger_up(20, 18, landmarks)

        thumb = self.thumb_up(landmarks)

        return (
            not thumb and
            not index and
            not middle and
            not ring and
            not pinky
        )

    def is_open_palm(self, landmarks):

        return (
            self.finger_up(8, 6, landmarks) and
            self.finger_up(12, 10, landmarks) and
            self.finger_up(16, 14, landmarks) and
            self.finger_up(20, 18, landmarks)
        )

    def is_peace(self, landmarks):

        return (
            self.finger_up(8, 6, landmarks) and
            self.finger_up(12, 10, landmarks) and
            not self.finger_up(16, 14, landmarks) and
            not self.finger_up(20, 18, landmarks)
        )

    def is_thumbs_up(self, landmarks):

        return (
            self.thumb_up(landmarks) and
            not self.finger_up(8, 6, landmarks) and
            not self.finger_up(12, 10, landmarks) and
            not self.finger_up(16, 14, landmarks) and
            not self.finger_up(20, 18, landmarks)
        )

    def detect(self, hand_landmarks):

        landmarks = hand_landmarks.landmark

        if self.is_thumbs_up(landmarks):
            return "👍 Thumbs Up"

        if self.is_fist(landmarks):
            return "✊ Fist"

        if self.is_open_palm(landmarks):
            return "✋ Open Palm"

        if self.is_peace(landmarks):
            return "✌️ Peace"

        return "Unknown"