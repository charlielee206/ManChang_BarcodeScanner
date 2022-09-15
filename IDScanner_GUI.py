# import the necessary packages
from imutils.video import VideoStream
import tkinter as tk
from pyzbar import pyzbar
import imutils
import time
import os
import cv2
import pandas as pd

CurrentUser = ''



def IDScanning():
	CurrentData = ''

	print("[ID] starting video stream...")
	vs = VideoStream(src=2).start()
	time.sleep(2.0)

	while True:
		flag = 0;
		frame = vs.read()
		frame = imutils.resize(frame, width=720)
		cv2.putText(frame, "Please Scan Your ID:", (115,60), cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,0),6,2)
		cv2.putText(frame, "Please Scan Your ID:", (115,60), cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),2,2)
		
		barcodes = pyzbar.decode(frame)

		for barcode in barcodes:
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

			if(barcodeType == 'CODE39'):
				if(CurrentData != barcodeData):
					CurrentData = barcodeData
					#print(barcodeData)
					flag = 1

		
		#cv2.namedWindow("Student ID Scanner", cv2.WND_PROP_FULLSCREEN)
		#cv2.setWindowProperty("Student ID Scanner",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		cv2.imshow("Student ID Scanner", frame)
		cv2.moveWindow("Student ID Scanner", 440,150)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			print("[ID] cleaning up...")
			cv2.destroyAllWindows()
			vs.stop()
			break
		
		if (flag == 1):
			os.system('play -nq -t alsa synth {} sine {}'.format(0.2, 880))
			os.system('play -nq -t alsa synth {} sine {}'.format(0.2, 1300))
			
			print("[ID] cleaning up...")
			cv2.destroyAllWindows()
			vs.stop()
			return barcodeData
			#break

def BorrowScan2():
    CurrentData = '' #Current Scanned ISBN
	
    

    while True:
        print("[ISBN] starting video stream...")
        vs = VideoStream(src=2).start()
        time.sleep(2.0)
        window.destroy()
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
                        print(barcodeData)
                        fields = ['CSVBookName','CSVBookVolume','CSVISBN','CSVPublisher','CSVAvailability']
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
	Index = int(ScannedBookData[0]) # Ignore first line + start at 0 --> Index is 2 less than the line no. in barcodes.csv
	# updating the column value/data
	df.loc[Index, 'CSVAvailability'] = CurrentUser
  
	# writing into the file
	df.to_csv("barcodes.csv", index=False)
	print("Edit Done!")
	CheckoutWindow.destroy()


def CheckoutScreen():
	global CheckoutWindow
	global ScannedBookData
	ScannedBookData = ['','','','','']
	CheckoutWindow = tk.Tk()
	CheckoutWindow.title("CheckOut")
	CheckoutWindow.geometry("1600x900")
	CheckoutWindow.attributes('-fullscreen',True)
	CheckoutWindow.configure(background = 'black')

	ScannedBookData = BorrowScan2()
	print("CurrentISBN:")
	print(ScannedBookData)
	#ScannedBookData[0] = Index, [1] = Name, [2] = Volume, [3] = ISBN, [4] = Availability

	if ScannedBookData == None:
		print("Error!")
		return -1

	btn_Cancel = tk.Button(
		master=CheckoutWindow,
		text="[Cancel]",
		relief = 'flat',
		bg = 'black',
		fg = 'white',
		font = ('Consolas',20),
		command=CheckoutWindow.destroy
	)

	btn_Okay = tk.Button(
		master = CheckoutWindow,
		text = "[OK]",
		relief = 'flat',
		bg = 'black',
		fg = 'white',
		font = ('Consolas',20),
		command = AppendCSV
		)

	
	GreetText = 'Is the Information Correct?'
	LabelText = '>> User: '
	LabelText = LabelText + CurrentUser
	BookText = '>> Book: '
	BookText = BookText + ScannedBookData[1]
	VolumeText = '>> Volume: '
	if str(ScannedBookData[2]) == '' or ScannedBookData[2] == ' ' or str(ScannedBookData[2]) == 'nan':
		VolumeText = ''
	else:
		VolumeText = VolumeText + str(ScannedBookData[2])


	lbl_Title = tk.Label(CheckoutWindow,font=("Consolas",8), 
        text = "          _____                    _____                            _____                            _____                            _____                            _____                        _____           \n         /\    \                  /\    \                          /\    \                          /\    \                          /\    \                          /\    \                      /\    \          \n        /::\____\                /::\    \                        /::\    \                        /::\____\                        /::\    \                        /::\____\                    /::\    \         \n       /:::/    /                \:::\    \                      /::::\    \                      /::::|   |                       /::::\    \                      /::::|   |                    \:::\    \       \n      /:::/    /                  \:::\    \                    /::::::\    \                    /:::::|   |                      /::::::\    \                    /:::::|   |                     \:::\    \       \n     /:::/    /                    \:::\    \                  /:::/\:::\    \                  /::::::|   |                     /:::/\:::\    \                  /::::::|   |                      \:::\    \      \n    /:::/    /                      \:::\    \                /:::/__\:::\    \                /:::/|::|   |                    /:::/  \:::\    \                /:::/|::|   |                       \:::\    \     \n   /:::/    /                       /::::\    \              /::::\   \:::\    \              /:::/ |::|   |                   /:::/    \:::\    \              /:::/ |::|   |                       /::::\    \    \n  /:::/    /               ____    /::::::\    \            /::::::\   \:::\    \            /:::/  |::|___|______            /:::/    / \:::\    \            /:::/  |::|___|______                /::::::\    \   \n /:::/    /               /\   \  /:::/\:::\    \          /:::/\:::\   \:::\ ___\          /:::/   |::::::::\    \          /:::/    /   \:::\ ___\          /:::/   |::::::::\    \              /:::/\:::\    \  \n/:::/____/               /::\   \/:::/  \:::\____\        /:::/__\:::\   \:::|    |        /:::/    |:::::::::\____\        /:::/____/  ___\:::|    |        /:::/    |:::::::::\____\            /:::/  \:::\____\ \n\:::\    \               \:::\  /:::/    \::/    /        \:::\   \:::\  /:::|____|        \::/    / ~~~~~/:::/    /        \:::\    \ /\  /:::|____|        \::/    / ~~~~~/:::/    /           /:::/    \::/    / \n \:::\    \               \:::\/:::/    / \/____/          \:::\   \:::\/:::/    /          \/____/      /:::/    /          \:::\    /::\ \::/    /          \/____/      /:::/    /           /:::/    / \/____/  \n  \:::\    \               \::::::/    /                    \:::\   \::::::/    /                       /:::/    /            \:::\   \:::\ \/____/                       /:::/    /           /:::/    /           \n   \:::\    \               \::::/____/                      \:::\   \::::/    /                       /:::/    /              \:::\   \:::\____\                        /:::/    /           /:::/    /            \n    \:::\    \               \:::\    \                       \:::\  /:::/    /                       /:::/    /                \:::\  /:::/    /                       /:::/    /            \::/    /             \n     \:::\    \               \:::\    \                       \:::\/:::/    /                       /:::/    /                  \:::\/:::/    /                       /:::/    /              \/____/              \n      \:::\    \               \:::\    \                       \::::::/    /                       /:::/    /                    \::::::/    /                       /:::/    /                                    \n       \:::\____\               \:::\____\                       \::::/    /                       /:::/    /                      \::::/    /                       /:::/    /                                     \n        \::/    /                \::/    /                        \::/____/                        \::/    /                        \::/____/                        \::/    /                                      \n         \/____/                  \/____/                          ~~                               \/____/                                                           \/____/                                       \n                                                                                                                                                                                                                   ",
        bg = 'black', fg = 'White')
	lbl_GreetText = tk.Label(master = CheckoutWindow, text = GreetText, bg = 'black', fg = 'white', font = ("Consolas",25))
	lbl_UserName = tk.Label(master = CheckoutWindow, text = LabelText, bg = 'black', fg = 'white', font = ("Consolas",20))
	lbl_Bookname = tk.Label(master = CheckoutWindow, text = BookText, bg = 'black', fg = 'white', font = ("Consolas",20))
	lbl_VolumeName = tk.Label(master = CheckoutWindow, text = VolumeText, bg = 'black', fg = 'white', font = ("Consolas",20))

	lbl_Title.pack(pady = 20)
	lbl_GreetText.pack(pady=5)
	lbl_UserName.pack(pady=5)
	lbl_Bookname.pack(pady=5)
	lbl_VolumeName.pack(pady=5)
	btn_Okay.pack(pady=10)
	btn_Cancel.pack(pady=5)

	

	CheckoutWindow.mainloop()



CurrentBook = ''
window = tk.Tk()
window.title("Loginpage")
window.geometry("1600x900")
window.attributes('-fullscreen',True)
window.configure(background = 'black')

lbl_Title = tk.Label(window,font=("Consolas",8), 
        text = "          _____                    _____                            _____                            _____                            _____                            _____                        _____           \n         /\    \                  /\    \                          /\    \                          /\    \                          /\    \                          /\    \                      /\    \          \n        /::\____\                /::\    \                        /::\    \                        /::\____\                        /::\    \                        /::\____\                    /::\    \         \n       /:::/    /                \:::\    \                      /::::\    \                      /::::|   |                       /::::\    \                      /::::|   |                    \:::\    \       \n      /:::/    /                  \:::\    \                    /::::::\    \                    /:::::|   |                      /::::::\    \                    /:::::|   |                     \:::\    \       \n     /:::/    /                    \:::\    \                  /:::/\:::\    \                  /::::::|   |                     /:::/\:::\    \                  /::::::|   |                      \:::\    \      \n    /:::/    /                      \:::\    \                /:::/__\:::\    \                /:::/|::|   |                    /:::/  \:::\    \                /:::/|::|   |                       \:::\    \     \n   /:::/    /                       /::::\    \              /::::\   \:::\    \              /:::/ |::|   |                   /:::/    \:::\    \              /:::/ |::|   |                       /::::\    \    \n  /:::/    /               ____    /::::::\    \            /::::::\   \:::\    \            /:::/  |::|___|______            /:::/    / \:::\    \            /:::/  |::|___|______                /::::::\    \   \n /:::/    /               /\   \  /:::/\:::\    \          /:::/\:::\   \:::\ ___\          /:::/   |::::::::\    \          /:::/    /   \:::\ ___\          /:::/   |::::::::\    \              /:::/\:::\    \  \n/:::/____/               /::\   \/:::/  \:::\____\        /:::/__\:::\   \:::|    |        /:::/    |:::::::::\____\        /:::/____/  ___\:::|    |        /:::/    |:::::::::\____\            /:::/  \:::\____\ \n\:::\    \               \:::\  /:::/    \::/    /        \:::\   \:::\  /:::|____|        \::/    / ~~~~~/:::/    /        \:::\    \ /\  /:::|____|        \::/    / ~~~~~/:::/    /           /:::/    \::/    / \n \:::\    \               \:::\/:::/    / \/____/          \:::\   \:::\/:::/    /          \/____/      /:::/    /          \:::\    /::\ \::/    /          \/____/      /:::/    /           /:::/    / \/____/  \n  \:::\    \               \::::::/    /                    \:::\   \::::::/    /                       /:::/    /            \:::\   \:::\ \/____/                       /:::/    /           /:::/    /           \n   \:::\    \               \::::/____/                      \:::\   \::::/    /                       /:::/    /              \:::\   \:::\____\                        /:::/    /           /:::/    /            \n    \:::\    \               \:::\    \                       \:::\  /:::/    /                       /:::/    /                \:::\  /:::/    /                       /:::/    /            \::/    /             \n     \:::\    \               \:::\    \                       \:::\/:::/    /                       /:::/    /                  \:::\/:::/    /                       /:::/    /              \/____/              \n      \:::\    \               \:::\    \                       \::::::/    /                       /:::/    /                    \::::::/    /                       /:::/    /                                    \n       \:::\____\               \:::\____\                       \::::/    /                       /:::/    /                      \::::/    /                       /:::/    /                                     \n        \::/    /                \::/    /                        \::/____/                        \::/    /                        \::/____/                        \::/    /                                      \n         \/____/                  \/____/                          ~~                               \/____/                                                           \/____/                                       \n                                                                                                                                                                                                                   ",
        bg = 'black', fg = 'White')


CurrentUser = ''


btn_Exit = tk.Button(
	master=window,
	text="[Exit]",
	relief = 'flat',
	bg = 'black',
	fg = 'white',
	font = ('Consolas',20),
	command=window.destroy
)
btn_Borrow = tk.Button(
	master = window,
	text = "[Borrow]",
	relief = 'flat',
	bg = 'black',
	fg = 'white',
	font = ('Consolas',20),
	command = CheckoutScreen
	)
	
CurrentUser = IDScanning()
	
	
print("Current User: ", CurrentUser)
LabelText = 'Current User: ['
LabelText = LabelText + CurrentUser + ']'
lbl_Greet = tk.Label(window, text = "Welcome!", bg = 'black', fg = 'white', font = ("Consolas",20))
lbl_UserName = tk.Label(window, text = LabelText, bg = 'black', fg = 'white', font = ("Consolas",13))


lbl_Title.pack(pady = 20)
lbl_Greet.pack(pady = 10)
lbl_UserName.pack(pady=10)
btn_Borrow.pack(pady=5)
btn_Exit.pack(pady=5)


window.mainloop()
	
