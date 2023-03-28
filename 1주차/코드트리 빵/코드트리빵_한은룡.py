'''
150ms / 36MB
#유형
-구현 및 BFS

#풀이
- 모두 이동 -> 모두 편의점 들어가는 지 체크 -> 캠프로 나올 수 있는 사람 있는지 체크 -> 정지조건 탐색


#쟁점
- 매초 * (매 인원  + 1 (캠프위치)) 만큼 bfs 실행이라 부담스러울 수 있음 -> bfs를 구현할 떄 최단거리로
- 모두 이동한 후에 편의점을 들어가는거라 위치가 겹칠 수 있음
- dist 구할 때 기본값을 -1로 둬서 최단거리 찾을 떄 자꾸 갈 수 없는 곳을 탐색하는 문제
- private / global 자료 구조 정리가 필요했음

#자료구조
- Graph : 2차원 배열 편의점/캠프에 도착할 떄마다 -1
- 캠프 위치 : 1차원 배열 / 도착할 때 마다 하나씩 없앰/ remove가 부담스럽긴 해도 그 수가 얼마 안됨
- 편의점 위치 : dict(index : tuple)

#어려운 점
- 시간 초과할까봐 무서움..
- 일부 자료를 함수마다 호출, 참조 -> 참조만한다면 Global 하게, 함수 내에서 조작을한다 private하게 구현


'''
from collections import deque


n, m = map(int, input().split())
Graph = [list(map(int, input().split())) for _ in range(n)]

Where_store = {x: tuple(map(lambda x: int(x) - 1, input().split())) for x in range(m)}

Where_camps = []  # 캠프 위치
for i in range(n):
    for j in range(n):
        if Graph[i][j] == 1:
            Where_camps.append((i, j))

# bfs 함수
dr = [-1, 0, 0, 1]  # 상 좌 우 하
dc = [0, -1, 1, 0]


def bfs(r, c):
    """
    모든 격자의 위치에서 (r,c)까지의 최단거리를 계산하고 출력하는 함수
    return: dist 2차원 격자
    """
    dist = [[-1 for _ in range(n)] for _ in range(n)]  # 거리 겸 지나온 곳
    dist[r][c] = 0
    q = deque()
    q.append((r, c))
    while q:
        r, c = q.popleft()
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if nr not in range(n) or nc not in range(n) or Graph[nr][nc] == -1 or dist[nr][nc] > -1:  # 격자 밖 / 갈 수 없는 곳 / 이미 지나온 곳
                continue
            dist[nr][nc] = dist[r][c] + 1
            q.append((nr, nc))
    return dist


# 다음 이동위치
def next_pos(num):
    """
    현재 위치와 맵의 상황, 목적지까지를 참조해 다음 위치를 반환하는 함수
    """
    if not isinstance(People[num], tuple):
        raise TypeError("NotStateOfPeople_3")

    if People[num] == Where_store[num]:
        raise ValueError("AlreadyArrive")

    r, c = People[num]  # 사람 위치
    sr, sp = Where_store[num]  # 편의점 목적지의 위치
    dist = bfs(sr, sp)  # 편의점 목적지까지의 최단거리

    min_value = 1e9
    min_pos = (r, c)  # 사람의 현재 위치
    for i in range(4):
        nr, nc = r + dr[i], c + dc[i]
        if nr not in range(n) or nc not in range(n) or Graph[nr][nc] == -1:
            continue
        else:
            if min_value > dist[nr][nc] and dist[nr][nc] != -1:  # 더 작다면 / 조건에 부합
                min_value = dist[nr][nc]
                min_pos = (nr, nc)
    return min_pos


# 베이스 캠프 위치
def find_camp(num):
    """
    현재 맵과 목적지를 참조해 최단 캠프를 찾는 함수
    """
    if Where_camps == []:
        raise ValueError("NotExistCamps")

    sr, sp = Where_store[num]  # 편의점 목적지의 위치
    dist = bfs(sr, sp)  # 편의점 목적지까지의 최단거리

    min_value = 1e9
    min_pos = (n, n)  # 여기서 에러나면 못 찾은 것
    for cr, cc in Where_camps:  # 캠프의 위치
        if min_value > dist[cr][cc] and dist[cr][cc] != -1:
            min_value = dist[cr][cc]
            min_pos = (cr, cc)
    return min_pos


'''process'''
def process():
    for t in range(100000):  # 분조심
        # 1. 이동
        for num in range(m):
            if People[num] == 'WAIT' or People[num] == 'ARRIVE':  # 아직 안 들어왔거나 이미 도착했다면
                continue
            elif isinstance(People[num], tuple):
                nr, nc = next_pos(num)  # 다음위치
                People[num] = (nr, nc)  # 이동
            else:
                raise TypeError("NotStateOfPeople_1")

        # 2. 편의첨 체크
        for num in range(m):
            if People[num] == 'WAIT' or People[num] == 'ARRIVE':
                continue
            elif isinstance(People[num], tuple) and People[num] == Where_store[num]:  # 이제 막 도착했다면
                r, c = People[num]
                Graph[r][c] = -1  # 해당 편의점은 방문 불가 처리
                People[num] = 'ARRIVE'  # 도착 처리
            elif isinstance(People[num], tuple) and People[num] != Where_store[num]:
                continue
            else:
                raise TypeError("NotStateOfPeople_2")

        # 3.새 투입
        if t < m:  # 아직 담은 사람이 있다면
            if Where_camps == []:
                raise ValueError("NotExistCamps_1")
            nr, nc = find_camp(t)
            People[t] = (nr, nc)
            Where_camps.remove((nr, nc))  # 가능한 camps
            Graph[nr][nc] = -1  # 해당 캠프도 못감

        # 4. 마무리 찾기
        flag = 0
        for state in People:
            if state == "ARRIVE":
                flag += 1
        if flag == m:
            break
    return t + 1


People = ['WAIT' for _ in range(m)]  # idx는 사람 번호 'WAIT' : 대기, 'ARRIVE' : 도착

print(process())