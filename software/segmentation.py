import cv2
import numpy as np


def segment_color(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(image)
    total = 0
    for i in range(image.shape[1]):
        total += v[10, i]
    if total < 150000:
        val_white = 50
    else:
        val_white = 120

    Rmin = np.array([150, 90, 0])
    Rmax = np.array([255, 255, 255])
    Rmask1 = cv2.inRange(image, Rmin, Rmax)
    Rmin = np.array([0, 90, 0])
    Rmax = np.array([10, 255, 255])
    Rmask2 = cv2.inRange(image, Rmin, Rmax)
    Rmask = Rmask1 + Rmask2

    Bmin = np.array([100, 50, 50])
    Bmax = np.array([140, 255, 255])
    Bmask = cv2.inRange(image, Bmin, Bmax)

    Wmin = np.array([0, 0, val_white])
    Wmax = np.array([255, 50, 255])
    Wmask = cv2.inRange(image, Wmin, Wmax)

    result = Bmask + Wmask + Rmask
    return result


def segmentation_img(new_frame):
    # Colors
    color = segment_color(new_frame)

    # Edges
    img = new_frame
    img = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)
    img = cv2.Canny(img, 80, 250)

    img = img + color
    return img
