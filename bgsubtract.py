

import cv2
import numpy as np

def main():
    # Initialize video capture from file
    cap = cv2.VideoCapture('input.mp4')

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Adjustable threshold for detecting change
    change_threshold = 30

    # Minimum number of white pixels to update the bounding box
    min_white_pixel_count = 500  # Adjust this as needed

    # Read the first frame
    ret, first_frame = cap.read()
    if not ret:
        print("Error: Could not read the first frame from video.")
        return

    # Convert the first frame to grayscale
    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # Variable to store the previous bounding box coordinates
    prev_bounding_box = None

    # Variable to store the mask rectangle
    mask_rect = None

    # Let the user draw the mask rectangle
    def draw_rectangle(event, x, y, flags, param):
        nonlocal mask_rect
        if event == cv2.EVENT_LBUTTONDOWN:
            mask_rect = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            mask_rect.append((x, y))

    # Let the user draw the mask rectangle
    print("Draw a rectangle where the mask should always be black.")
    cv2.namedWindow('Draw Mask')
    cv2.setMouseCallback('Draw Mask', draw_rectangle)

    while True:
        temp_frame = first_frame.copy()
        if mask_rect and len(mask_rect) == 2:
            cv2.rectangle(temp_frame, mask_rect[0], mask_rect[1], (0, 255, 0), 2)
        cv2.imshow('Draw Mask', temp_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow('Draw Mask')

    if not mask_rect or len(mask_rect) != 2:
        print("No valid rectangle drawn. Exiting.")
        return

    # Extract the rectangle coordinates
    x1, y1 = mask_rect[0]
    x2, y2 = mask_rect[1]
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    while True:
        # Capture the next frame
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        # Convert the current frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute the absolute difference between the current and the first frame
        diff = cv2.absdiff(gray, first_gray)

        # Create a binary mask based on the threshold
        _, raw_mask_before_rect = cv2.threshold(diff, change_threshold, 255, cv2.THRESH_BINARY)

        # Copy raw mask before applying rectangle
        raw_mask = raw_mask_before_rect.copy()

        # Apply the user-drawn rectangle to the mask
        raw_mask[y1:y2, x1:x2] = 0

        # Create a kernel for the erosion operation (a 3x3 kernel)
        kernel = np.ones((3, 3), np.uint8)

        # Apply erosion to remove white pixels not surrounded by other white pixels
        mask = cv2.erode(raw_mask, kernel, iterations=1)

        # Find the coordinates of the white pixels
        white_pixels = np.where(mask == 255)

        if len(white_pixels[0]) > 0 and len(white_pixels[1]) > 0:
            # Get the bounding box that covers all white pixels
            min_x = np.min(white_pixels[1])
            max_x = np.max(white_pixels[1])
            min_y = np.min(white_pixels[0])
            max_y = np.max(white_pixels[0])

            # If the number of white pixels is greater than the threshold, update the bounding box
            if len(white_pixels[0]) >= min_white_pixel_count:
                prev_bounding_box = (min_x, min_y, max_x, max_y)

        # If no update, carry over the previous bounding box
        if prev_bounding_box is not None:
            min_x, min_y, max_x, max_y = prev_bounding_box
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
            # Add text above the bounding box
            bbox_width = max_x - min_x
            bbox_height = max_y - min_y
            cv2.putText(frame, f"Boomerang: ({min_x}, {min_y}), Size: {bbox_width}x{bbox_height}",
                        (min_x, min_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show the raw mask before applying the rectangle
        cv2.imshow('Raw Mask Before Rectangle', raw_mask_before_rect)
        
        # Show the raw mask and the processed mask
        cv2.imshow('Raw Mask', raw_mask)
        cv2.imshow('Processed Mask', mask)

        # Show the original frame
        cv2.imshow('Video', frame)

        # Wait for a key press to move to the next frame
        key = cv2.waitKey(0)
        if key & 0xFF == ord('q'):
            break

    # Release the video and close windows
    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    main()
