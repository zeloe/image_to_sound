import cv2 as cv
import numpy as np
import random as rng
from pythonosc import udp_client
import time
import glob
#index for rows
rowtemp = np.zeros(2501)
indexrow = 0
indexrowy = 0
indexrange = 0
indexrangeoffset = 50
######################
color = 0
######################
client = udp_client.SimpleUDPClient('127.0.0.1', 8000)
client_pd = udp_client.SimpleUDPClient('127.0.0.1', 9000)
######################
values = []
amp = []
samp_pos = []
######################
flagcheck = True

path = '/home/osz/Desktop/the_screaming_sample/'
counter = 0
###################
for name in glob.glob('/home/osz/Desktop/the_screaming_sample/humans_names/*'):
      img = cv.imread(name)
      gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
      cv_resized_img = cv.resize(gray, (500, 500), interpolation = cv.INTER_AREA)
      src_gray = cv_resized_img.copy()
      src_gray = cv.blur(src_gray, (3,3))
      threshold = 25
      # Detect edges using Canny
      canny_output = cv.Canny(src_gray, threshold, threshold * 2)
      # Find contours
      contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
      # Draw contours
      drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
      for i in range(len(contours)):
            color = (255, 255, 255)
            cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
            temp2 = drawing.copy()
      if(indexrow > 450):
            break
      cv.imwrite(path + str(counter) + ".jpg",temp2)
      values.append(path + str(counter) + ".jpg")
      values.append(indexrowy)
      values.append(indexrow)
      client.send_message('/img', values)
      values.clear()
      counter += 1
      for x2 in range(50):
            for y2 in range(50):
                  color = (temp2[indexrowy + y2][indexrow + x2])
                  if color[0] > 0:
                        values.append(indexrowy + y2)
                        values.append(indexrow + x2)
                        client.send_message('/pos', values)
                        client_pd.send_message('/amp',indexrowy + y2)
                        client_pd.send_message('/samppos',indexrow + x2)
                        values.clear()
                        time.sleep(0.01)
      indexrowy += 50
      
      if indexrowy > 450:
            indexrow += 50
            indexrange += 50
            indexrangeoffset += 50
            indexrowy = 0
            if(indexrow > 450):
                  break

cv.destroyAllWindows()