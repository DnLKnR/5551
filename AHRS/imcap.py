import cv2
import numpy as np
if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # get camera
    _, frame = cap.read()
    cv2.imwrite('image.png', frame)
    print('done')
