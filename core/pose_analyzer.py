import math
import numpy as np

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LEFT_WRIST = 15
RIGHT_WRIST = 16

LEFT_HIP = 23
RIGHT_HIP = 24

LEFT_KNEE = 25
RIGHT_KNEE = 26

LEFT_ANKLE = 27
RIGHT_ANKLE = 28


class PoseAnalyzer:

    def __init__(self, visibility_threshold=0.5, smoothing_alpha=0.25):
        self.visibility_threshold = visibility_threshold
        self.smoothing_alpha = smoothing_alpha

        self.previous_angles = {
            "left_elbow": None,
            "right_elbow": None,
            "left_knee": None,
            "right_knee": None
        }

    def calculate_angle(self, a, b, c):

        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)
        c = np.array(c, dtype=np.float32)

        ba = a - b
        bc = c - b

        magnitude_ba = np.linalg.norm(ba)
        magnitude_bc = np.linalg.norm(bc)

        if magnitude_ba == 0 or magnitude_bc == 0:
            return None

        dot_product = np.dot(ba, bc)

        cosine_angle = dot_product / (
            magnitude_ba * magnitude_bc
        )

        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

        angle = np.degrees(
            np.arccos(cosine_angle)
        )

        return float(angle)

    def get_point(self, landmark):
        return (landmark.x, landmark.y)

    def is_visible(self, landmark):
        visibility = getattr(landmark, "visibility", 1.0)

        return visibility >= self.visibility_threshold

    def calculate_smoothed_angle(self, name, angle):

        if angle is None:
            return self.previous_angles[name]

        previous = self.previous_angles[name]

        if previous is None:
            smoothed = angle
        else:
            alpha = self.smoothing_alpha

            smoothed = (
                alpha * angle
                + (1 - alpha) * previous
            )

        self.previous_angles[name] = smoothed

        return float(smoothed)

    def get_joint_angles(self, pose_landmarks):

        joints = {
            "left_elbow": (
                LEFT_SHOULDER,
                LEFT_ELBOW,
                LEFT_WRIST
            ),

            "right_elbow": (
                RIGHT_SHOULDER,
                RIGHT_ELBOW,
                RIGHT_WRIST
            ),

            "left_knee": (
                LEFT_HIP,
                LEFT_KNEE,
                LEFT_ANKLE
            ),

            "right_knee": (
                RIGHT_HIP,
                RIGHT_KNEE,
                RIGHT_ANKLE
            )
        }

        angles = {}

        for name, (a_idx, b_idx, c_idx) in joints.items():

            a = pose_landmarks[a_idx]
            b = pose_landmarks[b_idx]
            c = pose_landmarks[c_idx]

            if not (
                self.is_visible(a)
                and self.is_visible(b)
                and self.is_visible(c)
            ):
                angles[name] = self.previous_angles[name]
                continue

            raw_angle = self.calculate_angle(
                self.get_point(a),
                self.get_point(b),
                self.get_point(c)
            )

            angles[name] = self.calculate_smoothed_angle(
                name,
                raw_angle
            )

            print(
                "LEFT:",
                "shoulder =", self.get_point(pose_landmarks[LEFT_SHOULDER]),
                "elbow =", self.get_point(pose_landmarks[LEFT_ELBOW]),
                "wrist =", self.get_point(pose_landmarks[LEFT_WRIST])
            )

        return angles


if __name__ == "__main__":

    analyzer = PoseAnalyzer()

    fake_landmarks = [
        type(
            "Landmark",
            (),
            {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "visibility": 1.0
            }
        )()
        for _ in range(33)
    ]

    fake_landmarks[LEFT_SHOULDER].x = 0
    fake_landmarks[LEFT_SHOULDER].y = 0

    fake_landmarks[LEFT_ELBOW].x = 1
    fake_landmarks[LEFT_ELBOW].y = 0

    fake_landmarks[LEFT_WRIST].x = 1
    fake_landmarks[LEFT_WRIST].y = 1

    # Right elbow test
    fake_landmarks[RIGHT_SHOULDER].x = 0
    fake_landmarks[RIGHT_SHOULDER].y = 0

    fake_landmarks[RIGHT_ELBOW].x = 1
    fake_landmarks[RIGHT_ELBOW].y = 0

    fake_landmarks[RIGHT_WRIST].x = 1
    fake_landmarks[RIGHT_WRIST].y = 1

    # Left knee test
    fake_landmarks[LEFT_HIP].x = 0
    fake_landmarks[LEFT_HIP].y = 0

    fake_landmarks[LEFT_KNEE].x = 1
    fake_landmarks[LEFT_KNEE].y = 0

    fake_landmarks[LEFT_ANKLE].x = 1
    fake_landmarks[LEFT_ANKLE].y = 1


    # Right knee test
    fake_landmarks[RIGHT_HIP].x = 0
    fake_landmarks[RIGHT_HIP].y = 0

    fake_landmarks[RIGHT_KNEE].x = 1
    fake_landmarks[RIGHT_KNEE].y = 0

    fake_landmarks[RIGHT_ANKLE].x = 1
    fake_landmarks[RIGHT_ANKLE].y = 1

    angles = analyzer.get_joint_angles(fake_landmarks)

    print(angles)