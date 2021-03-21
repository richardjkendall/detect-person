# import the necessary packages
import numpy as np
import cv2
import imutils
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Load an color image in grayscale
img = cv2.imread('person.jpg')
img = imutils.resize(img, width=min(800, img.shape[1]))
#frame = cv2.resize(img, (640, 480))
# using a greyscale picture, also for faster detection
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# detect people in the image
# returns the bounding boxes for the detected objects
boxes, weights = hog.detectMultiScale(gray, winStride=(4,4), padding=(8,8), scale=1.05)
print(boxes)

if len(boxes) > 0:
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(img, (xA, yA), (xB, yB),
        (0, 255, 0), 2)

    cv2.imwrite("person_out.jpg", img)

    # Display the resulting frame
    while(True):
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
