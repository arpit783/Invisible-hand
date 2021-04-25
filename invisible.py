import cv2
import numpy as np
import time
  
# replace the skin color pixels ( or undesired area ) with
# background pixels to generate the invisibility feature. 
  
# taking video.mp4 as input.
capture_video = cv2.VideoCapture('1.mp4')
     
# give the camera to warm up
time.sleep(1) 
count = 0 
background = 0 
  
# capturing the background in range of 60
# to save the background image
for i in range(60):
    return_val, background = capture_video.read()
    if return_val == False :
        continue 
  
background = np.flip(background, axis = 1) # flipping of the frame 
  
# we are reading from video 
while (capture_video.isOpened()):
    return_val, img = capture_video.read()
    if not return_val :
        break 
    count = count + 1
    img = np.flip(img, axis = 1)
  
    # convert the image - BGR to HSV
    # as we focused on detection of skin color 
  
    # converting BGR to HSV for better detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
  
    # lower and upper range for mask1
    lower_skin = np.array([0, 48, 80])       
    upper_skin = np.array([20, 255, 255])
    mask1 = cv2.inRange(hsv, lower_skin, upper_skin)
    # setting the lower and upper range for mask2 
    lower_skin = np.array([108, 23, 82])
    upper_skin = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, lower_skin, lower_skin)
    mask1 = mask1 + mask2
  
    # Refining the mask corresponding to the detected skin color
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                         np.uint8), iterations = 2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1)
    mask2 = cv2.bitwise_not(mask1)
  
    # Generating the final output
    res1 = cv2.bitwise_and(background, background, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
  
    cv2.imshow("DISAPPEAR HAND", final_output)
    k = cv2.waitKey(10)
    if k == 27:
        break