import cvzone

classNames = ['spoof', 'real']
confidence_threshold = 0.6

def annotate_frame(frame, results):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0])
            if conf > confidence_threshold:
                color = (0, 255, 0) if classNames[cls] == 'real' else (0, 0, 255)
                cvzone.cornerRect(frame, (x1, y1, x2 - x1, y2 - y1), colorC=color)
                cvzone.putTextRect(
                    frame,
                    f"{classNames[cls].upper()} {int(conf * 100)}%",
                    (x1, y1 - 10),
                    scale=2,
                    thickness=4,
                    colorR=color
                )
    return frame