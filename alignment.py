'''https://gist.github.com/slowkow/06c6dba9180d013dfd82bec217d22eb5'''

import numpy as np

def nw(x, y, match = 1, mismatch = 1, gap = 1, gap_str='-', diff_str='_'): #Needleman-Wunsch algorithm
    '''
    6 inputs. 'x' and 'y' are the sequences we want to align. 
    'match', 'mismatch', 'gap' are the score used to compute the score matrix in Needleman-Wunsch algorithm, all default to 1, no need to change.
    'gap_str' is the string to represent a 'gap' between ground truth and hypothesis. Default is '-', '〇' is used because it is easier for checking
    '''
    nx = len(x)
    ny = len(y)
    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))
    F[:,0] = np.linspace(0, -nx * gap, nx + 1)
    F[0,:] = np.linspace(0, -ny * gap, ny + 1)
    # Pointers to trace through an optimal aligment.
    P = np.zeros((nx + 1, ny + 1))
    P[:,0] = 3
    P[0,:] = 4
    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if x[i] == y[j]:
                t[0] = F[i,j] + match
            else:
                t[0] = F[i,j] - mismatch
            t[1] = F[i,j+1] - gap
            t[2] = F[i+1,j] - gap
            tmax = np.max(t)
            F[i+1,j+1] = tmax
            if t[0] == tmax:
                P[i+1,j+1] += 2
            if t[1] == tmax:
                P[i+1,j+1] += 3
            if t[2] == tmax:
                P[i+1,j+1] += 4
    # Trace through an optimal alignment.
    i = nx
    j = ny
    rx = []
    ry = []
    while i > 0 or j > 0:
        if P[i,j] in [2, 5, 6, 9]:
            if x[i-1] != y[j-1]:
                rx.append(diff_str)
                ry.append(diff_str)
            rx.append(x[i-1])
            ry.append(y[j-1])

            i -= 1
            j -= 1
        elif P[i,j] in [3, 5, 7, 9]:
            rx.append(x[i-1])
            # ry.append(gap_str)
            # if x[i-1] == ' ' and not y[j-1]:
            #     ry.append(' ')
            # else:
            #     ry.append(gap_str)
            # if x[i-1] != ' ' and j >=0 and j <= len(y):
            #     ry.append(gap_str)
            # else:
            #     ry.append(' ')
                
            if x[i-1] == ' ' and j >=0 and j <= len(y):
                ry.append(' ')
            else:
                ry.append(gap_str)
            i -= 1
        elif P[i,j] in [4, 6, 7, 9]:
            ry.append(y[j-1])
            # if y[j-1] == ' ' and not x[i-1]:
            #     rx.append(' ')
            # else:
            #     rx.append(gap_str)
            # rx.append(gap_str)
            if y[j-1] == ' ' and i >=0 and i <= len(x):
                rx.append(' ')
            else: 
                rx.append(gap_str)
            # if y[j-1] != ' ' and i >=0 and i <= len(x):
            #     rx.append(gap_str)
            # else:
            #     rx.append(' ')
            j -= 1
    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    return rx, ry

def show(GT, HYPO, gap_str='〇'):
    
    gt_a, hypo_a = nw(GT, HYPO, gap_str=gap_str)
    assert len(gt_a) == len(hypo_a)
    print(gt_a)
    print(hypo_a)

def write(GT, HYPO,file):
    
    gt_a, hypo_a = nw(GT, HYPO, gap_str='〇')
    assert len(gt_a) == len(hypo_a)
    idx = 0
    with open(file, 'w', encoding='utf-8') as f:
        
        while idx <len(gt_a):
            last = idx
            idx = gt_a.rfind(' ', idx, idx+100)+1
            f.write(hypo_a[last: idx])
            f.write(gt_a[last: idx])
            

if __name__ == "__main__":
    GT = '踏入2017年維港兩岸有三十三萬人欣賞煙花慶祝各個倒數熱門地點亦人頭湧湧迎接新一年璀璨煙花告別2016人人用手機留住最美一刻期望新一年同樣精彩'
    HYPO = '2017年維港兩岸有三十三萬人欣賞煙花慶祝各個度數據本地點都人頭湧湧迎接新嘅兩電一齊睇下倒數一刻外面有幾咁熱鬧最殘煙花告別2016人用手機留住最靚一刻期望新一年同樣精彩'
    '''
    alignment result: 
    踏入2017年維港兩岸有三十三萬人欣賞煙花慶祝各個倒數熱門地點亦人頭湧湧迎接新〇〇〇〇〇〇〇〇〇一〇〇〇〇〇〇〇年璀璨煙花告別2016人人用手機留住最美一刻期望新一年同樣精彩
    〇〇2017年維港兩岸有三十三萬人欣賞煙花慶祝各個度數據本地點都人頭湧湧迎接新嘅兩電一齊睇下倒數一刻外面有幾咁熱鬧最殘煙花告別2016〇人用手機留住最靚一刻期望新一年同樣精彩
    '''
    show(GT, HYPO)
