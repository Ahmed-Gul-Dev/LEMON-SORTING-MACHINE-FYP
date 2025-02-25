import cv2

cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(1)

while True:
    ret, image = cap.read()
    ret2, image2 = cap2.read()

    #cv2.imwrite("Image.jpg",image2)

    image2 = image2[356:118, 625:114]

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

