import pandas as pd
import re
import zipfile

filename = './data/bbc-fulltext.zip'
zip = zipfile.ZipFile(filename, 'r')
files = zip.namelist()

pattern = r'([A-Z]+\w*(?:\s*[A-Z]+\w*)+)'

res = []

for i in files:
    s = str(zip.read(i))
    names = re.findall(pattern,s)
    res += list(filter(len, names))
    
s = pd.Series(res)
s.drop_duplicates(keep='first',inplace=True)
filepath = './result/B_01.csv'
s.to_csv(filepath,index=False, header=False)