# import the necessary packages
from imutils.video import VideoStream
import tkinter as tk
from pyzbar import pyzbar
import imutils
import time
import os
import cv2
import pandas as pd


def BorrowScan2():
    global CurrentData
    CurrentData = '' #Current Scanned ISBN
	
    

    while True:
        print("[ISBN] starting video stream...")
        vs = VideoStream(src=2).start()
        time.sleep(2.0)
        #window.destroy()
        while True:
            flag = 0;
            frame = vs.read()
            frame = imutils.resize(frame, width=720)
            barcodes = pyzbar.decode(frame)
            cv2.putText(frame, "Please Scan Book:", (135,60), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,0),6,2)
            cv2.putText(frame, "Please Scan Book:", (135,60), cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2,2)
            
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
				#print(barcodeType)
                # 
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                if(barcodeType == 'EAN13'):
                    if(CurrentData != barcodeData):
                        CurrentData = barcodeData
                        print("StartSearch!")
                        fields = ['CSVBookName','CSVBookVolume','CSVISBN','CSVPublisher']
                        df=pd.read_csv('barcodes.csv',usecols=fields)
                        #print(len(df.CSVISBN))
                        i = 0
                        for isbn in df.CSVISBN:
                            i = i + 1
                            
                            if isbn == barcodeData:
                                i = i - 1
                                list = [i,df.CSVBookName[i],df.CSVBookVolume[i], df.CSVISBN[i]]
                                if list == None:
                                    print("NotFound")
                                    break
                                else:
                                    print("Found ",list)
                                    flag = 1
                                    os.system('play -nq -t alsa synth {} sine {}'.format(0.2, 1900))
                                    print("[ISBN] cleaning up...")
                                    cv2.destroyAllWindows()
                                    vs.stop()
                                    return list                   
            cv2.imshow("Book Scanner", frame)
            cv2.moveWindow("Book Scanner", 440,150)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("[INFO] cleaning up...")
                cv2.destroyAllWindows()
                vs.stop()
                break
            if (flag == 1):
                os.system('play -nq -t alsa synth {} sine {}'.format(0.2, 1900))
                print("[ISBN] cleaning up...")
                cv2.destroyAllWindows()
                vs.stop()
                break

def AppendCSV():
	print("Opening CSV File.....")
	df = pd.read_csv("barcodes.csv")
	Index = 0
	print(ScannedBookData)
	Index = int(ScannedBookData[0])
	# updating the column value/data
	df.loc[Index, 'CSVAvailability'] = '0'
  
	# writing into the file
	df.to_csv("barcodes.csv", index=False)
	print("Edit Done!")
	#CheckoutWindow.destroy()

ScannedBookData = BorrowScan2()
AppendCSV()