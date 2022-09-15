from imutils.video import VideoStream
import tkinter as tk
from pyzbar import pyzbar
import imutils
import time
import os
import cv2
import pandas as pd
from PIL import Image
from PIL import ImageTk


def BorrowScan2():
    CurrentData = '' #Current Scanned ISBN
    while True:
        print("[ISBN] starting video stream...")
        vs = VideoStream(src=2).start()
        time.sleep(2.0)
        print("Hello")
		
        while True:
            flag = 0;
            frame = vs.read()
            frame = imutils.resize(frame, width=720)
            barcodes = pyzbar.decode(frame)
            
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
                                    return list                   
            cv2.imshow("Book Scanner", frame)
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

        
        


def read(searchitem): 
	while(True):
		fields = ['CSVBookName','CSVBookVolume','CSVISBN','CSVPublisher']
		df=pd.read_csv('barcodes.csv',usecols=fields)
		print(len(df.CSVISBN))
		i = 0
		for isbn in df.CSVISBN:
			i = i + 1

			if isbn == searchitem:
				i = i - 1
				list = [i,df.CSVBookName[i],df.CSVBookVolume[i], df.CSVISBN[i]]
				if list == None:
					print("NotFound")
					break
				else:
					print("Found")
					return list
		print("NotFound! Restarting!")
        

BorrowScan2()