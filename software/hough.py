import cv2
import numpy as np


# Finds circles in gray image and matches with white, red and blue mask from original image
def find_circles(image, img_gray, img_color, array_circles):
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, img_gray.shape[0] / 8, param1=50, param2=30, minRadius=10, maxRadius=30)  #  img_gray.shape[0] / 8
    circles = circles_to_array(circles)
    # print(circles)
    filtered_circles = filter_circles(array_circles, circles)
    if filtered_circles:
        matched_circles = match_circles(filtered_circles, img_color)
    else:
        matched_circles = []
    # for i in range(len(circles)):
    #      cv2.circle(image, (circles[i][0], circles[i][1]), circles[i][2], (255, 0, 0), 2)
    #      cv2.circle(image, (circles[i][0], circles[i][1]), 2, (255, 0, 0), 3)
    # for i in range(len(filtered_circles)):
    #      cv2.circle(image, (filtered_circles[i][0], filtered_circles[i][1]), filtered_circles[i][2], (0, 0, 255), 2)
    #      cv2.circle(image, (filtered_circles[i][0], filtered_circles[i][1]), 2, (0, 0, 255), 3)
    for i in range(len(matched_circles)):
        cv2.circle(image, (matched_circles[i][0], matched_circles[i][1]), matched_circles[i][2], (0, 255, 0), 2)
        cv2.circle(image, (matched_circles[i][0], matched_circles[i][1]), 2, (0, 0, 255), 3)
    return image, circles, matched_circles


def find_circles_single_image(image, img_gray, img_color):
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, img_gray.shape[0] / 8, param1=50, param2=30, minRadius=10, maxRadius=30)  #  img_gray.shape[0] / 8
    circles = circles_to_array(circles)
    # print(circles)
    matched_circles = match_circles(circles, img_color)
    # for i in range(len(circles)):
    #     cv2.circle(image, (circles[i][0], circles[i][1]), circles[i][2], (255, 0, 0), 2)
    #     cv2.circle(image, (circles[i][0], circles[i][1]), 2, (255, 0, 0), 3)
    for i in range(len(matched_circles)):
        cv2.circle(image, (matched_circles[i][0], matched_circles[i][1]), matched_circles[i][2], (0, 255, 0), 2)
        cv2.circle(image, (matched_circles[i][0], matched_circles[i][1]), 2, (0, 0, 255), 3)
    return image


# Gets all pixelvalues within found circles
# If pixelvalues are higher than threshold, they get accepted
def match_circles(circles, img):
    values = []
    new_circles = []
    # drawing = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for i in range(len(circles)):
        value = 0
        radius = int(circles[i][2])
        for j in range(int(circles[i][2])):
            for k in range(j):
                value += img[int(circles[i][1]) + radius - j][int(circles[i][0]) + k]  # right under
                value += img[int(circles[i][1]) - radius + j][int(circles[i][0]) + k]  # right up
                value += img[int(circles[i][1]) + radius - j][int(circles[i][0]) - k]  # left under
                value += img[int(circles[i][1]) - radius + j][int(circles[i][0]) - k]  # left up
                # cv2.circle(drawing, (int(circles[i][0]) + k, int(circles[i][1]) + radius - j), 3, (0, 255, 0), 2)
                # cv2.circle(drawing, (int(circles[i][0]) + k, int(circles[i][1]) - radius + j), 3, (0, 255, 0), 2)
                # cv2.circle(drawing, (int(circles[i][0]) - k, int(circles[i][1]) + radius - j), 3, (0, 255, 0), 2)
                # cv2.circle(drawing, (int(circles[i][0]) - k, int(circles[i][1]) - radius + j), 3, (0, 255, 0), 2)
        values.append(value)
        if value > radius * 3500:
            array = [circles[i][0], circles[i][1], circles[i][2]]
            new_circles.append(array)
    # print(values)
    # cv2.imshow("fig", drawing)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return new_circles


# compares circles from last frame with new one
def filter_circles(array_circles, circles):
    new_circles = []

    # Filter circles from array_circles
    for i in range(len(circles)):
        x = circles[i][0]
        y = circles[i][1]
        teller = 0
        for j in range(len(array_circles)):
            for k in range(len(array_circles[j])):
                if abs(array_circles[j][k][0] - x) < 15 and abs(array_circles[j][k][1] - y) < 15:
                    teller += 1
        if teller > 2:
            new_circles.append(circles[i])
    return new_circles


# Convert circles to array
def circles_to_array(circles):
    new_circles = []
    for i in range(len(circles[0])):
        array = [circles[0][i][0], circles[0][i][1], circles[0][i][2]]
        new_circles.append(array)
    circles = new_circles
    return circles
