import cv2
import mediapipe as mp
import numpy as np

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.prev_angle = None
        self.smoothed_angle = 0
        self.alpha = 0.1  # smoothing factor

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        landmarks = None
        angle = None
        confidence = 0
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks
            confidence = results.multi_handedness[0].classification[0].score
            # Calculate angle using wrist and middle finger MCP
            wrist = hand_landmarks.landmark[0]
            middle_mcp = hand_landmarks.landmark[9]
            vec = np.array([middle_mcp.x - wrist.x, middle_mcp.y - wrist.y])
            angle = np.arctan2(vec[1], vec[0]) * 180 / np.pi
            # Smooth angle
            if self.prev_angle is None:
                self.smoothed_angle = angle
            else:
                diff = angle - self.prev_angle
                if abs(diff) > 180:
                    if diff > 0:
                        diff -= 360
                    else:
                        diff += 360
                self.smoothed_angle += self.alpha * diff
            self.prev_angle = angle
        return landmarks, self.smoothed_angle, confidence

    def draw_landmarks(self, frame, landmarks):
        if landmarks:
            self.mp_draw.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)