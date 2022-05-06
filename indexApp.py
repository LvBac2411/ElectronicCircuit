from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from time import sleep
from threading import Thread
import sqlite3

from matplotlib.pyplot import text
import utils
import FaceRecogni

cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainner.yml')

fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)

window = Tk()
window.title("Face Detection OpenCV")

video = cv2.VideoCapture(0)
canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

canvas = Canvas(window, width = canvas_w, height= canvas_h , bg= "white")
canvas.pack()

photo = None
sampleNum = 0
faceUser = 0

def faceUserBW():
    global faceUser
    faceUser = 1 - faceUser

pane0 = Frame(window)
pane0.pack(fill = BOTH, expand = True)

lbl0 = Label(pane0, text="nhap id")
lbl0.pack(side=LEFT, padx=5, pady=5)

entry0 = Entry(pane0)
entry0.pack(fill=X, padx=5, expand=True)

pane1 = Frame(window)
pane1.pack(fill = BOTH, expand = True)

lbl1 = Label(pane1, text="Tao moi nguoi dung")
lbl1.pack(side=LEFT, padx=5, pady=5)

entry1 = Entry(pane1)
entry1.pack(fill=X, padx=5, expand=True)

pane2 = Frame(window)
pane2.pack(fill = BOTH, expand = True)

buttonUpdate = Button(pane2, text = "nhan dien", command=faceUserBW)
buttonUpdate.pack(side=LEFT, pady=5)

buttonExit = Button(pane2,text="Exit")
buttonExit.pack(side=RIGHT)

pane3 = Frame(window)
pane3.pack(fill = BOTH, expand = True)

def saveImg():
    global sampleNum
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    centerH = frame.shape[0] // 2
    centerW = frame.shape[1] // 2
    sizeboxW = 300
    sizeboxH = 400
    cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)
    if(entry1.get()==''):
        messagebox.showerror('erorr','chua nhap ten nguoi dung')
        return
    if(entry0.get()==''):
        messagebox.showerror('erorr','chua nhap id')
        return
    sampleNum += 1
    utils.WriteFace(frame, entry1.get(), sampleNum, entry0.get())
    print(sampleNum)
    if(sampleNum > 99):
        FaceRecogni.insertOrUpdate(int(entry0.get()),str(entry1.get()))
        print(int(entry0.get()))
        sampleNum = 0

button = Button(pane3,text = "Black & White")
button.pack(side=RIGHT)

buttonSave = Button(pane3,text = "Save", command=saveImg)
buttonSave.pack(side=LEFT, pady=5)

count = 0

#api(update)
def send_to_server():
    sleep(5)
    return

def update_frame():
    global canvas, photo, count
    # Doc tu camera
    ret, frame = video.read()

    frame = cv2.flip(frame, 1)

    centerH = frame.shape[0] // 2
    centerW = frame.shape[1] // 2
    sizeboxW = 300
    sizeboxH = 400
    cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    if faceUser==0:
        frame = utils.FaceRec(frame)
    else:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=detector.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            # Vẽ hình chữ nhật quanh mặt
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            # Nhận diện khuôn mặt, trả ra 2 tham số id: mã nhân viên và dist (dộ sai khác)
            id,dist=recognizer.predict(gray[y:y+h,x:x+w])

            profile=None
            #cv2.imshow("test",gray[y:y+h,x:x+w])
            # Nếu độ sai khác < 28% thì lấy profile
            if (dist<=65):
                print(dist)
                profile=FaceRecogni.getProfile(id)

            # Hiển thị thông tin tên người hoặc Unknown nếu không tìm thấy
            if(profile!=None):
                cv2.putText(frame, "Name: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
            else:
                cv2.putText(frame, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor1, 2)
    # Convert hanh image TK
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    # Show
    canvas.create_image(0,0, image = photo, anchor=tkinter.NW)

    count = count +1
    if (sampleNum>0 and sampleNum<100):
        #send_to_server()
        saveImg()
        # thread = Thread(target=saveImg)
        # thread.start()

    window.after(15, update_frame)

update_frame()

window.mainloop()
