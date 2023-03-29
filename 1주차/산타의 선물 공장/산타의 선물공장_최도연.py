import sys
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

def remove(idx):
    previdx = box[idx][1]
    nextidx = box[idx][2]
    box[idx][4] = 1
    
    box[previdx][2] = nextidx
    box[nextidx][1] = previdx

def push_back(idx):
    beltidx = box[idx][3]
    tailidx = beltidx*2+1
    previdx = box[tailidx][1]

    box[previdx][2] = idx
    box[idx][1] = previdx

    box[idx][2] = tailidx
    box[tailidx][1] = idx

    box[idx][4] = 0

def pull_front(idx):
    beltidx = box[idx][3]
    headidx = beltidx*2
    tailidx = beltidx*2+1

    oldhead = box[headidx][2]
    oldtail = box[tailidx][1]
    newtail = box[idx][1]

    box[headidx][2] = idx
    box[idx][1] = headidx

    box[oldtail][2] = oldhead
    box[oldhead][1] = oldtail
    
    box[newtail][2] = tailidx
    box[tailidx][1] = newtail

def f_200(w_max):
    res = 0
    for i in range(1,m+1):
        # if broken, pass
        if isbroken[i]: continue
        # if empty, pass
        idx = box[2*i][2]
        if idx < startidx: continue

        weight = box[idx][0]
        if weight <= w_max:
            res += weight
            remove(idx)
            # box[idx][4] = 1
        else:
            remove(idx)
            push_back(idx)

    return res

def f_300(r_id):
    # does not exist or already deleted
    idx = d.get(r_id)
    if idx == None or box[idx][4]: return -1

    remove(idx)

    return r_id

def f_400(f_id):
    # does not exist or already deleted
    idx = d.get(f_id)
    if idx == None or box[idx][4]: return -1
    # print("###",idx,box[idx][4])
    if box[idx][1] >= startidx:
        pull_front(idx)

    return box[idx][3]

def f_500(b_num):
    if isbroken[b_num]: return -1
    isbroken[b_num] = 1
    beltidx = b_num
    while True:
        if beltidx+1 > m: beltidx = 1
        else: beltidx += 1
        # beltidx = (beltidx+1) > m ? 
        if isbroken[beltidx] == 0: break
    # print("beltidx:", beltidx)
    movedhead = box[b_num*2][2]
    movedtail = box[b_num*2+1][1]
    travel = movedhead
    end = b_num*2+1
    while True:
        box[travel][3] = beltidx
        travel = box[travel][2]
        if travel == end: break

    tailidx = beltidx*2+1
    oldtail = box[tailidx][1]

    box[oldtail][2] = movedhead
    box[movedhead][1] = oldtail

    box[movedtail][2] = tailidx
    box[tailidx][1] = movedtail

    return b_num

def debug():
    for i in range(m):
        print("###",i,"###")
        # belt[i].traverse()
        print()

q = int(input())
q-=1
t = list(map(int,input().split()))
n,m = t[1],t[2]
startidx = 2*(m+1)
idid = t[3:3+n]
ww = t[3+n:]
d={}
ID = startidx
for _ in range(n):
    d[idid[_]]=ID
    ID+=1

num = n//m
# startidx = 2*(m+1)
# idx = beltidx(1~m) [headidx, tailidx] -1 means NULL
beltinfo=[[]]
for i in range(m):
    beltinfo.append([num*i,num*i+num-1])

# weight, previdx, nextidx, beltidx, deleted
box = [[],[]]
for i in range(m):
    box.append([-1,-1,num*i+startidx,i+1,0])
    box.append([-1,num*i+num-1+startidx,-1,i+1,0])
for i in range(n):
    box.append([ww[i],i-1+startidx,i+1+startidx,i//num+1,0])
for i in range(1,m+1):
    box[box[2*i][2]][1] = 2*i
    box[box[2*i+1][1]][2] = 2*i+1
# print(box)
isbroken = [0]*(1+m)

for _ in range(q):
    cmd,val = map(int, input().split())
    if cmd == 200:
        print(f_200(val))
        # debug()
    elif cmd == 300:
        print(f_300(val))
        # debug()
    elif cmd == 400:
        print(f_400(val))
        # debug()
    elif cmd == 500:
        print(f_500(val))
        # debug()