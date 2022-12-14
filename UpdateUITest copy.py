import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from pyzbar import pyzbar

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.entery = ''
        global CurrentScanned 
        CurrentScanned = ''
        global CurrentType
        self.LastScanned = ''
        CurrentType = ''


         # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        print(CurrentScanned)

        if (self.LastScanned != CurrentScanned):
            self.Lastcanned = CurrentScanned
            print("1")
            if (CurrentType == 'EAN13'):
                print(CurrentScanned)
 
         # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
 
        self.ent_Manual = tkinter.Entry(window, width = 50)
        self.ent_Manual.pack(anchor=tkinter.CENTER, expand = True)

         # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
 
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
 
        self.window.mainloop()
 
    def snapshot(self):
        if self.entery == '':
            self.entery = self.ent_Manual.get()
        print(self.entery)
        return(self.entery)
 
    def update(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source=2):
         # Open the video source
        self.vid = cv2.VideoCapture(2)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
			        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                CurrentScanned = barcodeData
                CurrentType = barcodeType
                

            if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
 
     # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
           self.vid.release()
 
 # Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")