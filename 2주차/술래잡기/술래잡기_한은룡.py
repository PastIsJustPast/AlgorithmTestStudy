'''
격자 안에 들어오는지는 그떄그떄 확인할 것
인풋 인자는 가급적 대문자로 통일
순환하는 값을 만들고 싶다면 r = r / 가능한 r의 값의 길이로 해라
2차원 리스트 안의 리스트는 언제나 list.remove를 동반할 수 있으니 주의할것
'''

from copy import deepcopy
N,M,H,K = map(int,input().split())

Runner_info = {} #idx로 접근하는 러너 정보 tuple or "OUT"
Runner_map = [[[] for _ in range(N)] for _ in range(N)]
for num in range(M):
    _r,_c,_d = list(map(lambda x : int(x) -1, input().split()))
    Runner_info[num] = (_r,_c,_d)
    Runner_map[_r][_c].append(num)
    
Tree_map = [[False for _ in range(N)] for _ in range(N)]
for _ in range(H):
    _r,_c = list(map(lambda x: int(x) -1,input().split()
    Tree_map[_r][_c] = True



dr = [0,1,0,-1] #우0 하1 좌2 상3
dc = [1,0,-1,0]

def next_pos_runner(r,c,d):
    cr,cc =  Catcher_pos
    #if cr == r and cc == c : raise ValueError("SameRunnerCatcher")
    #길이 초과
    if abs(r - cr) + abs(c - cc) > 3: return r,c,d
    #길이 미초과
    nr,nc = r + dr[d], c + dc[d]

    #격자 안
    if nr in range(N) and nc in range(N):
        if (nr,nc) == (cr,cc) : #술래가 있다면
            return r,c,d
        else:
            return nr,nc,d
    #격자 밖
    else:
        d = (d + 2) % 4
        nr, nc = r + dr[d], c + dc[d]
        if (nr,nc) == (cr,cc) : #술래가 있다면
            return r,c,d
        else :
            return nr,nc,d


def next_pos_catcher(round) -> tuple:
    round = round % len(Path)
    next_round = (round +1 ) % len(Path)

    pos = Path[round]
    next_pos = Path[next_round]
    direction = next_pos[0] - pos[0] , next_pos[1] - pos[1]
    return pos,direction

def get_path():
    drc = [(-1,0), (0, 1), (1, 0), (0, -1)]  # 상 우 하 좌
    min = N // 2
    r,c = mid, mid
    path =[(r,c)]
    #정방향
    for level in range(1,mid + 1):
        #상
        r,c = r + drc[0][0] , c + drc[0][1]
        path.append((r,c))
        # 우
        for _ in range(2 * level - 1):
            r,c = r + drc[1][0], c + drc[1][1]
            path.append((r,c))

        #하 좌 상
        for i in [2,3,0] :
            for _ in range(2 * level):
                r,c = r + drc[i][0], c+ drc[i][1]
                path.append((r,c))
    #역방향
    path += path[1:-1][::-1]
    return path

def catch(pos,direction, runner_info,runner_map):
    num_catch = 0
    r,c = pos
    for length in range(3):
        nr,nc = r+ length * direction[0], c+length * direction[1]
        if nr not in range(N) or nc not in range(N): break

        if runner_map[nr][nc] != [] and not Tree_map[nr][nc] : #도망자가 있고 나무가 없다면
            catched_runner = runner_map[nr][nc]
            num_catch += len(catched_runner )
            runner_map[nr][nc] = []
            for num in catched_runner:
                runner_info[num] = "OUT"
        else :
            continue
    return runner_info,runner_map,num_catch


Runner_info = deepcopy(_Runner_info)
Runner_map = deepcopy(_Runner_map)
Tree_map = deepcopy(_Tree_map)

'''process'''

Total_score = 0
mid = N // 2
Catcher_pos = (mid,mid)
Path = get_path()
for R in range(K): #라운드
    score = 0
    #도망자 이동
    for num in range(M):
        if Runner_info[num] == "OUT":
            continue
        else :
            r,c,d = Runner_info[num]
            #이동전 제거
            Runner_map[r][c].remove(num)
            #다음 위치
            r,c,d = next_pos_runner(r,c,d)
            Runner_info[num] = (r,c,d)
            Runner_map[r][c].append(num)


    #술래 이동
    Catcher_pos,Direction = next_pos_catcher(R + 1)


    #술래 체크
    Runner_info,Runner_map,num_catch = catch(Catcher_pos,Direction, Runner_info,Runner_map)
    score = (R + 1) * num_catch
    Total_score += score

    cnt = 0
    for num in range(M):
        if Runner_info[num] == "OUT":
            cnt += 1
    if cnt == M:
        break
print(Total_score)

