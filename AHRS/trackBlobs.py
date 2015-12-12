import cv2
import numpy as np


showColorBlobs = True
showMaskedColors = False

if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # get camera

    #get default vals
    _, frame = cap.read()
    h, w, c = frame.shape # height, width, channels
    dims = (w/4, h/4)
    print(dims)

    # define range of colors in HSV
    lower_yellow = np.array([10, 50, 10])
    upper_yellow = np.array([40, 255, 255])

    lower_blue = np.array([100, 50, 10])
    upper_blue = np.array([140,255,255])

    #lower_green = np.array([50, 50, 20])
    #upper_green = np.array([80, 255, 255]) 

    # track previous and new positions
    yellow_prev_pos = None
    yellow_pos = None
    blue_prev_pos = None
    blue_pos = None
    self_speed = 1


    while(True):
        yellow_prev_pos = yellow_pos
        yellow_pos = None
        blue_prev_pos = blue_pos
        blue_pos = None

        # Take each frame
        _, frame = cap.read()

        #resize image 4x smaller    
        frame = cv2.resize(frame, dims)

        # smooth it
        frame = cv2.blur(frame,(3,3))

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #green_mask = cv2.inRange(hsv, lower_green, upper_green)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        masks = [blue_mask, yellow_mask]
        for a in range(0, len(masks)):
            m = masks[a]
            # find contours in the threshold image
            _, contours, _ = cv2.findContours(m,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            # finding contour with maximum area and store it as best_cnt
            max_area = 0
            best_cnt = None
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt

            # finding centroids of best_cnt and draw a circle there
            if best_cnt is not None and max_area > 200.0: # minimum blob size is 200
                M = cv2.moments(best_cnt)

                """
                these are the centerpoints, for each colored mask m. 
                there will be between 0 and 3 of these, for each mask
                """
                cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                if a == 0:
                    blue_pos = (cx, cy)
                else:
                    yellow_pos = (cx, cy)
                cv2.circle(frame,(cx,cy),5,(0, 255, 0),-1)

        # blue is striker
        if yellow_pos is not None and yellow_prev_pos is not None and blue_pos is not None and blue_prev_pos is not None:
            yellow_speed = (yellow_prev_pos[0]-yellow_pos[0], yellow_prev_pos[1]-yellow_pos[1])
            # if puck is coming towards me, move to intercept
            if yellow_speed[1] < 0:
                x = yellow_pos[0]+yellow_speed[0]*(blue_pos[1]-yellow_pos[1])/yellow_speed[1]
                cv2.circle(frame, (x, blue_pos[1]), 3, (0, 0, 255), -1)

        if showColorBlobs:
            try: 
                cv2.line(frame, yellow_pos, yellow_prev_pos, (0, 255, 255))
            except Exception:
                pass

            cv2.imshow('frame',frame)

        if showMaskedColors:
            mask = blue_mask + green_mask + red_mask
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame, frame, mask= mask)
            cv2.imshow('res',res) # shows combined masks

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()



