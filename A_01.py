import pandas as pd
import re

# Task 1
# Actually, I don't know how to deal with the names like НҮРДІБЕК БАЛЖАН, because they can be both M and F

file_name = './data/State Grants 2020.xlsx' 
df = pd.concat(pd.read_excel(file_name, sheet_name=[0,1,2,3,4]), ignore_index=True)[:-1]

M = r'ұлы|улы|уғли|угли|вич|ов|ев[^\w]'
F = r'қызы|кызы|қизи|кизи|вна|вна|ова|ева[^\w]'

def identifyGender(FIO):
    FIO = FIO.lower()
    if (re.search(F, FIO)):
        return 'F'
    if (re.search(M, FIO)):
        return 'M'
    return ''

df['Gender'] = df.apply(lambda row: identifyGender(row.FIO), axis = 1)
file_path = './result/A_01.csv'
df.to_csv(file_path, columns=['FIO', 'Gender'])

# bigender = df[df['Gender'] == '']
# bigender.to_csv('bigender.csv')
# print(bigender)
# AS you can see, still 116 students have bigender names


