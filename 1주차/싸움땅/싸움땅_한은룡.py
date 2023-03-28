'''

#유형
- 구현

#풀이법
- 모든 라운드는 플레이어 인덱스 순서대로 움직인다. -> 모든 행위는 플에이어 인덱스를 기준으로 다룰 예정
- 이동 -> 해당 위치에 플레이어 파악 -> 없다 -> 총 확인 및 줍지
                               -> 있으면 결투 -> 승리자 승점 -> 패배자 무기 버리고 이동 -> 이동 후 총 확인 및 줍기 (이때 플레이어와 또 마주칠일 없음)


#자료 구조(?)
- 총의 위치 : 2차원 리스트 안의 리스트 (총이 한 격자 안에 여러자루 있을 수 있기 때문)
- 플레이어 정보 : dict(index : [x,y,d,s,gun : 총]
- 플레이어 위치 : 2차원 배열안의 배열 (한 격자안에 두 플레이어가 존재할 수 있기 때문)


#쟁점
- 한 격자 안에 플레이어와 총이 둘 이상씩 있을 수 있다.
- 모든 격자를 돌아가면서 플레이어를 찾고 이동할 경우 시간이 터진다.
    - 뒤늦게 알았지만 플레이어는 최대 20명이라 플레이어 정보인 dict만 관리해도 됐다.
- 이동방식이 두개다. (일반적인 경우와 패배 경우)

#어려운점
- 다루는 정보가 많아서 에러 조심

#시간복잡도?
- 탐색이 아니라 신경안써도 됨
'''


n,m,k = map(int,input().split())
where_guns = [[[x] for x in list(map(int,input().split()))  ] for _ in range(n)] # 총 위치. 2차원 배열 안의 리스트

where_players = [[[] for _ in range(n)] for _ in range(n)] #둘 이상의 플레이어가 속할 수 있으므로 2차원 배열 안의 배열
players = {}
for i in range(m):
    x,y,d,s = map(int,input().split())
    players[i] = [x-1,y-1,d,s,0] #위치,방향,능력,총
    where_players[x-1][y-1].append(i)


dx = [-1,0,1,0] #상 우 하 좌
dy = [0,1,0,-1]

score = [0 for _ in range(m)]

#이동
def normal_move(num_player,players,where_players):
    """일반적인(플레이어가 혼자 있을 때) 플레이어의 이동함수"""
    x,y,d,s,gun = players[num_player]

    nx,ny = x + dx[d], y + dy[d]
    if nx not in range(n) or ny not in range(n):
        d = (d + 2) % 4 # 반대
    nx, ny = x + dx[d], y + dy[d]

    #이동 및 갱신
    where_players[x][y] = []
    where_players[nx][ny].append(num_player)
    players[num_player] = [nx,ny,d,s,gun]
    return players,where_players


#총 비교 / 갖기/ 내려놓기
def check_and_get_guns(num_player,players, where_guns):
    x,y,d,s,gun = players[num_player]
    #체크
    if where_guns[x][y] != [0]: #어떤 총이라도 있다면
        temp_guns = [gun] + where_guns[x][y]
        max_gun = max(temp_guns)  #총은 최대 3개까지 있을 수 있음
        temp_guns.remove(max_gun)

        #갱신
        players[num_player] = x,y,d,s,max_gun
        where_guns[x][y] = temp_guns
    else: #아무 총도 없다면 그냥 간다.
        pass
    return players, where_guns


#패배자 액션
def action_loser (loser,players,where_guns,where_players):
    """무기를 버리고 이동한다."""
    x,y,d,s,gun = players[loser]
    #버리기
    if gun != 0:
        if where_guns[x][y] != [0] :
            where_players.append(gun)
        else:
            where_players[x][y] = [gun]
        gun = 0 #버림
    else:
        pass

    #다음 위치 탐색
    for _ in range(4):
        nx,ny = x + dx[d], y + dy[d]
        if nx not in range(n) or ny not in range(n) or where_players[nx][ny] != [] : #누군가 있거나 벽이라면
            d = (d + 1) % 4
        else: #아무도 없다면 (무조건 4서치 안에 끝나는가..?. 최소 바로 뒤에는 갈 수 있네)
            break
    where_players[x][y].remove(loser)
    where_players[nx][ny] = [loser]  # 아무도 없는 곳에 간다.
    players[loser] = [nx, ny, d, s, gun]

    return players,where_guns,where_players



#플레이어 싸우기 비교
def fight_and_get_score(one,two,score):
    """두 플레이어의 싸움을 승패를 결정하고 결정하고 점수를 반영한다"""
    #승패
    one_s, one_gun = players[one][3:]
    two_s, two_gun= players[two][3:]
    one_sum,two_sum = one_s + one_gun, two_s + two_gun

    if one_sum > two_sum :
        winner = one
        loser = two
    elif one_sum < two_sum :
        winner = two
        loser = one
    else :
        if one_s > two_s :
            winner = one
            loser = two
        else :
            winner = two
            loser = one

    #스코어 합산
    score[winner] += abs(one_sum - two_sum)

    return winner,loser,score


#process
def process(players,where_guns,where_players,score):
    for _ in range(k):
        for num_player in players:
            #이동
            players,where_players = normal_move(num_player, players,where_players)

            #플레이어 겹치는 것 체크
            x,y = players[num_player][:2]
            if len(where_players[x][y]) == 1 : #이동한 위치가 혼자라면
                #무기 체크
                players, where_guns =check_and_get_guns(num_player,players, where_guns)

            else: #둘 이라 싸운다면
                one,two = where_players[x][y]
                winner, loser, score = fight_and_get_score(one,two,score)

                players,where_guns,where_players = action_loser (loser,players,where_guns,where_players) #패배자는 무기버리고 이동
                players, where_guns = check_and_get_guns(winner,players, where_guns) #승리자는 무기 비교
                players, where_guns = check_and_get_guns(loser,players, where_guns) #패배자는 이동후 무기 비교

    return score

process(players,where_guns,where_players,score)

for x in score :
    print(x, end = ' ')

