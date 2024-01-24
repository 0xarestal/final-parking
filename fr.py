import cv2

# Replace 'PHONE_IP_ADDRESS' with your phone's IP address
url = 'http://192.168.0.110:8080/video'

# Open the video stream
cap = cv2.VideoCapture(url)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Phone Camera', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
