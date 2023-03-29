``````
하찮은 저의 풀이입니다 ..!!
5번 벨트 고장기능 구현을 하지 못했습니다 ...!

`````````

from collections import deque
q = int(input())

def factoryBuild(inputArr): # 공장 설립
    # print('factoryBuild',inputArr)
    global n
    global m
    global beltArr
    global isBeltArr
    n, m = int(inputArr[0]),int(inputArr[1])
    idArr = inputArr[2:2+n]
    wArr = inputArr[2+n:]
    # beltArr = [deque([]) for _ in range(m)]
    beltArr = [{} for _ in range(m)]
    isBeltArr = [True] * m
    for i in range(len(beltArr)):
        for j in range(i*(n//m),i*(n//m)+(n//m)):
            # beltArr[i].append({'id': int(idArr[j]), 'w': int(wArr[j])})
            # beltArr[i].append({idArr[j]: int(wArr[j])})
            beltArr[i][idArr[j]] = int(wArr[j])
    print("beltArr",beltArr)
    

def boxOff(w_max):
    print('boxOff')
    totalOffw = 0
    for i in beltArr:
        tempArr = deque(i.items())
        # print(tempArr)
        temp = tempArr.popleft()
        # print(temp[1])

        if temp[1] <= w_max:
            totalOffw += temp[1]
            # i 에서 제거 하기
            i.pop(temp[0])
        else:
            tempArr.append(temp)
            i[temp[0]] = temp[1]
            # i 에서 제거 하고 다시 붙이기

        
    # print("beltArr",beltArr)
    return totalOffw


def boxRemove(r_id): # 300
    print('boxRemove')
    isR_id = -1
    for i in beltArr:
        temp = i.keys()
        # print('boxRemove', temp)
        if str(r_id) in temp:
            isR_id = r_id
            i.pop(str(r_id))
            break
    # print("beltArr",beltArr)
    return isR_id


def boxConfirm(f_id):
    print('boxConfirm')
    result = -1
    for i in range(len(beltArr)):
        tempkey = list(beltArr[i].keys())
        tempitem = list(beltArr[i].items())
        print(tempkey,tempitem)
        if str(f_id) in tempkey:
            index = tempkey.index(str(f_id))
            temp = tempitem[index:]
            tempitem = temp + tempitem[:index]
            print("index",index,tempitem)

            temp = {}
            for t in tempitem:
                temp[t[0]] = t[1]
            beltArr[i] = temp
            result = i
            break
    print('confirm beltArr',beltArr)
    return result


def brokenBelt(b_num):
    b_num -= 1
    print('brokenBelt')
    if isBeltArr[b_num]:
        for i in range(b_num+1,len(isBeltArr)):
            if isBeltArr[i]:
                tempitem = list(beltArr[i].items()) + list(beltArr[b_num:].items())
                print('broken',tempitem)
                # temp = {}
                # for t tempitem:
                #     temp[t[0]] = t[1]
                # beltArr[i]
    else:
        return b_num +1

for _ in range(q):
    order = input().split()
    if int(order[0]) == 100:
        factoryBuild(order[1:])

    elif int(order[0]) == 200:
        print(boxOff(int(order[1])))

    elif int(order[0]) == 300:
        print(boxRemove(int(order[1])))

    elif int(order[0]) == 400:
        print(boxConfirm(int(order[1])))

    elif int(order[0]) == 500:
        print(brokenBelt(int(order[1])))
