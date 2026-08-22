import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_PATH = "models/pose_landmarker_lite.task"

class PoseDetector:
    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path = MODEL_PATH
        )


        options = vision.PoseLandmarkerOptions(
            base_options = base_options,
            running_mode = vision.RunningMode.IMAGE,
            num_poses = 1,
            min_pose_detection_confidence = 0.5,
            min_pose_presence_confidence = 0.5,
            min_tracking_confidence = 0.5,
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(options)

    def detect(self , frame):
        rgb_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = rgb_frame
        )

        result = self.landmarker.detect(mp_image)

        return result
    