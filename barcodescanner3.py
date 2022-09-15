# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2
import requests
import json
import pandas as pd
import os

duration = 0.2  # seconds
freq = 1900  # Hz

CurrentData = ''

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=2).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
# open the output CSV file for writing and initialize the set of
# barcodes found thus far
csv = open(args["output"], "a")
found = set()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
	for barcode in barcodes:
		# extract the bounding box location of the barcode and draw
		# the bounding box surrounding the barcode on the image
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		# the barcode data is a bytes object so if we want to draw it
		# on our output image we need to convert it to a string first
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		# draw the barcode data and barcode type on the image
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		

		if(CurrentData != barcodeData):
			CurrentData = barcodeData
			print(barcodeData)

			url = 'https://www.nl.go.kr/seoji/SearchApi.do?cert_key=dc580de6947efefaca1baa74e1e77d561172c35140b2bec92a181f74d8ab1ced&result_style=json&page_no=1&page_size=20&isbn='

			isbn = barcodeData
			url = url + isbn
			
			response = requests.get(url)

			contents = response.text
			print(contents)

			json_ob = json.loads(contents)

			if(json_ob['TOTAL_COUNT'] == '1'):
				Total_Count = json_ob["TOTAL_COUNT"]
				Book_Publisher = json_ob['docs'][0]['PUBLISHER']
				Book_ISBN = json_ob['docs'][0]['EA_ISBN']
				Book_Title = json_ob['docs'][0]['TITLE']
				Book_Volume = json_ob['docs'][0]['VOL']
				#print(Total_Count)
				print(Book_Title)
				os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
				#print(Book_Volume)
				#print(Book_ISBN)
				#print(Book_Publisher)

		# if the barcode text is currently not in our CSV file, write
		# the timestamp + barcode to disk and update the set
				if barcodeData not in found:
					csv.write("{},{},{},{},{}\n".format(
						Book_Title, Book_Volume, Book_ISBN, Book_Publisher,'0'))
					csv.flush()
					found.add(barcodeData)
					
	# show the output frame
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()