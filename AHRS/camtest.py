#LDFLAGS:  -L/usr/local/opt/opencv3/lib
#CPPFLAGS: -I/usr/local/opt/opencv3/include
#ssh -X pi@128.101.182.192
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
sift = cv2.xfeatures2d.SIFT_create()
fast = cv2.FastFeatureDetector_create()

def run():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        kps = fast.detect(frame, None)
        img = np.zeros((len(frame),len(frame[0])), np.uint8)
        cv2.drawKeypoints(frame, kps, img)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.waitKey(30)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

run()
