from collections import deque

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

# 격자의 크기 n, 사람의 수 m
n, m = map(int, input().split())
# 갈 수 없는 격자 (이미 사람이 도착한 편의점 or 사람이 선택한 베캠)
prohibited = [[False for _ in range(n)] for _ in range(n)]
player = [[-1, -1] for _ in range(m)] # player 기초 위치 m으로 설정
store = []
base = []

for i in range(n):
    row = list(map(int, input().split()))

    for j in range(n):
        # 베이스캠프 list에 위치 추가
        if row[j]==1: base.append((i, j))

for _ in range(m):
    # 가게 위치 store list에 추가
    x, y = map(int, input().split())
    store.append((x-1, y-1)) # 이때 5by5 격자는 (5, 5) 로 들어오므로 -1씩 좌표를 빼줌

base.sort()

# idx번째 사람이 출발할 베이스 캠프 위치 좌표 return 
def findAndSetBaseCamp(idx):
    # 최소거리, 목표 베이스캠프 위치 초기화
    min_distance = float('inf')
    final_bx, final_by = -1, -1
    for bx, by in base:
        # 베이스캠프에 갈 수 없는 경우는 패스
        if prohibited[bx][by]: continue
        # 테크닉: 베이스캠프"에서부터" 최소거리를 찾기 시작함
        distance = bfs(bx, by, idx)
        if min_distance>distance:
            # 최소거리 갱신
            min_distance = distance
            final_bx, final_by = bx, by

    # 최소거리 베이스캠프 찾으면 해당 베이스캠프는 이미 사람이 접수했으므로 prohibited = True 처리
    prohibited[final_bx][final_by] = True

    return final_bx, final_by

# 베캠에서부터 idx번째 사람이 편의점까지 이동하는데 걸리는 최단거리
def bfs(bx, by, idx):
    visited = [[False for _ in range(n)] for _ in range(n)]
    store_x, store_y = store[idx] # idx번째 사람이 가고자 하는 편의점 위치
    queue = deque()
    queue.append((bx, by, 0))
    visited[bx][by] = True

    while queue:
        cur_x, cur_y, cur_d = queue.popleft()

        if cur_x==store_x and cur_y==store_y:
            return cur_d

        for d in range(4):
            new_x, new_y = cur_x + dx[d], cur_y + dy[d]
            if 0<=new_x<n and 0<=new_y<n and not visited[new_x][new_y] and not prohibited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y, cur_d + 1))

    # 경로가 없을 때 갈 수 없음을 inf를  return해서 표시해준다. 런타임 에러 방지
    return float('inf')

# idx번째 사람 최단거리 패스로 움직이기 시작했을때 움직인 후의 x,y좌표 리턴
def findShortestPath(idx):
    # idx번째 사람의 현 위치가 -1, -1이면 (아직 출발 안함) -1, -1 리턴
    if player[idx][0]==-1 and player[idx][1]==-1:
        return -1, -1

    # 플레이어의 현 위치 cur_x, cur_y
    cur_x, cur_y = player[idx]
    # 최단거리 초기화
    min_distance = float('inf')
    result_x, result_y = -1, -1
    for d in range(4):
        next_x, next_y = cur_x + dx[d], cur_y + dy[d]
        if not(0<=next_x<n and 0<=next_y<n) or prohibited[next_x][next_y]: continue

        local_min_distance = bfs(next_x, next_y, idx)

        if min_distance>local_min_distance:
            min_distance = local_min_distance
            result_x, result_y = next_x, next_y

    return result_x, result_y

def allPlayerArriveStore():
    for i in range(m):
        if not(player[i][0]==-1 and player[i][1]==-1): return False
    return True

time = 1
while True:
    # next moves  : t 시점의 플레이어들의 이동 상태가 담김 (x좌표, y좌표, 상태(0이면 베캠에서 출발, 1이면 이동중))
    next_moves = []
    if time<=m:
        # 1~time-1번째 사람들까지 최단거리를 찾아서 이동함
        for i in range(0, time-1):
            x, y = findShortestPath(i) # 모든 i번째 사람들이 최단거리를 향해 한 칸 이동함
            next_moves.append((x, y, 1)) 

        # time번째의 사람 출발시 어느 베이스캠프에서 시작할지 설정함
        x, y = findAndSetBaseCamp(time-1)
        next_moves.append((x, y, 0))
    else:
        # 1~m번째 사람들까지 최단거리를 찾아서 이동함
        for i in range(0, m):
            x, y = findShortestPath(i)
            next_moves.append((x, y, 1))

    for i in range(len(next_moves)):
        if next_moves[i][2]==1 and next_moves[i][0]==store[i][0] and next_moves[i][1]==store[i][1]:
            # 이동하다 편의점에 도착한 경우
            prohibited[store[i][0]][store[i][1]] = True
            player[i][0] = -1
            player[i][1] = -1
        elif next_moves[i][2]==0:
            # 이제 막 베이스캠프에서 출발한 경우
            prohibited[next_moves[i][0]][next_moves[i][1]] = True
            player[i][0] = next_moves[i][0]
            player[i][1] = next_moves[i][1]
        else:
            # 이동하고 있는데, 아직 편의점에 도착하지 못한 경우
            player[i][0] = next_moves[i][0]
            player[i][1] = next_moves[i][1]

    # print(next_moves)
    if allPlayerArriveStore(): break
    time += 1

print(time)