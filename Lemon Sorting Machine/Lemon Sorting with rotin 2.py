# Lemon Sorting Code  (Hamdard University)
# Start Date: 10-01-2023.
# Author: Muhammad Taha.
# Company: REX ENGINEERING SOLUTIONS

import cv2
import numpy as np
import serial                               # pip install pyserial

ser = serial.Serial('COM1', 9600)
CheckStatus = 0;
color = 0;
discard = 0
discard2 = 0

# Load the video capture object
# You can change the camera port here (e.g: 0,1,2,3,4)
cap = cv2.VideoCapture(0)
# You can change the camera port here (e.g: 0,1,2,3,4)
cap2 = cv2.VideoCapture(1)

# This variable is used to find contour in oval or cicle shape
aspect_ratiouser = 2.6
contoursize = 2500          # Size of Contour
contoursizeRotin = 1500     # Size of Contour Rotin Lemon

# Define the range of green color
lower_green = (40, 40, 40)
upper_green = (80, 255, 255)
# Define the range of yellow color
lower_yellow = (20, 100, 100)
upper_yellow = (40, 255, 255)
# Define the range of brown color (represent rotting)
lower_brown = (10, 50, 20)
upper_brown = (30, 255, 200)
# Define the range of brown color (represent rotting)
lower_black = (0, 0, 0)
upper_black = (180, 30, 50)


# def Lemon_Detector(img):

while True:
    ret, image = cap.read()
    ret2, image2 = cap2.read()

    if ser.inWaiting() > 0 and CheckStatus == 0:
        # Read the available bytes
        data = ser.read(ser.inWaiting())
        datad = data.decode();
        print(data)
        if datad.find("Check") != -1:
            print("Start Testing Image")
            CheckStatus = 1;
            ret, image = cap.read()
            ret2, image2 = cap2.read()
        else:
           print("Wrong Data From Arduino")
           CheckStatus = 0;
    
    if(CheckStatus == 1):
        print("Algorithm Apply")
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Create a mask for the green color range
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        # Create a mask for the yellow color range
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # Create a mask for the brown color range
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        # Create a mask for the brown color range
        black_mask = cv2.inRange(hsv, lower_black, upper_black)
        # Apply morphological operations to remove noise and fill gaps in the masks
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
        brown_mask = cv2.morphologyEx(brown_mask, cv2.MORPH_OPEN, kernel)
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
        # Combine the two masks
        combined_mask = cv2.bitwise_or(green_mask, yellow_mask)
        # Combine the two masks
        rotting_mask = cv2.bitwise_or(brown_mask, black_mask)
    
        # Convert the frame to HSV color space
        hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
        # Create a mask for the green color range
        green_mask2 = cv2.inRange(hsv2, lower_green, upper_green)
        # Create a mask for the yellow color range
        yellow_mask2 = cv2.inRange(hsv2, lower_yellow, upper_yellow)
        # Create a mask for the brown color range
        brown_mask2 = cv2.inRange(hsv2, lower_brown, upper_brown)
        # Create a mask for the brown color range
        black_mask2 = cv2.inRange(hsv2, lower_black, upper_black)
        # Apply morphological operations to remove noise and fill gaps in the masks
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        yellow_mask2 = cv2.morphologyEx(yellow_mask2, cv2.MORPH_OPEN, kernel2)
        green_mask2 = cv2.morphologyEx(green_mask2, cv2.MORPH_OPEN, kernel2)
        brown_mask2 = cv2.morphologyEx(brown_mask2, cv2.MORPH_OPEN, kernel2)
        black_mask2 = cv2.morphologyEx(black_mask2, cv2.MORPH_OPEN, kernel2)
        # Combine the two masks
        combined_mask2 = cv2.bitwise_or(green_mask2, yellow_mask2)
        # Combine the two masks
        rotting_mask2 = cv2.bitwise_or(brown_mask2, black_mask2)
    
        # Find contours in the brown mask
        contours, _ = cv2.findContours(
            rotting_mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Iterate through the contours
        for contour in contours:
            # Get the area of the contour
            area = cv2.contourArea(contour)
            # Get the aspect ratio of the bounding box for the contour
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            # Check if the contour is large and has a low aspect ratio (indicating a round shape)
            if area > contoursizeRotin:
                # Draw the bounding box around the contour
                cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 100, 100), 2)
                # Print a label for the rotting lemon
                cv2.putText(image2, "Rotten Lemon", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 100), 2)
                print("Discard 2")
                discard2 = 1
                ser.write("Reject&".encode())
                CheckStatus = 0
                color = 3
                #print("Rotten Detected")
            else:
                discard2 = 0
                
    
        # Find contours in the brown mask
        contours, _ = cv2.findContours(
            rotting_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Iterate through the contours
        for contour in contours:
            # Get the area of the contour
            area = cv2.contourArea(contour)
            # Get the aspect ratio of the bounding box for the contour
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            # Check if the contour is large and has a low aspect ratio (indicating a round shape)
            if area > contoursizeRotin:
                # Draw the bounding box around the contour
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 100, 100), 2)
                # Print a label for the rotting lemon
                cv2.putText(image, "Rotten Lemon", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 100), 2)
                print("Discard 1")
                discard = 1
                ser.write("Reject&".encode())
                CheckStatus = 0
                color =3
                #print("Rotten Detected")
            else:
                discard = 0
    
        if(discard == 0 and discard2 == 0):
            # Find contours in the Yellow mask
            contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Iterate through the contours
            for contour in contours:
                area = cv2.contourArea(contour)
                # Get the aspect ratio of the bounding box for the contour
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                # Check if the contour is large and has a low aspect ratio (indicating a round shape)
                if area > contoursize and aspect_ratio < aspect_ratiouser:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # Print a label for the rotting lemon
                    cv2.putText(image, "Yellow Lemon", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    print("Yellow Detected")
                    ser.write("Yellow&".encode())
                    color = 1;
    
                # Iterate through the contours
                if color == 0:
                    # Find contours in the Green mask
                    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for contour in contours:
                        # Get the area of the contour
                        area = cv2.contourArea(contour)
                        # Get the aspect ratio of the bounding box for the contour
                        x, y, w, h = cv2.boundingRect(contour)
                        aspect_ratio = w / h
                        # Check if the contour is large and has a low aspect ratio (indicating a round shape)
                        if area > contoursize and aspect_ratio < aspect_ratiouser:
                            # Draw the bounding box around the contour
                            cv2.rectangle(image, (x, y), (x + w, y + h),
                                          (255, 0, 0), 2)
                            # Print a label for the rotting lemon
                            cv2.putText(image, "Green Lemon", (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                            print("Green Detected")
                            ser.write("Green&".encode())
                            color =2;
            
        if(color == 0):
            CheckStatus = 1
            color = 0;
        else:
            CheckStatus = 0
            color = 0;

        
    # Show the image with the rotting lemons highlighted
    cv2.imshow("Sorting & Rotten detection", image)

    # Show the image with the rotting lemons highlighted
    cv2.imshow("Rotten Detection", image2)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.close()
# Release the video capture object
cap.release()
# Release the video capture object
cap2.release()
# Close all the windows
cv2.destroyAllWindows()
