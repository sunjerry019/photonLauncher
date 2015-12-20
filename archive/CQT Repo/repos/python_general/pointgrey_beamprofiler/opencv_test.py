import numpy as np
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    keyp = cv2.waitKey(1)
    # print keyp
    if keyp == ord('p'):
        plt.imshow(frame)
        plt.show()
    elif keyp == ord('q'):
        break
    # if cv2.waitKey(1) & 0xFF == ord('p'):

for i in range(30):
    print(cap.get(i))
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
