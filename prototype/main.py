import cv2

from core.pose_detector import PoseDetector
from core.pose_analyzer import PoseAnalyzer
from mediapipe.tasks.python import vision

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
    (28, 30), (28, 32),
    (30, 32),
]

def main():
    detector = PoseDetector()
    analyzer = PoseAnalyzer()
    

    camera = cv2.VideoCapture(0, cv2.CAP_MSMF)

    if not camera.isOpened():
        print("Error: Could not open webcam. ")
        return 

    print("Camera started. Press 'q' to quit. ")

    while True:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read frame.")
            break

        result = detector.detect(frame)

        if result.pose_landmarks:
            angles = analyzer.get_joint_angles(result.pose_landmarks[0])

            print("Angles:", angles)

            if angles["left_elbow"] is not None:
                cv2.putText(
                    frame,
                    f"Left Elbow: {angles['left_elbow']:.1f}",
                    (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )
        cv2.imshow("KhelAI - Camera Test", frame)

        if result.pose_landmarks:
            height, width, _ = frame.shape

            for pose_landmarks in result.pose_landmarks:
                #draw landmarks

                for landmark in pose_landmarks:
                    
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x,y),
                        4,
                        (0,255,0),
                        -1
                    )
                #Draw connections
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

        cv2.imshow("KhelAI - Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()