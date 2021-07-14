import pandas as pd
import re
import zipfile

filename = './data/spamlord.zip'
zip = zipfile.ZipFile(filename, 'r')
files = zip.namelist()

email = r'(?<!\\)([\w\_\-\.]+@(?:[a-z]{2,}\.)+[a-z]{2,4})\b'
phone = r'((?:\d{3}\-){2}\d{4})'

res = {'item': [], 'type': []}

for i in files:
    s = str(zip.read(i))
    emails = re.findall(email,s)
    for j in emails:
        if j not in res['item']:
            res['item'].append(j)
            res['type'].append('email')
    phones = re.findall(phone,s)
    for j in phones:
        if j not in res['item']:
            res['item'].append(j)
            res['type'].append('phone')

df = pd.DataFrame(res, columns=['item', 'type'])
filepath = './result/C_01.csv'
df.to_csv(filepath, index=None)