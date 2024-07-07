import cv2

# List to store quadrant coordinates
quadrant_coords = []

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global x1, y1, drawing, quadrant_coords

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1, y1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (x1, y1), (x, y), (0, 255, 0), 2)
            cv2.imshow("Frame", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = x, y
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        quadrant_coords.append((x1, y1, x2, y2))
        print(f"Quadrant {len(quadrant_coords)}: {(x1, y1, x2, y2)}")

# Load video and get first frame
cap = cv2.VideoCapture("AI_Assignment_video.mp4")
ret, img = cap.read()
if not ret:
    print("Failed to read video")
    exit(1)

drawing = False
x1, y1 = -1, -1

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_rectangle)

while True:
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("Final quadrant coordinates:", quadrant_coords)
