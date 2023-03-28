"""
틀리지 않고 구현하는 것이 제일 중요함

"""

from collections import deque
from copy import deepcopy

n,m,k,C = map(int,input().split())
graph  = [list(map(int,input().split())) for _ in range(n)] #-1 벽, 0 빈칸, 1

dr = [0,0,1,-1]
dc = [1,-1,0,0]

def growth(arr) :
    """
    현재 상태에서 성장한 arr를 출력하는 함수
    """
    temp = [[0 for _ in range(n)] for _ in range(n)]

    for r in range(n):
        for c in range(n):
            cnt = 0
            if arr[r][c] > 0 : #나무가 있다면
                for i in range(4):
                    nr,nc = r + dr[i], c + dc[i]
                    if nr < 0 or nr >= n or nc < 0 or nc >= n : continue #밖이거나
                    elif killer[nr][nc] > 0 or arr[nr][nc] == -1 : continue #제초제있거나 벽이거나
                    elif arr[nr][nc] >0 : #주변에 나무가 있을 때
                        cnt +=1
                    else : pass

                arr[r][c] += cnt
    return arr

def copyTree(arr):
    """
    현재 상태에서 복제한 arr를 출력하는 함수
    """
    temp = deepcopy(arr)

    for r in range(n):
        for c in range(n):
            cnt = 0
            lst = []
            if arr[r][c] > 0:  # 나무가 있다면
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]
                    if nr < 0 or nr >= n or nc < 0 or nc >= n:continue  # 벽이 있거나
                    elif killer[nr][nc] > 0 or arr[nr][nc] == -1 : continue #제초제있거나 벽이거나
                    elif arr[nr][nc] == 0 : #기존에 나무가 없는 칸이라면
                        cnt +=1
                        lst.append((nr,nc))

            if cnt > 0 : #번식할 수 있는 칸이 있다면
                for nr,nc in lst :
                    temp[nr][nc] += arr[r][c] // cnt
            else : pass

    return temp

def bfs(r,c,arr):
    """
    현재 위치에서 박멸할 수 있는 칸과 나무의 수 출력하는 함수
    :return: [pos], socre / 하나도 제거하지 못하면 [] , 0 으로 나감
    """
    if arr[r][c] <= 0 or killer[r][c] > 0 : #빈칸이거나 벽이거나 제초제가 뿌려진 곳이라면 태울 수 있는게 없다
        return [] , 0

    direc = [(1,1),(1,-1),(-1,1),(-1,-1)]

    kill = [(r,c)] #해당 위치
    score = arr[r][c] #해당 위치의 나무 수

    for dr,dc in direc :
        for l in range(1,k+1) :
            nr,nc = r + dr * l , c + dc * l
            if nr < 0 or nr >= n or nc < 0 or nc >= n : break #벽이면 아예 끝
            elif arr[nr][nc] == -1 : break #벽이면 아예 끝
            # 빈칸일 때는 추가는 하되 끝
            elif arr[nr][nc] == 0 :
                kill.append((nr,nc))
                break
            # 나무 만나면 계속
            elif arr[nr][nc] > 0 : #빈칸이 아니다
                kill.append((nr,nc))
                score += arr[nr][nc]

    return kill, score

def boom(arr,lst):
    """
    제초제 위치를 갱신 + 현재 나무 상태에서 최고의 박멸 위치를 받아 제거
    갱신이 먼저야
    :return: arr
    """
    global killer
    for r in range(n):
        for c in range(n):
            if killer[r][c] > 0 :
                killer[r][c] -= 1


    for r,c in lst :
        arr[r][c] = 0
        killer[r][c] = C

    return arr

"""process"""
arr = deepcopy(graph)
killer = [[0 for _ in range(n )] for _ in range(n)] #제초제의 위치 및 수명
answer = 0
for t in range(1,m + 1):
    #성장
    arr = growth(arr)
    #번식
    arr = copyTree(arr)

    #박멸 위치 선택
    max_cnt = 0 #이 턴에 최대로 제거한 나무의 수
    max_lst = [] #이 턴에 최대로 제거할 수 있는 제초제의 위치

    for r in range(n):
        for c in range(n):
            kill , cnt = bfs(r,c,arr)
            if max_cnt < cnt : #행과 열이 적은 칸에 제초제를 뿌려야 하니 초과하는 것만 갱신
                max_cnt = cnt
                max_lst = kill
            else :
                pass

    #박멸
    arr = boom(arr,max_lst)
    answer += max_cnt

print(answer)
