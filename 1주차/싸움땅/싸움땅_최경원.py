import sys
input=sys.stdin.readline

#####1. 입력 받기 #####
# n: 격자의 크기, m : 플레이어 수, k:라운드 수
n,m,k=map(int, input().split())

# 총의정보 - 3차원 배열로 저장
gun=[[0]*n for _ in range(n)]
for i in range(n):
    arr=list(map(int, input().split()))
    for j in range(n):
        gun[i][j]=[arr[j]]

# 플레이어들의 정보 x,y (플레이어 위치),d(방향), s(초기 능력치)
graph=[[-1]*n for _ in range(n)]
players=[]
for i in range(m):
    x,y,d,s=map(int, input().split())
    # 마지막의 0은 총의 능력치를 저장하기 위함.
    players.append([x-1,y-1,d,s,0])
    graph[x-1][y-1]=i

# 문제에 나타난 방향 정보
dx, dy=[-1,0,1,0],[0,1,0,-1]



########2.게임시작 함수 정의 ######
result=[0]*m
def game(k):
    #k라운드 동안 진행됨
    for _ in range(k):
        # 플레이어 번호 순서대로 진행
        for i in range(m):
            a,b=0,0
            x,y,d,s,g=players[i][0],players[i][1],players[i][2],players[i][3],players[i][4]
            # 내 방향으로 이동
            nx,ny=dx[d]+x,dy[d]+y
            if 0<=nx<n and 0<=ny<n:
                a,b=nx,ny
            else:
                # 격자를 벗어나면 반대 방향으로 이동 + 방향이 바뀌었으므로 players[i][2]를 바꿔줌
                a,b=x-dx[d],-dy[d]+y
                players[i][2]=(d+2)%4

            # 플레이어가 없으면 총 획득하고 원래 있던 것 두고오기/ a,b는 새롭게 이동한 방향, x,y는 원래 장소
            if graph[a][b]==-1:
                gun[a][b].sort(reverse=True)
                if gun[a][b][0]>g:
                    mid=players[i][4]
                    players[i][4]=gun[a][b][0]
                    gun[a][b].remove(players[i][4])
                    gun[a][b].append(mid)
                # 플레이어 이동
                graph[a][b]=graph[x][y]
                graph[x][y]=-1
                players[i][0],players[i][1]=a,b

            # 플레이어가 있는 경우, 싸움.
            else:
                graph[x][y]=-1 # 결과가 어찌됐던 일단 초기자리에는 아무도 없음.
                # 누가 이기는지 정하기
                new_play=graph[a][b] #a,b위치에 있는 플레이어는 new_player
                if s+g>players[new_play][3]+players[new_play][4]:
                    win,lose=i, new_play
                elif s+g<players[new_play][3]+players[new_play][4]:
                    win,lose=new_play,i
                else:
                    # 두 플레이어의 능력치가 같은 경우, 초기능력치 비교
                    if s>players[new_play][3]:
                        win,lose=i,new_play
                    else:
                        win,lose=new_play,i

                # 이긴 사람은 능력치 차이만큼 점수 얻고 위치 선점
                result[win]+=players[win][3]+players[win][4]-players[lose][4]-players[lose][3]
                players[win][0],players[win][1]=a,b
                graph[a][b]=win

                # 진 사람은 총 내려놓고 이동 (a,b에서 이동하는 것.)
                gun[a][b].append(players[lose][4])
                players[lose][4]=0
                for k in range(4):
                    lx,ly=dx[(players[lose][2]+k)%4]+a,dy[(players[lose][2]+k)%4]+b
                    if 0<=lx<n and 0<=ly<n and graph[lx][ly]==-1:
                        if len(gun[lx][ly])==0:
                            break
                        else:
                            gun[lx][ly].sort(reverse=True)
                            players[lose][4]=gun[lx][ly][0]
                            gun[lx][ly].remove(players[lose][4])
                            if len(gun[lx][ly])==0:
                                gun[lx][ly].append(0)
                        # 여기를 고침
                        graph[lx][ly]=lose
                        players[lose][0],players[lose][1]=lx,ly
                        players[lose][2]=(players[lose][2]+k)%4
                        break
                    else:
                        continue
                
                # 이긴사람 더 좋은 총 획득하기
                gun[a][b].sort(reverse=True)
                if players[win][4]<gun[a][b][0]:
                    mid=players[win][4]
                    players[win][4]=gun[a][b][0]
                    gun[a][b].remove(players[win][4])
                    #마지막으로 고친 부분
                    gun[a][b].append(mid)

            
game(k)
for i in result:
    print(i,end=' ')
