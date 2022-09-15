# ManChang_BarcodeScanner
Shite BarcodeScanner/Library Management system with Shite GUI  
  
Requires OpenCV and pyZbar (and zbar).  

Actual Library Management System (Borrow and Return) : Main.py</br>
Add Books to List: barcodescanner3.py  

Barcodes are appended to barcodes.csv.</br>
run RemoveDupe.py to remove duplicate entries in the csv file.  

Book data comes from the korean national library. Thus, an internet connection is required to scan books.</br>
Internet connection is not required to run the management program.  

The main program opens other python scripts using os.</br>
Written for Ubuntu. IDK what works for mac or windows, but you have to change Main.py if you're going to use it on a different operating syste,.</br>
Couldn't be arsed to do it myself.
