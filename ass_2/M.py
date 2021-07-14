words = ['in', 'life']

unigram = {}
file = open('./data/count_1w.txt', 'r')
txt = file.read().strip().split('\n')
V = len(txt)
file.close()
for word in txt:
    w, c = tuple(word.split('\t'))
    unigram[w] = int(c)
del txt

bigram = {}
file = open('./data/count_2w.txt', 'r')
txt = file.read().strip().split('\n')
file.close()
for word in txt:
    w, c = tuple(word.split('\t'))
    ws = w.split(' ')
    if (ws[0] ==  words[0]) or (ws[1] in words[1]):
        bigram[tuple(ws)] = int(c)
del txt

def p(first, second, third):
    p1, p2 = 0,0
    bi = bigram.get(tuple([first, second]))
    if bi is None:
        bi = 1
        p1 = bi/(unigram[first]+V)
    else:
        p1 = bi/(unigram[first])
    bi = bigram.get(tuple([second, third]))
    if bi is None:
        bi = 1
        p2 = bi/(unigram[second]+V)
    else:
        p2 = bi/(unigram[second])
    return p1 * p2
    
for i in unigram:
    pr = p('in', i, 'life')
    print(f'{i}\t {pr}')