import cv2

from core.pose_detector import PoseDetector

def main():
    detector = PoseDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam. ")
        return 

    print("Camera started. Press 'q' to quit. ")

    while True:
        success , frame = camera.read()

        if not success:
            print("Error: Could not read frame.")
            break

        result = detector.detect(frame)

        if result.pose_landmarks:
            for pose_landmarks in result.pose_landmarks:
                for landmark in pose_landmarks:
                    height, width, _ = frame.shape

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x,y),
                        4,
                        (0,255,0),
                        -1
                    )
            cv2.imshow("KhelAI - Pose Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()