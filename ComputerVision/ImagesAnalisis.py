import cv2
import numpy as np
import os

COLOR_RANGES = {
    "yellow": [((20, 100, 100), (35, 255, 255))],
    "green":  [((35, 100, 100), (85, 255, 255))],
    "blue":   [((100, 100, 100), (130, 255, 255))],
    "red":    [((0, 100, 100), (10, 255, 255)), ((170, 100, 100), (180, 255, 255))]
}

def main():
    image_paths = fileList()

    for path in image_paths:
        image = cv2.imread(path)
        if image is None:
            continue
            
        shapes = detectShapes(image)
        drawAndPrint(shapes, image, os.path.basename(path))

def fileList():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "test_images")

    if not os.path.exists(path):
        print(f"Errore: impossibile trovare {path}")
        exit()
        
    image_files = []
    for file in os.listdir(path):
        if file.startswith("test") and file.endswith(".png"):
            image_files.append(os.path.join(path, file))

    image_files.sort()
    return image_files

def detectShapes(image):
    min_area = 100 
    detections = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for color_name, ranges in COLOR_RANGES.items():
        for border in findBorders(hsv, ranges):
            shape = selectShape(border, min_area, color_name)
            if shape is not None:
                detections.append(shape)

    return detections

def findBorders(hsv, ranges):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in ranges:
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        mask_range = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.bitwise_or(mask, mask_range)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def selectShape(cnt, min_area, color_name):
    area = cv2.contourArea(cnt)
    if area < min_area:
        return None
    
    x, y, w, h = cv2.boundingRect(cnt)
    cx = x + w // 2
    cy = y + h // 2

    detection = {
        "color": color_name,
        "bbox": (x, y, w, h),
        "center": (cx, cy),
        "area": float(area)
    }

    return detection

def drawAndPrint(shapeList, image, window_title="Detection Result"):
    print(f"\n--- Rilevamenti per {window_title} ---")
    
    # 1. Disegna TUTTE le forme trovate sull'immagine
    for detect in shapeList:
        x, y, w, h = detect["bbox"]
        cx, cy = detect["center"]
        color_name = detect["color"]
        area = detect["area"]

        # Disegna il rettangolo
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Disegna il centro
        cv2.circle(image, (cx, cy), 3, (0, 0, 255), -1)
        # Scrivi il testo sopra la figura
        cv2.putText(image, f"{color_name} ({int(area)}px)", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        print(detect)

    # 2. Mostra l'immagine completa una volta sola per file
    cv2.imshow(window_title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()