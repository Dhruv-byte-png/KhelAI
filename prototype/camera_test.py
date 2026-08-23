import cv2

for index in [0,1]:
    camera = cv2.VideoCapture(index, cv2.CAP_MSMF)

    if not camera.isOpened():
        print(f"Could not open Camera {index}")
        continue
    print(f" Testing Camera {index}. Press 'q' to close.")

    while True:
        success, frame  = camera.read()

        if not success:
            print(f"could not read camera {index}")
            break

        cv2.imshow(f"Camera {index}", frame)

        key = cv2.waitKey(1) & 0xFF 

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()