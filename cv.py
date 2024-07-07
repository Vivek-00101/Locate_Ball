import cv2
import numpy as np
import time

# Define the HSV color ranges for the balls
color_ranges = {
    "Green": ((35, 40, 40), (85, 255, 255)),
    "Yellow": ((20, 100, 100), (30, 255, 255)),
    "White": ((0, 0, 100), (180, 50, 255)), 
    "Orange": ((5, 100, 100), (25, 255, 255))
}

def detect_circles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=2.6, minDist=30, param1=130, param2=100, minRadius=35, maxRadius=70)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
    return circles

def identify_color(hsv, x, y, r):
    mask = np.zeros(hsv.shape[:2], dtype="uint8")
    cv2.circle(mask, (x, y), r, 255, -1)
    mean_val = cv2.mean(hsv, mask=mask)[:3]
    mean_val = np.array(mean_val, dtype=np.uint8)
    
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        if np.all(lower <= mean_val) and np.all(mean_val <= upper):
            return color
    return None

def get_quadrant(x, y, quadrant_rects):
    for i, (qx1, qy1, qx2, qy2) in enumerate(quadrant_rects, 1):
        if qx1 < x < qx2 and qy1 < y < qy2:
            return i
    return None

def track_balls(video_path, quadrant_coords):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    events = {}
    prev_positions = {}

    start_time = time.time()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = time.time() - start_time
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        circles = detect_circles(frame)

        if circles is not None:
            for (x, y, r) in circles:
                color = identify_color(hsv, x, y, r)
                if color:
                    cv2.circle(frame, (x, y), r, (0, 255, 255), 2)
                    cv2.putText(frame, color, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    current_quad = get_quadrant(x, y, quadrant_coords)

                    if current_quad:
                        if color not in prev_positions:
                            prev_positions[color] = None
                        
                        if prev_positions[color] != current_quad:
                            if prev_positions[color] is not None:
                                events[(color, prev_positions[color], "Exit")] = timestamp
                            
                            events[(color, current_quad, "Entry")] = timestamp
                            prev_positions[color] = current_quad

        # Draw quadrant rectangles
        for i, (qx1, qy1, qx2, qy2) in enumerate(quadrant_coords, 1):
            cv2.rectangle(frame, (qx1, qy1), (qx2, qy2), (0, 255, 0), 2)
            cv2.putText(frame, f'Quadrant {i}', (qx1 + 10, qy1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    with open("events.txt", "w") as f:
        for (color, quadrant, event), timestamp in events.items():
            f.write(f"{timestamp:.2f}, {quadrant}, {color}, {event}\n")

quadrant_coords = [
    (1256, 545, 1740, 993),  # Quadrant 1 
    (794, 542, 1214, 1018),  # Quadrant 2
    (802, 28, 1215, 504),    # Quadrant 3
    (1266, 26, 1744, 506)    # Quadrant 4
]


track_balls("AI Assignment video.mp4", quadrant_coords)
