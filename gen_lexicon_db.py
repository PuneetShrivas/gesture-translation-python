import pandas as pd
import math
import numpy as np
from tabulate import tabulate
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
sheet_url = "https://docs.google.com/spreadsheets/d/13ZdCH1jrLM8UjGmXdgRkBlERotjGucG8c4fiVf-pmjM/edit#gid=1213135862"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
result=pd.read_csv(url_1).to_numpy().tolist()
Total_lemmas = result[0][6]
rows = math.floor(Total_lemmas/3)
rem_cols = math.floor(Total_lemmas%3)
lemmas=[]
for i in range(0,rows):
    for j in range(0,3):
        lemmas.append({'text':str(result[11*(i)+9][1+10*(j)]).lower().strip(),'seq':(result[11*(i)+10][1+10*(j)]),'sizeX':str((result[11*(i)+11][1+10*(j)])).split(',')[0],'sizeY':str((result[11*(i)+11][1+10*(j)])).split(',')[1]})


i=i+1
for j in range(0,rem_cols):
        lemmas.append({'text':(result[11*(i)+9][1+10*(j)]),'seq':(result[11*(i)+10][1+10*(j)]),'sizeX':str((result[11*(i)+11][1+10*(j)])).split(',')[0],'sizeY':str((result[11*(i)+11][1+10*(j)])).split(',')[1]})

dataframe=pd.DataFrame(lemmas)
print(dataframe)
dataframe.to_csv(r"./data/dictionary.csv")