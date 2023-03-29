import sys
from collections import deque
input=sys.stdin.readline

#### 1. 입력 ####
# n: 격자의 크기, m : 사람의 수
n,m=map(int, input().split())
# 0의 경우 빈 공간, 1의 경우 베이스캠프
base=[]
graph=[]
for i in range(n):
    graph.append(list(map(int, input().split())))
    for j in range(n):
        if graph[i][j]==1:
            base.append((i,j))

# 사람들이 가고자하는 편의점 위치
store=[]
for _ in range(m):
    a,b=map(int, input().split())
    store.append((a-1,b-1))
people=[[-1,-1] for _ in range(m)] # 사람들의 현재 상태. 만약 도착했어도 -1로 해줄것임 !


#### 2. 함수 정의 ####
dx,dy=[-1,0,0,1],[0,-1,1,0] # 우선 순위대로 정의
def bfs(ax,ay,visited): 
    q=deque()
    q.append((ax,ay))
    visited[ax][ay]=1
    while q:
        x,y=q.popleft()
        for i in range(4):
            nx,ny=dx[i]+x, dy[i]+y
            if 0<=nx<n and 0<=ny<n and visited[nx][ny]==0 and not graph[nx][ny]==-1:
                visited[nx][ny]=visited[x][y]+1
                q.append((nx,ny))

#### 3. 메인함수 시작 ####
time=0
num=0
while 1:
    time+=1
    # 1) 가고싶은 편의점을 향해 1칸 이동. -> 편의점을 기준으로 bfs
    for i in range(m):
        if people[i][0]==-1 and people[i][1]==-1:
            continue
        x,y=store[i][0],store[i][1]
        visited=[[0]*n for _ in range(n)]
        bfs(x,y,visited)
        min_val=100000
        for j in range(4):
            nx,ny=people[i][0]+dx[j],people[i][1]+dy[j]
            if 0<=nx<n and 0<=ny<n and graph[nx][ny]==0:
                # 여기서 visited를 0 이상으로 해주어야 함. !!! 왜냐면 갈 수 없는 경우 모두 0으로 표시되므로
                if 0<visited[nx][ny]<min_val:
                    min_val=visited[nx][ny]
                    c,d=nx,ny
        people[i][0],people[i][1]=c,d

    # 2) 해당 편의점에 도착하면 멈춤
    for i in range(m):
        if people[i][0]==-1 and people[i][1]==-1:
            continue
        if people[i][0]==store[i][0] and people[i][1]==store[i][1]:
            # 이 부분에서 people -1,-1을 먼저 선언해줘서 무한루프 걸렸었음..
            graph[people[i][0]][people[i][1]]=-1
            people[i][0],people[i][1]=-1,-1
    # store에서 가까운 베이스캠프 지정해주기
    if time<=m:
        base_camp=[]
        min_val=10000001
        visited=[[0]*n for _ in range(n)]
        bfs(store[num][0],store[num][1],visited)
        for x,y in base:
            if 0<visited[x][y]<min_val:
                min_val=visited[x][y]
                base_camp=[x,y]
        people[num][0],people[num][1]=base_camp[0],base_camp[1]
        graph[base_camp[0]][base_camp[1]]=-1
        num+=1
    # 끝나는 조건 명시
    ans=0
    if time>m:
        for x,y in people:
            if x==-1 and y==-1:
                ans+=1
    if ans==m:
        break
print(time)
