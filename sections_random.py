import cv2 as cv
import numpy as np
import random as rng
from pythonosc import udp_client
import time
import glob
import itertools
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
#######################
firstflag = False
tempy = 0
tempx = 0
whileflag = False
x_index = np.arange(0,10)
y_index = np.arange(0,10)
n = 100
combinations = list(itertools.product(x_index,y_index))
np.random.shuffle(combinations)
selected_combinations = combinations[:n]
x_index,y_index = zip(*selected_combinations)
offsets_x = np.array(x_index) * 50
offsets_y = np.array(y_index) * 50
print(len(offsets_x))
##############
for name in glob.glob('/home/osz//Desktop/desktop_backup/CNN_Images/Mushrooms/Hygrocybe/*'):
      img = cv.imread(name)
      gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
      cv_resized_img = cv.resize(gray, (500, 500), interpolation = cv.INTER_AREA)
      src_gray = cv_resized_img.copy()
      src_gray = cv.blur(src_gray, (3,3))
      threshold = 100
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
      if counter > 100:
            break
      cv.imwrite(path + str(counter) + ".jpg",temp2)
      firstflag = True
      #var_randx =int(index_randx[(rand_indx1[])])
      #var_randy =int(index_randy[(rand_indy1)])
      var_randx = int(offsets_x[counter])
      var_randy = int(offsets_y[counter])
      values.append(path + str(counter) + ".jpg")
      values.append(var_randy)
      values.append(var_randx)
      client.send_message('/img', values)
      values.clear()
      counter += 1
      if counter == 100:
            break
      for x2 in range(50):
            for y2 in range(50):
                  color = (temp2[var_randy + y2][var_randx + x2])
                  if color[0] > 0:
                        values.append(var_randy + y2)
                        values.append(var_randx + x2)
                        client.send_message('/pos', values)
                        client_pd.send_message('/amp',var_randy + y2)
                        client_pd.send_message('/samppos',var_randx + x2)
                        values.clear()
                        time.sleep(0.005)

cv.destroyAllWindows()