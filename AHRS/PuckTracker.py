import cv2
import numpy as np
import time
#from matplotlib import pyplot as plt

class PuckTracker:
    def __init__(self, height=320, width=240, template='Puck'):
        self.template = cv2.imread('templates/' + template + '.png',0)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, height)
        self.cap.set(4, width)
        
    def get_coordinates(self):
        ## This function will return the current coordinates of the puck
        ret, frame = self.cap.read()
        ## Use frame to find out where puck is
        ## compute center coordinates
        ## return (x, y)
        pass
      
    
    def test_templatematching_loop(self):
        i = 2
        w, h = self.template.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[i])
        while 1:
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            # Apply template Matching
            res = cv2.matchTemplate(frame,self.template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            radius 	= w//2
            center	= (top_left[0] + radius, top_left[1] + radius)
            ## If above produces properly, we dont have to do below
            cv2.circle(frame, center, radius, 255, 2)
            cv2.imshow('frame',frame)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
                
    def test_sift_loop(self):
        sift = cv2.xfeatures2d.SIFT_create()
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # Our operations on the frame come here
            kps = sift.detect(frame, None)
            img = np.zeros((len(frame),len(frame[0])), np.uint8)
            cv2.drawKeypoints(frame, kps, img)
            # Display the resulting frame
            cv2.imshow('frame',frame)
            cv2.waitKey(30)
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
    
    def test_meanshift_loop(self):

        # take first frame of the video
        ret,frame = self.cap.read()

        # setup initial location of window
        # r,h,c,w - region of image
        #           simply hardcoded the values
        r,h,c,w = 200,20,300,20  
        track_window = (c,r,w,h)

        # set up the ROI for tracking
        roi = frame[r:r+h, c:c+w]
        hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

        while(1):
            ret ,frame = self.cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

            # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

            # Draw it on image
            x,y,w,h = track_window
            img2 = cv2.circle(frame, (x + w//2,y + h//2), w//2, 255,2)
            cv2.imshow('frame',img2)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
    
    def test_houghcircles_loop(self):
        while 1:
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT,1,20,
                                        param1=50,param2=30,minRadius=0,maxRadius=0)

            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
                break
            cv2.imshow('detected circles',frame)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
        
    def test_canny_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.Laplacian(frame, cv2.CV_32F)
            cframe = cv2.cvtColor(cframe, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Canny(cframe,300,300)
            #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #frame = cv2.medianBlur(frame,5)
            
            cv2.imshow('canny',cframe)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        
    def test_contours_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame2, contours, -1, (0,255,0), 3)
            cv2.imshow('contours',frame)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
        
    def test_circlecontours_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[4]
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                if radius < 30 or radius > 100:
                    continue
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('contours',frame)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
    
    def test_circlecontours_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[4]
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                if radius < 30 or radius > 100:
                    continue
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('circle contours',frame)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
    
    def test_laplacian_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Laplacian(cframe, cv2.CV_32F)
            cv2.imshow('laplacian',cframe)
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
    
    def test_laplaciancontours_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Laplacian(cframe, cv2.CV_8U)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (0,255,0), 3)
            cv2.imshow('laplacian contours',frame)
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()

    def test_laplaciancontourscircles_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Laplacian(cframe, cv2.CV_8U)
            thresh = np.zeros(frame.size, np.uint8)
            thresh = cv2.erode(thresh, None, 1)
            thresh = cv2.dilate(thresh, None, 1)
            #ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('laplacian contours circles',frame)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()        

    def test_sample_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (9,9), 0)
            cframe = cv2.erode(cframe, None, 1)
            cframe = cv2.dilate(cframe, None, 1)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_BINARY)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                cv2.circle(cframe,center,radius,(0,255,0),2)
            cv2.imshow('Sample',cframe)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows() 

    def test_sobelcontourscircles_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Sobel(cframe,cv2.CV_8U,1,1,ksize=5)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                if radius < 50 or radius > 80:
                    continue
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('laplacian contours circles',frame)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
        
    def test_sobelcontourscircles_loop(self):
        while 1:
            ret, frame = self.cap.read()
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cframe = cv2.GaussianBlur(cframe, (5,5), 0)
            cframe = cv2.Sobel(cframe,cv2.CV_8U,1,1,ksize=5)
            ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                if radius < 50 or radius > 80:
                    continue
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('laplacian contours circles',frame)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows() 
    
    def test_time(self):
        time_start = time.time()
        ret, frame = self.cap.read()
        cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cframe = cv2.GaussianBlur(cframe, (9,9), 0)
        cframe = cv2.erode(cframe, None, 1)
        cframe = cv2.dilate(cframe, None, 1)
        ret, thresh = cv2.threshold(cframe,127,255,cv2.THRESH_BINARY)
        frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = (int(radius))
            cv2.circle(cframe,center,radius,(0,255,0),2)
        time_end  = time.time()
        print("Time to compute all circles: {0}s".format(time_end - time_start))

    def jjrobotsMethodology(self):
        while 1:
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = cv2.GaussianBlur(frame, (5,5), 0)
            thresh = np.zeros(frame.size, np.uint8)
            thresh = cv2.erode(thresh, None, 1)
            thresh = cv2.dilate(thresh, None, 1)
            frame2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.ContourArea(contour)
                if area < 20 or area > 400:
                    break
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = (int(radius))
                if radius < 50 or radius > 80:
                    continue
                cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.imshow('jjrobots in python',frame)
            k = cv2.waitKey(0) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()
    
    
PuckTracker().test_time()

