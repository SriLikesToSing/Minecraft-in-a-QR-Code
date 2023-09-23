from pyzbar import pyzbar
import argparse
import cv2
import math
from imutils import perspective
import numpy as np
from skimage import color
from skimage import io
import os

STRING = ""

def roundup(x):
    return int(math.ceil(x/100.0) * 100)

def order_points_new(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # if use Euclidean distance, it will run in error when the object
    # is trapezoid. So we should use the same simple y-coordinates order method.

    # now, sort the right-most coordinates according to their
    # y-coordinates so we can grab the top-right and bottom-right
    # points, respectively
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
	help="path to directory of QR codes")
args = vars(ap.parse_args())

#image = cv2.imread(args["image"])

for files in os.listdir(args["directory"]):

    print(files)

    image = cv2.imread("./{}/{}".format(args["directory"],files))

    barcodes = pyzbar.decode(image)

    dictCords = {}
    dictText = {}
    cords = []

    #check if image is processed correctly
    if len(barcodes) != 4:
        print("rescan image bitchass")

    for barcode in barcodes:
        
        (x, y, w, h) = barcode.rect

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

        print("Barcode Cords x:{}, y:{}, w:{}, h:{}".format(x, y, w, h))

        dictText["{}, {}".format(x, y)] = text
        cords.append([x,y])
        dictCords[x] = y

    #cords = sorted(cords, key=lambda k: [k[1], k[0]])

    ordered = order_points_new(np.array(cords))

    cords = (ordered.tolist())

    print(cords)

    print(dictText["{}, {}".format(int(cords[2][0]), int(cords[2][1]))])
    print("-----------------")

    print(dictText["{}, {}".format(int(cords[3][0]), int(cords[3][1]))])
    print("-----------------")

    print(dictText["{}, {}".format(int(cords[1][0]), int(cords[1][1]))])
    print("-----------------")

    print(dictText["{}, {}".format(int(cords[0][0]), int(cords[0][1]))])
    print("-----------------")

    line1 = dictText["{}, {}".format(int(cords[0][0]), int(cords[0][1]))]
    line2 = dictText["{}, {}".format(int(cords[1][0]), int(cords[1][1]))]
    line3 = dictText["{}, {}".format(int(cords[3][0]), int(cords[3][1]))]
    line4 = dictText["{}, {}".format(int(cords[2][0]), int(cords[2][1]))]

    text = line1+line2+line3+line4
    
    text = text.replace(' (QRCODE)', '')

    STRING+=text



    cv2.imwrite("THERESULT.jpg", image)

print(STRING)

#writes base64 output to txt file
with open("OUTPUT.txt", "w") as text_file:
    text_file.write(STRING)

