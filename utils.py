import os
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def filterImg(path="Media/CD.jpg"):
    outpath = "MediaEdit" + os.sep + os.path.basename(path)
    img = cv2.imread(path)
    blur = cv2.bilateralFilter(img, 9, 60, 60)
    cv2.imwrite(outpath, blur)
    return outpath

# tim canh bang


def CannyDetection(path="Media/CD.jpg", percentage=100):
    img = cv2.imread(path)
    edges = cv2.Canny(img, 100, 200)
    edges = _Percentage(edges, percentage)
    outpath = "MediaEdit" + os.sep + os.path.basename(path)
    cv2.imwrite(outpath, edges)
    return outpath


# Nhan dien khuon mat
def FaceRec(img, percentage=100):
    # img=cv2.imread(path)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    img = _Percentage(img, percentage)
    #pathFace = "MediaEdit" + os.sep + os.path.basename(path)
    # cv2.imwrite(pathFace,img)
    return img


def WriteFace(img, name, sampleNum, Id):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Ghi dữ liệu khuôn mặt vào thư mục dataSet
        cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) +
                    ".jpg", gray[y:y + h, x:x + w])


# chinh kich co anh
def _Percentage(img, per):
    scale_percent = per
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

# img = decodeImg("tet.txt")
# cv2.imshow("data", img)
# cv2.waitKey(0)
#encodeImg("D:\Pictures\clock.jpg", "encodedData.json")
