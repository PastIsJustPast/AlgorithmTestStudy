'''
인자 헷갈리는거 진짜 하지말자..
i,j,r,c 이런거 안 헷갈리게 잘 해야함 조금이라도 글로벌 느낌나면 무조건 대문자!
시계 반시계 아예 외워


'''

from copy import deepcopy
from collections import deque

n,m,k = map(int,input().split())
#Graph = [list(map(int,input().split())) for _ in range(n)]
Graph = []
for info in input().split('\n'):
    Graph.append(list(map(int,info.split())))

Head_man = []
for i in range(n):
    for j in range(n):
        if Graph[i][j] == 1:
            Head_man.append((i,j))
dr = [0,0,1,-1]
dc = [1,-1,0,0]
#그릅 정보 찾기
def get_graph_info():
    """그륩 정보를 반환하는 함수
    return  dict(num, deque(), [])
    """
    graph_info = {}
    for num, pos in enumerate(Head_man):
        r,c = pos
        train,rail = deque(),list()
        train.append((r,c))
        rail.append((r,c))

        q = deque()
        q.append((r,c))
        visited = [[False for _ in range(n)] for _ in range(n)]
        visited[r][c] =True
        while q :
            r,c = q.popleft()
            if Graph[r][c] <= 2:
                # 첫 몸통 찾기
                for i in range(4):
                    nr,nc = r + dr[i] , c + dc[i]
                    if nr in range(n) and nc in range(n) and not visited[nr][nc] and Graph[nr][nc] > 0 :  #몸통이나 꼬리 찾기
                        if Graph[nr][nc] == 2 or Graph[nr][nc] ==3 :
                            visited[nr][nc] = True
                            train.append((nr, nc))
                            rail.append((nr, nc))
                            q.append((nr, nc))
                            break
                        else :
                            continue #레일이 나와도 튕기기
                    else :
                        continue
            else: #꼬리던 레일이던 레일만 찾기
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]
                    if nr in range(n) and nc in range(n) and not visited[nr][nc] and Graph[nr][nc] > 0 :  #
                        if Graph[nr][nc] == 4 :
                            visited[nr][nc] = True
                            rail.append((nr, nc))
                            q.append((nr, nc))
                            break
                        else :
                            continue
                    else :
                        continue

        graph_info[num] = (train, rail)
    return graph_info

#이동
def move_train(train,rail):
    if not isinstance(train,deque) :
        raise TypeError("Not Deque")
    if not isinstance(rail,list) :
        raise TypeError("Not rail")
    #첫 주자
    head_man = "Not tuple"
    temp = deepcopy(train)
    temp.pop()
    

    r,c = train[0]
    for i in range(4):
        nr,nc = r + dr[i] , c + dc[i]
        if nr not in range(n) or nc not in range(n) or Graph[nr][nc] == 0 : continue
        if (nr,nc) not in temp and (nr,nc) in rail : #이동 위치
            head_man = (nr,nc)
            break
        else :
            continue
    if head_man == "Not tuple": raise ValueError("Not Head Man")

    #엮기
    train.pop()
    train.appendleft(head_man) #제일 처음 넣기

    return train

#선물 경로
def get_gift_lst(round):
    round = round % (n * 4)
    dir = round // n
    d = round % n
    #거리
    gift_lst = [(d,i) for i in range(n)]
    #방향
    for _ in range(dir):
        gift_lst = [(n-1-c,r) for r,c in gift_lst]
    return gift_lst

def get_receiver(gift_lst):
    num_group, score = "NaN", 0
    for num in Graph_info.keys():
        train, rail = Graph_info[num]
        for gr,gs in gift_lst:
            if (gr,gs) in train :
                num_group = num
                score = train.index((gr,gs)) + 1
                return num_group, score **2
    return num_group, score ** 2

def print_graph(graph_info):
    temp = [[0 for _ in range(n)] for _ in range(n)]
    for num in graph_info.keys():
        train, rail = graph_info[num]
        for idx in range(len(train)):
            r,c = train[idx]
            temp[r][c] = idx+1
    return temp



'''process'''
Graph_info = get_graph_info()
Total_score = 0
print_graph(Graph_info)
for R in range(k):
    score = "NaN"
    #이동
    for num_group in range(m):
        train,rail = Graph_info[num_group]
        train = move_train(train,rail)
        Graph_info[num_group] = train,rail #여기서만 바뀜


    #선물 경로
    gift_lst = get_gift_lst(R)

    #선물 이동
    num_group, score = get_receiver(gift_lst)

    if num_group != "NaN" :
        Total_score += score

        #이동 경로 변경
        train,rail = Graph_info[num_group]
        train.reverse()
        Graph_info[num_group] = train,rail
    else :
        pass





print(Total_score)






