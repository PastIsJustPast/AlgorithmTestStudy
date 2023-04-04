"""
정리 안하고 그대로 올립니닷..! git commit comment 링크(https://github.com/PastIsJustPast/AlgorithmTestStudy/commit/03b29d7147061c96d4d54efb75f7abaf12f762a4)를 참고해주세요
""'
"""
n*n 
술래 정중앙 시작 arr[n//2+1][n//2+1]
m명 도망자 상하 아래쪽 먼저 or 좌우 오른쪽 먼저
h개 나무
초기에 나무와 도망자 겹쳐 주어질 수 있음

게임
m명 도망자 먼저 동시에 움직이고
술래 움직이고
도 => 술 => 도 => 술 .. 
k번 반복

# 도망자 움직임
술래와 거리가 3이하인 도망자 만 움직임
거리 = |x1 - x2| + |y1 - y2|

격자 벗어나지 않을때
    현재 바라보는 칸으로 1칸 이동 
        움직이는 칸에 술래가 있으면 움직이지 않음
        없으면 이동 나무가 있어도 이동
격자 벗어날때
    현재 방향과 반대로 틀어주기
    현재 바라보는 칸으로 1칸 이동 
        움직이는 칸에 술래가 있으면 움직이지 않음 ? 
        없으면 이동 나무가 있어도 이동

# 술래 움직임
1. 이동
달팽이 모양으로 움직임 시계방향 상 우 하 좌
끝(arr[0][0])에 도달하면 다시 반시계
2. 방향 업데이트
이동한 위치에서의 방향 속성을 업데이트 해주어야함
3. 잡기
현재 위치에서 현재 방향의 3칸 내의 술래를 잡음 
잡은 도망자의 수 = 점수
나무에 가려진 도망자는 안보여서 못잡음
"""
"""
입력 
n 격자 ,m 도망자수,h 나무수,k 턴횟수 n은 반드시 홀수
m개 줄에 걸친 x,y 도망자 위치, dir 방향 1 = 좌우 2 = 상하
h개 줄에 걸친 x,y 나무 위치
"""
"""
[전략]
술래 속성 Player: 위치, 방향 (도망자를 잡는 방향, 다음 이동방향)
도망자 속성 Runner: 위치, 방향 (다음 이동 방향)
나무 속성 Tree: 위치

[기능]
공통 기능
    움직이려는 위치가 격자 범위 내 있는지 판단 기능

도망자 움직임 기능
    - 술래와 거리 파악 기능
    - 움직이려는 위치가 격자 범위 내 있는지 판단 기능 (공통)
    - 움직이려는 칸에 술래 있는지 파악 기능 
    - 1칸 이동 기능 

술래 움직임 기능
    - 초기화
        방향에 대한 move_arr => player_arr
        시계 방향일때 상 우 하 좌로 방향 설정
        arr[0][0] 위치라면 반시계 하 우 상 좌로 방향 설정
    - 이동 기능
        방향대로 한칸 이동
    - 방향 업데이트 기능
        시계 방향일때 상 우 하 좌 순서에 따라 다음 단계로 업데이트
        방문한 칸이라면 기존 방향 유지
    - 잡기 기능

# arr 의 하나의 칸 구성
arr[][][0] - 성질 : 'none', 'player'.. 
arr[][][1] - 방향 : player, runner 은 [1]에 방향 

player_arr[][] = False # visited 의 여부만 확인
runner_arr[][] = -1 # runner_dic의 인덱스만 확인 # 위치에 있으면 인덱스 넣어주기
runner_dic = {인덱스: 방향, 0:3}

# 방향
dx dy
cw_dir 
ccw_dir

# memo
player이던 runner 이던 방향은 시계 반시계 상하좌우 같으니까
dx dy dir 로 표현해야겠다
# 아니 근데 player,runner가 tree랑 같이 있을 수 있넹 => tree_arr 따로 => tree check할때만 호출하고 초기 정보에서 수정 삭제되지 않으니깡
# runner가 동시에 같은 칸에 들어가면 어떻게하징? 돌아다니다가 그럴수도있자나 => player_arr, runner_arr, tree_arr 다 따로 해야겠넹..? =>겹치는 부분 없다고 하니까 일단 고..
# tree_arr는 없어도 될지도? ,,
"""    
# NONE, PLAYER, RUNNER, TREE = 'none','player', 'runner', 'tree' 
n,m,h,k = map(int,input().split())
# 상0 / 하1/ 좌2 / 우3
dx = [-1,1,0,0]
dy = [0,0,-1,1]
cw_dir = [0,3,1,2] # 상우하좌
turn = 1

# arr 출력 : 디버깅을 위한 함수
def arr_print():
    print("runner_arr")
    for i in runner_arr:
        print(i)

    print("player_arr")
    for i in player_arr:
        print(i)

    # print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

# 초기화
player_arr = [[ False for _ in range(n)] for _ in range(n)]
runner_arr = [[[] for _ in range(n)] for _ in range(n)]
runner_next_arr = [ [[] for _ in range(n)] for _ in range(n)]
runner_dic = {}
tree_arr = [[0 for _ in range(n)] for _ in range(n)]

# 술래 정보 초기화 
player_x = player_y = n//2 +1 -1
player_arr[player_x][player_x] = True
player_step_arr = []
player_dir = 0
player_isCW =  True
player_catch_count = 0

for i in range(m): # 도망자 정보 초기화 
    runner_x,runner_y,runner_dir  = map(int,input().split())
    runner_arr[runner_x-1][runner_y-1].append(i) # 인덱스 넣어주기
    if runner_dir == 1: # 좌우 => 우 먼저
        runner_dic[i] = 3
    else: # 상하 => 하 먼저
        runner_dic[i] = 1

for _ in range(h): # 나무 정보 초기화
    tree_x, tree_y = map(int,input().split())
    tree_x -= 1
    tree_y -= 1
    tree_arr[tree_x][tree_y] = 1 

def in_range(x,y): # 격자 내 확인
    return 0 <= x < n and 0 <= y < n

############ 도망자 기능 ##########
def runner_check_distance(rx,ry): # player와 거리 확인
    return abs(rx - player_x) + abs(ry - player_y) <= 3

def runner_next_pos_isPlayer(x,y): # 움직이려고하는 곳에 술래가 있나 확인
    return player_x == x and player_y == y
def runner_one_move(x,y,one_runner_idx,one_runner_dir):
    nx, ny = x + dx[one_runner_dir], y + dy[one_runner_dir]
    # Step 1.
    # 만약 격자를 벗어난다면
    # 우선 방향을 틀어줍니다.
    if not in_range(nx, ny):
        one_runner_dir = one_runner_dir - 1 if one_runner_dir == 1 or one_runner_dir == 3 else one_runner_dir + 1 # 하1, 우3 => 상0 좌2
        runner_dic[one_runner_idx] = one_runner_dir # 딕셔너리도 갱신  
        nx, ny = x + dx[one_runner_dir], y+ dy[one_runner_dir] 

    # Step 2.
    # 그 다음 위치에 술래가 없다면 움직여줍니다
    if not runner_next_pos_isPlayer(nx,ny): # 움직이려고하는 곳에 술래가 있나 확
        runner_next_arr[nx][ny].append(one_runner_idx)
    else: # 술래가 있으면 이동 불가
        runner_next_arr[x][y].append(one_runner_idx) # 그대로
    

def runner_move(): # 도망자 이동
    # print('*****************')
    global runner_dic, runner_next_arr, runner_arr
    for i in range(n):
        for j in range(n):
            runner_next_arr[i][j] = []
    # print(runner_arr)
      # Step 2. hider를 전부 움직여줍니다.
    for x in range(n):
        for y in range(n):
            # 술래와의 거리가 3 이내인 도망자들에 대해서만
            # 움직여줍니다.
            if runner_check_distance(x,y):
                # print(x,y,runner_arr[x][y])
                for one_runner in runner_arr[x][y]:
                    runner_one_move(x, y, one_runner, runner_dic[one_runner])
            # 그렇지 않다면 현재 위치 그대로 넣어줍니다.
            else:
                for one_runner in runner_arr[x][y]:
                    runner_next_arr[x][y].append(one_runner)

                  
    # for i in runner_next_arr:
      # print(i)
    # print("********************")
    # Step 3. next hider값을 옮겨줍니다.
    for i in range(n):
        for j in range(n):
            runner_arr[i][j] = runner_next_arr[i][j]
    return

############## 술래 기능 ###################
def player_dir_update(x,y):  # 방향 업데이트
    global player_dir, player_arr, player_isCW
    if x == y == 0: # 방향 전환 cw => ccw
        player_isCW = False
        player_arr = [[ False for _ in range(n)]for _ in range(n)] # 초기화
        # print(player_step_arr)
        temp = player_step_arr.pop()
        if temp == 0 or temp == 2:
            temp += 1
        else:
            temp -= 1
        return temp

    if x == y == n//2+1-1: # 다시 원 위치로 돌아왔을때 cw => ccw
        player_isCW = True
        player_arr = [[ False for _ in range(n)]for _ in range(n)] 
        return 0
        
    if not player_isCW: # ccw 이면 방향 업데이트 과정 필요없음 그냥 player_step_arr pop 해서 쓰면됨
        temp = player_step_arr.pop()
        if temp == 0 or temp == 2:
            temp += 1
        else:
            temp -= 1
        return temp

    temp_dir = player_dir + 1 if player_dir + 1 < 4 else 0 # 예상 경로에 가본적 있는지 확인하기
    x, y = x + dx[cw_dir[temp_dir]], y + dy[cw_dir[temp_dir]]

    if not player_arr[x][y]: ## 방문한 적없으면 
        if player_dir >= 3:
            return 0
        else:
            return player_dir + 1
    else:
        return player_dir
        

def player_catch_runner(x,y): # 잡기
    temp_dir = cw_dir[player_dir] if player_isCW else player_dir
    cnt = 0
    if temp_dir == 0 or temp_dir == 1: # 상 하
        # print("상하")
        [start_x,end_x] = [x-2,x] if temp_dir == 0 else [x, x+2]
        for i in range(start_x,end_x+1):
            # print(runner_arr[i][y],len(runner_arr[i][y]))
            if in_range(i,y) and runner_arr[i][y] and tree_arr[i][y] == 0:
                cnt += len(runner_arr[i][y])
                runner_arr[i][y] = [] #runner_arr 잡힌 도망자 업데이트


    else : 
        [start_y,end_y] = [y-2,y] if temp_dir == 2 else [y, y+2]
        for i in range(start_y,end_y+1):
            # print("좌우",player_dir,runner_arr[x][i] if in_range(x,i) else "범위 넘어감")
            if in_range(x,i) and runner_arr[x][i] and tree_arr[x][i] == 0:
                cnt += len(runner_arr[x][i])
                runner_arr[x][i] = []
    # print("~~~~~~~~~~~cnt",cnt)
    return cnt 

def player_move(): # 움직이기
    global player_dir, player_x, player_y,player_catch_count

    if player_isCW: #CW 방향이면
        # player_step_arr.append((player_x,player_y))
        player_step_arr.append(cw_dir[player_dir])
        player_x, player_y = player_x + dx[cw_dir[player_dir]], player_y + dy[cw_dir[player_dir]] # 방향대로 이동
    else:
        player_x, player_y = player_x + dx[player_dir], player_y + dy[player_dir] # 방향대로 이동

    # 방향 업데이트
    player_dir = player_dir_update(player_x,player_y)

    player_arr[player_x][player_y] = True

    # 잡기
    player_catch_count += player_catch_runner(player_x,player_y) * turn
    # print(turn,player_catch_count)

    return


  

# print(runner_dic)
# arr_print()
# print('####################')

while turn < k+1 :
    runner_move()
    player_move()
    
    # arr_print()
  
    turn += 1
    # print('####################')

print(player_catch_count)
