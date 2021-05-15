import cv2
import glob
import collections
import os
import time
import sys
import numpy as np
from imutils.video import FileVideoStream
from segmentation import segmentation_img
from hough import find_circles, find_circles_single_image
from Kalman import demo_kalman_xy


def iterate_video(filename):
    frames = 0
    start = time.time()
    queue = collections.deque()
    if not os.path.isfile(filename):
        raise Exception("file not found")
    vs = FileVideoStream(filename).start()
    queue.append(vs.read())
    queue.append(vs.read())
    queue.append(vs.read())
    queue.append(vs.read())
    queue.append(vs.read())
    queue.append(vs.read())
    array_circles = collections.deque([[], [], []])
    while vs.running():
        new_frame = vs.read()
        if vs.Q.qsize() == 1:
            break
        original_frame = new_frame
        new_frame = new_frame[180: 550, 200:new_frame.shape[1]]
        queue.append(new_frame)
        queue.popleft()
        img_gray = preprocessing_gray(new_frame)
        img_color = segmentation_img(new_frame)
        try:
            frames += 1
            print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
            result, circles, matched_circles = find_circles(new_frame, img_gray, img_color, array_circles)
            # cv2.imshow("Color", img_color)
            cv2.imshow("Original", original_frame)
            array_circles.append(circles)
            array_circles.popleft()

        except TypeError as exp:
            print(exp)
            print("No circles found")
            # cv2.imshow("Color", img_color)
            cv2.imshow("Original", original_frame)
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            sys.exit()
        elif key == ord('a'):
            break
        if vs.Q.qsize() < 2:  # If we are low on frames, give time to producer
            time.sleep(0.001)  # Ensures producer runs now, so 2 is sufficient


def testbench_images(database):
    start = 0
    while True:
        imgname = glob.glob('images/' + database + '/*.jpg')
        new_frame = cv2.imread(imgname[start])
        if new_frame.shape[0] > 1200:
            new_frame = cv2.resize(new_frame, (1200, 900))
        img_gray = preprocessing_gray(new_frame)
        img_color = segmentation_img(new_frame)
        try:
            result = find_circles_single_image(new_frame, img_gray, img_color)
            cv2.imshow('result image', result)
            # cv2.imshow('Color', img_color)
        except TypeError as exp:
            print(exp)
            print("No circles found")
            cv2.imshow('result image', new_frame)
        cv2.waitKey(0)
        start += 1


def preprocessing_gray(new_frame):
    # Original / Grey
    gray = cv2.cvtColor(new_frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 3)
    return gray


# def increase_brightness(img, value=30):
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)
#
#     lim = 255 - value
#     v[v > lim] = 255
#     v[v <= lim] += value
#
#     lim = 255 - value
#     s[s > lim] = 255
#     s[s <= lim] += value
#
#     final_hsv = cv2.merge((h, s, v))
#     img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
#     return img

# def iterate_video_with_kalman(filename):
#     frames = 0
#     start = time.time()
#     queue = collections.deque()
#     if not os.path.isfile(filename):
#         raise Exception("file not found")
#     vs = FileVideoStream(filename).start()
#     queue.append(vs.read())
#     queue.append(vs.read())
#     queue.append(vs.read())
#     queue.append(vs.read())
#     queue.append(vs.read())
#     queue.append(vs.read())
#     array_circles = collections.deque([[], [], []])
#
#     eerste_cirkel_gedetecteerd = 0
#     aantal_gedetecteerde_verkeersborden = 0
#
#     list_van_kalman_arrays = []
#     array_kalman = []
#
#     # print(array_kalman)
#     # array_kalman.append((120,145,20))
#     # array_kalman.append((112,123,21))
#     # print((array_kalman[0]))
#     # print(array_kalman[0][0][1])
#     array_kalman_x = []
#     array_kalman_y = []
#     while vs.running():
#         new_frame = vs.read()
#         if vs.Q.qsize() == 1:
#             break
#         original_frame = new_frame
#         new_frame = new_frame[180: 550, 200:new_frame.shape[1]]
#         queue.append(new_frame)
#         queue.popleft()
#         img_color = preprocessing_color(new_frame)
#         img_gray = preprocessing_gray(new_frame)
#         try:
#             frames += 1
#             print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
#             result, circles, matched_circles = find_circles(new_frame, img_gray, img_color, array_circles)
#             # cv2.imshow("Frame", result)
#
#             print("array_circles" + str(array_circles))
#             print(matched_circles)
#             x = 1
#             if matched_circles and eerste_cirkel_gedetecteerd == 0:
#                 array_kalman.append(matched_circles[0])
#                 list_van_kalman_arrays.append(array_kalman)
#                 eerste_cirkel_gedetecteerd = 1
#
#             if eerste_cirkel_gedetecteerd == 1:
#                 for i in range(len(list_van_kalman_arrays)):
#                     #print("lengte list_kalman_arrays:" + str(len(list_van_kalman_arrays)))
#                     for j in range(len(matched_circles)):
#                         # print("lengte van matched circles:" + str(len(matched_circles)))
#                         # print(matched_circles[j][0])
#                         # print("type: " + str(type(matched_circles)))
#                         # print("arraykalman[i][j]:" + str(list_van_kalman_arrays[i][j]))
#                         #lengte = len(list_van_kalman_arrays[i])
#                         if (matched_circles[j][0]-10 < list_van_kalman_arrays[i][-1][0]) and  (list_van_kalman_arrays[i][-1][0] < matched_circles[j][0]+10) and (matched_circles[j][1]-10 < list_van_kalman_arrays[i][-1][1]) and  (list_van_kalman_arrays[i][-1][1] < matched_circles[j][1]+10):
#                             print(x)
#                             x = x + 1
#                             lengte = len(list_van_kalman_arrays[i])
#                             if list_van_kalman_arrays[i][lengte-1] != matched_circles[j]:
#                                 list_van_kalman_arrays[i].append(matched_circles[j]) #voeg circkel toe bij verkeersbord dat als gedetecteerd was
#
#                         else:
#
#                             array_kalman.append(matched_circles[j])
#                             list_van_kalman_arrays.append((array_kalman)) #voeg nieuw gedetecteerd verkeersbord toe
#                             aantal_gedetecteerde_verkeersborden = aantal_gedetecteerde_verkeersborden + 1
#
#                         if len(list_van_kalman_arrays[i]) > 10:
#                             list_van_kalman_arrays[i].pop(0) #verwijder de eerste detectie van een verkeersbord dat al tien keer gedetecteerd is zodat er niet te veel vergeleken wordt
#
#                         verschil = len(list_van_kalman_arrays[i])-len(matched_circles)
#                         if len(matched_circles)+2 < len(list_van_kalman_arrays[i]): #dit wil zeggen dat er minder cirkels deze frmae gedetecteerd zijn dan er al verkeersborden gedetecteerd waren
#                             for k in range(verschil-1):
#                                 array_kalman_x.append(list_van_kalman_arrays[i][k][0])
#                                 array_kalman_y.append(list_van_kalman_arrays[i][k][1])
#                                 straal = list_van_kalman_arrays[i][k][2]
#                             # print(array_kalman_x)
#                             #x_matrix = np.matrix([[x], [y], [7], [1]])
#                             x_matrix = np.matrix([[array_kalman_x],[array_kalman_y],[7],[1]])
#                             x,y = demo_kalman_xy(array_kalman_x,array_kalman_y,x_matrix)
#                             array_kalman.append((x[0],y[0],straal))
#                             list_van_kalman_arrays[i][k].append(array_kalman)
#                             cv2.circle(original_frame, (x[0],y[0]), straal,(0, 255, 0), 2)
#                             cv2.circle(original_frame, (x[0],y[0]), 2, (0, 0, 255), 3)
#
#
#                     # print("list kalman: "+ str(list_van_kalman_arrays))
#                 # if not array_kalman_x and matched_circles:
#                 #     for i in range(len(matched_circles)):
#                 #         array_kalman_x.append(matched_circles[i][0])
#                 #         array_kalman_y.append(matched_circles[i][0])
#                 # else:
#             cv2.imshow("Color", img_color)
#             cv2.imshow("Original", original_frame)
#             array_circles.append(circles)
#             array_circles.popleft()
#         except TypeError as exp:
#             # print(exp)
#             # print("No circles found")
#             # cv2.imshow("Frame", new_frame)
#             cv2.imshow("Color", img_color)
#             cv2.imshow("Original", original_frame)
#         key = cv2.waitKey(5)&0xFF
#         if key == ord('q'):
#             sys.exit()
#         elif key == ord('a'):
#             break
#         if vs.Q.qsize() < 2:  # If we are low on frames, give time to producer
#             time.sleep(0.001)  # Ensures producer runs now, so 2 is sufficient

