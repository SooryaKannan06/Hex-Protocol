import cv2
from ultralytics import YOLO

# 🔴 Load your trained model
model = YOLO("best-yolov8s.pt")   # put your file path if needed

# 🎥 Start webcam
cap = cv2.VideoCapture(1)
# 🎨 Class colors (your idea)
colors = {
    0: (0, 255, 0),   # biodegradable → green
    1: (255, 0, 0),   # recyclable → blue
    2: (0, 0, 255)    # hazardous → red
}


# 🏷 Class names
names = ["biodegradable", "recyclable", "hazardous"]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 🔍 Predict
    results = model(frame, conf=0.5, iou=0.4)[0]

    # 📦 Draw boxes
    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        color = colors.get(cls, (255, 255, 255))
        label = f"{names[cls]} {conf:.2f}"

        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Put label
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 🖥 Show
    cv2.imshow("Waste Detection", frame)

    # ❌ Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()