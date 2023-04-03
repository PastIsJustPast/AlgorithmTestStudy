import sys
sys.stdin=open('input.txt')
input=sys.stdin.readline

### 1. 입력 받기 ###
graph = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
# m: 몬스터의 마리 수, t : 턴의 수
m,t=map(int, input().split())
# 팩맨의 위치
px,py=map(int, input().split())
px-=1
py-=1

for _ in range(m):
    a,b,d=map(int, input().split())
    graph[a-1][b-1][d-1]+=1

dead=[[[0]*3 for _ in range(4)] for _ in range(4) ]
# 순서대로 방향 정의(45도로 반시계방향)
dx,dy=[-1,-1,0,1,1,1,0,-1],[0,-1,-1,-1,0,1,1,1]
# 팩맨의 이동 방향 (상좌우하)
dxx,dyy=[-1,0,1,0],[0,-1,0,1]

# 해설에서 항상 쓰는 방식인데, 이 함수를 사용하는게 편할 것 같음
def in_range(x,y):
    return 0<=x and x<4 and 0<=y and y<4

def can_go(x,y):
    return in_range(x,y) and dead[x][y][0]==0 and dead[x][y][1]==0 and (x,y)!=(px,py)


#### 2. 함수 정의 ####
# 알 생성 함수. 
def egg_creating():
    eggs = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(8):
                if graph[i][j][k]!=0:
                    eggs[i][j][k]+=graph[i][j][k]
    return eggs

def move_monster():
    mid_store=[] # 순서가 꼬이지 않도록 mid_store를 만들어서 이동할 장소를 저장해줌.
    for i in range(4): #x좌표
        for j in range(4): #y좌표
            for k in range(8): #방향
                log=0
                if graph[i][j][k]==0:
                    continue
                for l in range(8): # 방향+45도 이동
                    direction=(k+l+8)%8
                    nx,ny=i+dx[direction],j+dy[direction]
                    if can_go(nx,ny):
                        mid_store.append((nx,ny,direction,graph[i][j][k]))
                        graph[i][j][k]=0
                        break
    for x,y,d,z in mid_store:
        graph[x][y][d]+=z
    

#해설 참고 - packman이 움직이고 dead가 갱신되는 부분이 안풀려서 답지를 참고함
def get_killed_num(dir1,dir2,dir3):
    x,y=px,py
    killed_num=0
    v_pos=[]
    for dir in [dir1,dir2,dir3]:
        nx,ny=x+dxx[dir],y+dyy[dir]
        if not in_range(nx,ny):
            return -1
        if not (nx,ny) in v_pos:
            killed_num+=sum(graph[nx][ny])
            v_pos.append((nx,ny))
        x,y=nx,ny
    return killed_num

def do_kill(best_route):
    global px,py
    dir1,dir2,dir3=best_route

    for move_dir in [dir1,dir2,dir3]:
        nx,ny=px+dxx[move_dir],py+dyy[move_dir]
        for i in range(8):
            dead[nx][ny][2] +=graph[nx][ny][i]
            graph[nx][ny][i]=0
        px,py=nx,ny               


def move_p():
    max_cnt=-1
    best_route=(-1,-1,-1)

    for i in range(4):
        for j in range(4):
            for k in range(4):
                m_cnt=get_killed_num(i,j,k)
                if m_cnt>max_cnt:
                    max_cnt=m_cnt
                    best_route=(i,j,k)
    do_kill(best_route)

def decay_m():
    for i in range(4):
        for j in range(4):
            for k in range(2):
                # 그 전의 값으로 치환시키는 것!
                dead[i][j][k]=dead[i][j][k+1]
            dead[i][j][2]=0

def monster_creating(eggs):
    for i in range(4):
        for j in range(4):
            for k in range(8):
                graph[i][j][k]+=eggs[i][j][k]

#틀린것 체크위한 함수
def test():
    for i in range(4):
        for j in range(4):
            for k in range(8):
                if graph[i][j][k]>0:
                    print(i,j,k)
    print()


### 3. 메인함수 ###
for _ in range(t):
    eggs=egg_creating()
    move_monster()
    move_p()
    decay_m()
    monster_creating(eggs)
cnt=0
for i in range(4):
    for j in range(4):
        for k in range(8):
            cnt+=graph[i][j][k]
print(cnt)
