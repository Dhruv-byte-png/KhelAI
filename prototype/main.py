import cv2

from core.pose_detector import PoseDetector
from core.pose_analyzer import PoseAnalyzer
from core.exercises.bicep_curl import BicepCurlAnanlyzer


POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),

    (9, 10),

    (11, 12),

    (11, 13), (13, 15),
    (15, 17), (15, 19), (15, 21),
    (17, 19),

    (12, 14), (14, 16),
    (16, 18), (16, 20), (16, 22),
    (18, 20),

    (11, 23),
    (12, 24),
    (23, 24),

    (23, 25), (25, 27),
    (27, 29), (27, 31),
    (29, 31),

    (24, 26), (26, 28),
    (28, 30), (30, 32),
]


def main():
    detector = PoseDetector()
    analyzer = PoseAnalyzer()
    curl_analyzer = BicepCurlAnanlyzer()

    camera = cv2.VideoCapture(0, cv2.CAP_MSMF)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Camera started. Press 'q' to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame.")
            break

        result = detector.detect(frame)

        # Default states when no pose is detected
        left_curl_state = "UNKNOWN"
        right_curl_state = "UNKNOWN"

        if result.pose_landmarks:
            angles = analyzer.get_joint_angles(
                result.pose_landmarks[0]
            )

            print("Angles:", angles)

            # Smooth the raw elbow angles
            left_angle = curl_analyzer.smooth_angle(
                angles["left_elbow"]
            )

            right_angle = curl_analyzer.smooth_angle(
                angles["right_elbow"]
            )

            # Determine curl state from smoothed angles
            left_curl_state = curl_analyzer.get_state(
                left_angle
            )

            right_curl_state = curl_analyzer.get_state(
                right_angle
            )

            print(
                f"Left Curl: {left_curl_state} | "
                f"Right Curl: {right_curl_state}"
            )

            # Display raw joint angles
            angle_names = [
                ("Left Elbow", angles["left_elbow"]),
                ("Right Elbow", angles["right_elbow"]),
                ("Left Knee", angles["left_knee"]),
                ("Right Knee", angles["right_knee"])
            ]

            y_position = 50

            for name, angle in angle_names:
                if angle is not None:
                    cv2.putText(
                        frame,
                        f"{name}: {angle:.1f}",
                        (30, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    y_position += 35

            # Display curl states
            cv2.putText(
                frame,
                f"Left Curl: {left_curl_state}",
                (30, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Right Curl: {right_curl_state}",
                (30, 235),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        # Draw pose landmarks and connections
        if result.pose_landmarks:
            height, width, _ = frame.shape

            for pose_landmarks in result.pose_landmarks:

                # Draw landmarks
                for landmark in pose_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (0, 255, 0),
                        -1
                    )

                # Draw connections
                for start, end in POSE_CONNECTIONS:

                    start_landmark = pose_landmarks[start]
                    end_landmark = pose_landmarks[end]

                    start_x = int(start_landmark.x * width)
                    start_y = int(start_landmark.y * height)

                    end_x = int(end_landmark.x * width)
                    end_y = int(end_landmark.y * height)

                    cv2.line(
                        frame,
                        (start_x, start_y),
                        (end_x, end_y),
                        (0, 255, 0),
                        2
                    )

        # Show camera
        cv2.imshow(
            "KhelAI - Camera Test",
            frame
        )

        # Quit with Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()