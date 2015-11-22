import cv2
import numpy as np
from matplotlib import pyplot as plt

class PuckTracker:
    def __init__(self, template):
        self.template = cv2.imread('templates/' + template + '.png',0)
        self.cap = cv2.VideoCapture(0)
        
    def get_coordinates(self):
        ## This function will return the current coordinates of the puck
        pass
       
    def test_loop(self):
        i = 0
        w, h = self.template.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[i])
        while 1:
            ret, frame = self.cap.read()
            
        
            # Apply template Matching
            res = cv2.matchTemplate(frame,self.template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            
            bottom_right = (top_left[0] + w, top_left[1] + h)
        
            frame = cv2.circle(frame,top_left, bottom_right, 255, 2)
            cv2.imshow('frame',frame)
            #plt.subplot(121),plt.imshow(res, cmap = 'gray')
            #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            #plt.subplot(122),plt.imshow(frame, cmap = 'gray')
            #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            #plt.suptitle(methods[i])
        
            #plt.show()
            
            
             


PuckTracker('puck').test_loop()

