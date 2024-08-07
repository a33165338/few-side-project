import cv2
import numpy as np

class YOLOObjectDetector:
    def __init__(self, config_path, weights_path, classes_path):
        # 加載 YOLO 模型
        self.net = cv2.dnn.readNet(weights_path, config_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        # 加載類別名稱
        with open(classes_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # 定義顏色
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def detect_objects(self, frame):
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        return indexes, boxes, confidences, class_ids

    def draw_labels(self, frame, indexes, boxes, confidences, class_ids):
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color = self.colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print(f"Detected {label} with confidence {confidences[i]:.2f} at [{x}, {y}, {w}, {h}]")  # Debug message

class VideoProcessor:
    def __init__(self, video_path, yolo_detector):
        self.cap = cv2.VideoCapture(video_path)
        self.yolo_detector = yolo_detector

    def process(self):
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            return

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            print("Frame read successfully.")  # Debug message

            indexes, boxes, confidences, class_ids = self.yolo_detector.detect_objects(frame)
            self.yolo_detector.draw_labels(frame, indexes, boxes, confidences, class_ids)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# 使用 YOLO 模型和影片處理器
yolo_detector = YOLOObjectDetector("D:\\Case\\VCAI\\yolov3.cfg", "D:\\Case\\VCAI\\yolov3.weights", "D:\\Case\\VCAI\\coco.names")
video_processor = VideoProcessor("D:\\Case\\VCAI\\test_video.mp4", yolo_detector)
video_processor.process()
