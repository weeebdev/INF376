import re

shePattern = r'(she\w*)\b'

file = open('./data/count_1w.txt')
txt = file.read()
file.close()
words = re.findall(shePattern, txt)
uniqWords = set(words)

enteredText = 'shep'

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])

    return res


for word in uniqWords:
    print("{:<7s} {:<15s} {:<2d}".format(enteredText, word.strip(), LD(enteredText, word)) )