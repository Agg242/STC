#!python
import pandas as pd
import numpy as np

def read_unidata(catfilter='Lu', casefilter='lowcase', big=False):
    ud = pd.read_csv("ucd/UnicodeData.txt", sep=';', converters={0: lambda x: int(x, base=16)},
                      names=['code', 'name', 'category', 'canclass', 'bidircat', 'chrdecomp',
                             'decdig', 'digval', 'numval', 'mirrored', 'uc1name', 'comment',
                             'upcase', 'lowcase', 'titlecase'],
                      usecols=['code', 'name', 'category', 'bidircat', 'upcase', 'lowcase', 'titlecase'])
    if big:
        ud = ud[ud['code'] >= (1<<16)]
    else:
        ud = ud[ud['code'] < (1<<16)]
    ud = ud[ud['category'] ==  catfilter]
    ud = ud.replace(np.nan, '0')
    for k in ['upcase', 'lowcase', 'titlecase']:
        ud[k] = ud[k].apply(int, base=16)
    if casefilter: # 'lowcase', 'upcase', 'titlecase'
        ud = ud[ud[casefilter] != 0]
    return ud


def read_casefold(big=False):
    cf = pd.read_csv("ucd/CaseFolding.txt", engine='python', sep='; #? ?', comment='#',
                     converters={0: lambda x: int(x, base=16)},
                     names=['code', 'status', 'lowcase', 'name'])
    if big:
        cf = cf[cf['code'] >= (1<<16)]
    else:
        cf = cf[cf['code'] < (1<<16)]
    cf = cf[cf.status.isin(['S', 'C'])]
    cf['lowcase'] = cf['lowcase'].apply(int, base=16)
    #print(cf['name'].values)
    #print(cf)
    return cf


def make_caselist(df):
    letters=[]
    for idx, row in df.iterrows():
        #print(idx+1, ':', row['code'], row['lowcase'] - row['code'], ',', chr(row['code']), chr(row['lowcase']), ',', row['name'])
        letters.append([idx+1, row['code'], row['lowcase'], row['name']])
    return letters


def make_casefold(letters):
    prevoffset = 0
    diffoffset = 0
    prev = [-1, 0, 0]
    diff = [-1, 0, 0]

    out = []
    n = 1
    for x in letters:
        offset = x[2] - x[1]
        diffoffset = prevoffset - offset
        if (diff[1] and x[1] - prev[1] != diff[1]) or (diff[2] and x[2] - prev[2] != diff[2]) or prevoffset != offset:
            out.append([x[1], x[2], n, x[3]]) # , ';', chr(x[1]), chr(x[2]), ';', x[1], offset, "CHANGE")
            #print(x[1], x[2], ';', chr(x[1]), chr(x[2]), ';', offset, "CHANGE", n+1)
            diff[1] = 0
            diff[2] = 0
            n = 1
        else:
            n += 1
            if diff[1] == 0:
                diff[1] = x[1] - prev[1]
                diff[2] = x[2] - prev[2]
            #print(x[1], x[2], ';', chr(x[1]), chr(x[2]), ';', offset)
            diff[1] = x[1] - prev[1]
            diff[2] = x[2] - prev[2]
        prev[2] = x[2]
        prev[1] = x[1]
        prevoffset = offset

    out.append(out[-1])
    out[-1][2] = 26
    cfold = []
    for i in range(0, len(out)-1):
        d = out[i][1] - out[i][0]
        cfold.append([out[i][0], out[i+1][2], d, out[i][3]])
    return cfold


def print_casefold(cfold):
    print('''
struct CaseFold casefold[] = {''')
    n = 1
    s = 5
    count = 0
    table = []
    print('   ', end='')
    for x in cfold:
        d = 2 if abs(x[2]) == 1 else 1
        a = x[0]
        b = x[0] + (x[1] - 1)*d
        c = b + x[2]
        if b >= 1<<16 or c >= 1<<16: # only to make sure...
            break
        #print(' {%d, %d, %d}, // %s %s, %s\n   ' % (a, b, c, chr(a), chr(a + x[2]), x[3]), end='')
        if True: # compact
            if n == s:
                n = 0
                if a > 1000:
                    s = 4
                print('\n   ', end='')
            print(' {%d, %d, %d},' % (a, b, c), end='')
            table.append((a, b, c))
        else:
            print(' {%d, %d, %d}, // ' % (a, b, c), end='')
            for y in range(x[0], x[0] + x[1], d):
                print('%s %s, ' % (chr(y), chr(y + x[2])), end='')
            print('')
        count += 1
        n += 1
    print('\n}; // %d' % (count))
    return table


def make_casetable():
    df = read_casefold()
    #df = read_unidata()
    letters = make_caselist(df)
    cfold = make_casefold(letters)
    return cfold


def print_casefold_low(table):
    cfold_low = [i for i in range(len(table))]
    cfold_low.sort(key=lambda i: table[i][2] - (table[i][1] - table[i][0]))

    print('uint8_t cfold_low[] = {\n   ', end='')
    for i in range(len(cfold_low)):
        print(" %d," % (cfold_low[i]), end='\n   ' if (i+1) % 20 == 0 else '')
    print('\n};')


########### main:

if __name__ == "__main__":
    print('#include "utf8tabs.h"')
    cfold = make_casetable()
    table = print_casefold(cfold)
    print_casefold_low(table)