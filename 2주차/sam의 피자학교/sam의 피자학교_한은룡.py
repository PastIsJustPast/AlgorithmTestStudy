from copy import deepcopy
N,K = map(int,input().split())
_arr = list(map(int,input().split()))


def adding(arr):
    '''밀가루 추가하는 함수'''
    min_idx = []
    min_value = 1e9
    #최소 찾기
    for idx, value in enumerate(arr):
        if value < min_value :
            min_idx = [idx]
            min_value = value
        elif value == min_value:
            min_idx.append(idx)
        else :
            continue
    #추가하기
    for idx in min_idx:
        arr[idx] +=1
    return arr


def rolling(arr):
    '''
    temp의 행길이와
    '''
    #처음 나누기
    first, second = arr[0],arr[1:]
    temp = [[first]]

    for idx in range(len(second)):
        #열 비교
        ncol = len(temp[0])

        #떼오기
        first,second = second[:ncol],second[ncol:] #슬라이싱이라 모두 리스트

        #합치기
        temp.append(first)

        #행비교
        nrow = len(temp)
        if nrow > len(second):
            break

        #회전
        temp = list(map(list,zip(*temp[::-1])))

    #두 도우 합치기. 마지막행에 추가
    temp[len(temp) - 1] += second

    #빈 열 채우기
    nrow = len(temp[len(temp)-1])
    ncol = len(temp[0])

    #열 맞추기
    for idx in range(len(temp) -1 ):
        temp[idx] += [0 for _ in range(nrow-ncol)]

    return temp

dr = [0,0,1,-1]
dc = [1,-1,0,0]
def flatting(arr_2d):
    nrow = len(arr_2d)
    ncol = len(arr_2d[0])

    temp = [[0 for _ in range(ncol)] for _ in range(nrow)]
    #합계치 구하기
    for r in range(nrow):
        for c in range(ncol):
            if arr_2d[r][c] == 0 : continue
            for i in range(4):
                nr,nc = r+ dr[i], c+dc[i]
                if nr not in range(nrow) or nc not in range(ncol) or arr_2d[nr][nc] == 0 : continue
                diff = abs(arr_2d[r][c] - arr_2d[nr][nc])
                mod = diff // 5
                if mod > 0 :
                    if arr_2d[r][c] > arr_2d[nr][nc] :
                        temp[r][c] -=mod
                        temp[nr][nc] +=mod
                    elif arr_2d[r][c] < arr_2d[nr][nc] :
                        temp[r][c] += mod
                        temp[nr][nc] -= mod
                    else :
                        continue
                else :
                    continue

    #더하기
    for r in range(nrow):
        for c in range(ncol):
            if arr_2d[r][c] == 0: continue
            arr_2d[r][c] += temp[r][c] //2
    #평탄화
    arr = []
    for c in range(ncol):
        for r in range(nrow-1,-1,-1):
            if arr_2d[r][c] != 0 :
                arr.append(arr_2d[r][c])
    return arr


def stacking(arr):
    #한번
    mid = len(arr)//2
    first, second = [arr[:mid]],[arr[mid:]]
    first = list(map(list,zip(*first[::-1])))
    first = list(map(list, zip(*first[::-1])))
    temp = first + second

    #두번
    mid //= 2
    first, second = [lst[:mid] for lst in temp],[lst[mid:] for lst in temp]
    first = list(map(list,zip(*first[::-1])))
    first = list(map(list, zip(*first[::-1])))
    temp = first + second
    return temp







'''process'''
arr = deepcopy(_arr)
for T in range(3000):
    #체크
    if max(arr) - min(arr) <= K :
        break

    #밀가루 추가
    arr = adding(arr)

    #피자 말기
    arr_2d = rolling(arr)

    #피자 평탄화
    arr = flatting(arr_2d)

    #피자 접기
    arr_2d = stacking(arr)

    #피자 평탄화
    arr = flatting(arr_2d)


print(T)
