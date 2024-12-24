
import cv2
import numpy as np

# Load the video
video_path = '.mp4'  # Replace with actual video path if needed
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read the first frame
ret, first_frame = cap.read()
if not ret:
    print("Error: Could not read the first frame.")
    cap.release()
    exit()

# Function to draw a bounding box
def draw_bounding_box(event, x, y, flags, param):
    global box_points, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        box_points = [(x, y)]
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_copy = first_frame.copy()
        cv2.rectangle(img_copy, box_points[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("Frame", img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        box_points.append((x, y))
        drawing = False
        cv2.rectangle(first_frame, box_points[0], box_points[1], (0, 255, 0), 2)
        cv2.imshow("Frame", first_frame)

# Setup for drawing bounding box
box_points = []
drawing = False
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_bounding_box)

# Display the first frame and wait for user to draw a box
while True:
    cv2.imshow("Frame", first_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') and len(box_points) == 2:
        break  # Exit loop when 'q' is pressed and box is drawn

cv2.destroyAllWindows()

# Generate points in the bounding box to track
box_points = np.array(box_points)
x1, y1 = box_points[0]
x2, y2 = box_points[1]
# Ensure points are always top-left and bottom-right
x1, x2 = min(x1, x2), max(x1, x2)
y1, y2 = min(y1, y2), max(y1, y2)

# Create an array of points within the bounding box to track
mask = np.zeros_like(first_frame[:, :, 0])
mask[y1:y2, x1:x2] = 1
p0 = cv2.goodFeaturesToTrack(cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY), mask=mask, maxCorners=100, qualityLevel=0.01, minDistance=5)

# Setup Lucas-Kanade parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Open the text file for writing coordinates
with open("tracked_coordinates.txt", "w") as f:
    f.write(f"Bounding box: {x1, y1, x2, y2}\n")

    # Start tracking the points
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow for the points
        p1, st, err = cv2.calcOpticalFlowPyrLK(cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY), gray_frame, p0, None, **lk_params)

        # Select good points (status array == 1 means successfully tracked points)
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # Draw the tracked points on the frame
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
            # Write the coordinates to the text file
            f.write(f"Frame {cap.get(cv2.CAP_PROP_POS_FRAMES)}: {a, b}\n")

        # Show the frame with tracked points
        cv2.imshow("Tracked Frame", frame)

        # Update the previous frame and points
        first_frame = frame.copy()
        p0 = good_new.reshape(-1, 1, 2)

        # Exit if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
