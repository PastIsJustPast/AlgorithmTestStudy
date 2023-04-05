from copy import deepcopy
from collections import deque

N  = int(input())
#Graph = [list(map(int,input().split())) for _ in range(n)]
_Graph = []
for info in input().split('\n'):
    _Graph.append(list(map(int,info.split())))


dr = [0,0,1,-1]
dc = [1,-1,0,0]

def print_graph(group_info):
    temp = [[False for _ in range(N)] for _ in range(N)]
    for num, tpl in group_info.items():
        for r,c in tpl[1] :
            temp[r][c] = num

    return temp

#bfs
def get_group_info():
    visited =[[False for _ in range(N)] for _ in range(N)]
    group_info = dict()
    idx = 0
    for R in range(N):
        for C in range(N):
            if not visited[R][C]:
                num = Graph[R][C]
                lst = [(R,C)]
                visited[R][C] = True

                #인접 찾기
                q = deque()
                q.append((R,C))
                while q :
                    r,c = q.popleft()
                    for i in range(4):
                        nr,nc = r + dr[i] , c + dc[i]
                        if nr in range(N) and nc in range(N) and Graph[nr][nc] == num and not visited[nr][nc]:
                            lst.append((nr,nc))
                            q.append((nr,nc))
                            visited[nr][nc] = True
                group_info[idx] = (num,lst)
                idx += 1
    return group_info

def search_near_bex(one, two):
    """두 그륩의 인접한 변의 갯수"""
    near_count = 0
    visited = [[False for _ in range(N)] for _ in range(N)]
    one_num, one_lst = one
    two_num, two_lst = two

    r,c = one_lst[0]

    q = deque()
    q.append((r,c))
    visited[r][c] = True

    while q :
        r,c = q.popleft()
        for i in range(4):
            nr,nc = r + dr[i], c+dc[i]
            if nr in range(N) and nc in range(N) and not visited[nr][nc]:
                if Graph[nr][nc] == one_num :
                    q.append((nr,nc))
                    visited[nr][nc] = True
                elif Graph[nr][nc] == two_num and (nr,nc) in two_lst :
                    near_count += 1
                else:
                    continue
    return near_count

def get_two_group_score(one,two):
    """ 두 그룹의 점수 """
    score = 0
    one_num, one_lst = one
    two_num, two_lst = two
    near_count = search_near_bex(one,two)


    score = (len(one_lst) + len(two_lst)) * one_num * two_num * near_count
    return score

def get_score():
    """
    그륩의 총 점수를 합
    """
    total_score = 0
    for i in range(len(Group_info)):
        for j in range(len(Group_info)):
            if i >= j :
                continue

            one,two = Group_info[i],Group_info[j]
            score = get_two_group_score(one,two)
            total_score += score

    return total_score



def rotate(graph):
    temp_arr = [lst[:] for lst in graph]
    mid = N // 2
    #십자
    temp_1 = temp_arr[mid][::-1]
    temp_2 = [lst[mid]  for lst in temp_arr]

    #가로
    for i in range(N):
        temp_arr[i][mid] = temp_1[i]
    #세로
    temp_arr[mid]= temp_2

    #격자 회전
    for r_start in [0,mid+1] :
        for c_start in [0,mid+1]:
            #복사
            temp_temp_arr = [[0 for _ in range(mid)] for _ in range(mid)]
            for i in range(mid):
                for j in range(mid):
                    temp_temp_arr[i][j] = temp_arr[r_start + mid - 1 - j][c_start + i ]
            #붙여넣기
            for i in range(mid):
                for j in range(mid):
                    temp_arr[r_start + i][c_start + j ] = temp_temp_arr[i][j]

    return temp_arr


'''process'''

Graph = deepcopy(_Graph)
Total_score = 0
#first
Group_info = get_group_info()
Total_score += get_score()

for i in range(3):
    Graph = rotate(Graph)
    Group_info = get_group_info()
    score = get_score()
    Total_score += score

print(Total_score)

