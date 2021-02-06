words = ['in', 'dairy', 'life', 'daisy', 'daily', 'fairy', 'fail']

unigram = {}
file = open('./data/count_1w.txt', 'r')
txt = file.read().strip().split('\n')
V = len(txt)
file.close()
for word in txt:
    w, c = tuple(word.split('\t'))
    if w in words:
        unigram[w] = int(c)
del txt

bigram = {}
file = open('./data/count_2w.txt', 'r')
txt = file.read().strip().split('\n')
file.close()
for word in txt:
    w, c = tuple(word.split('\t'))
    ws = w.split(' ')
    if (ws[0] in words) and (ws[1] in words):
        bigram[tuple(ws)] = int(c)
del txt


options = ['dairy', 'daisy', 'daily', 'fairy', 'fail']

for i in options:
    pr = p('in', i, 'life')
    print(f'{i}\t {pr}')