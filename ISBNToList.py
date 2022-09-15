import requests
import json
import pandas as pd

url = 'https://www.nl.go.kr/seoji/SearchApi.do?cert_key=dc580de6947efefaca1baa74e1e77d561172c35140b2bec92a181f74d8ab1ced&result_style=json&page_no=1&page_size=20&isbn='

isbn = '9788925248394'
isbn = '1'
url = url + isbn

response = requests.get(url)

contents = response.text

json_ob = json.loads(contents)

if(json_ob['TOTAL_COUNT'] == '1'):
    print("Hi")
    Total_Count = json_ob["TOTAL_COUNT"]
    Book_Publisher = json_ob['docs'][0]['PUBLISHER']
    Book_ISBN = json_ob['docs'][0]['EA_ISBN']
    Book_Title = json_ob['docs'][0]['TITLE']
    Book_Volume = json_ob['docs'][0]['VOL']
    print(Total_Count)
    print(Book_Title)
    print(Book_Volume)
    print(Book_ISBN)
    print(Book_Publisher)

#docs = json_ob['TOTAL_COUNT']['docs']['PAGE_NO']
#print(docs)

# Dataframe으로 만들기
#dataframe = pd.json_normalize(docs)

#print(dataframe)