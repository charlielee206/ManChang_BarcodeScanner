import pandas as pd



def read(searchitem): 
  fields = ['CSVBookName','CSVBookVolume','CSVISBN','CSVPublisher']
  df=pd.read_csv('barcodes.csv',usecols=fields)
  i = 0
  for isbn in df.CSVISBN:
    i = i + 1
    if isbn == searchitem:
      i = i-1
      print(i)
      print(df.CSVBookName[i])
      return 0
  print("NotFound!")

#df = pd.read_csv('barcodes.csv', skipinitialspace=True, usecols=fields)
# See the keys

#read('9788964071908')
read('177013')
#print (df.keys())
# See content in 'star_name'

#print (df.CSVBookName)

