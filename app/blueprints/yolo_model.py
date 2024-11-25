from ultralytics import YOLO

class YOLOModel:
    model = YOLO("models/l_version_1_300.pt").to("cpu")

    @staticmethod
    def detect(frame):
        return YOLOModel.model(frame, stream=True)
