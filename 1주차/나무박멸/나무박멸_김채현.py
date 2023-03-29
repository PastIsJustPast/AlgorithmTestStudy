``````
미완성 풀이 입니다..
다 풀지 못했습니다..!
제초제 유효기간을 언제 확인하고 없애야하는지 잘 모르겠네요..!
````````

n,m,K,c = list(map(int,input().split()))
arr = [[] for _ in range(n)]
for i in range(n):
    arr[i] = list(map(int,input().split()))
# print(arr)
killTree = 0

#전처리
# 정리
for i in range(len(arr)):
    for j in range(len(arr[i])):
        if arr[i][j] == 0:
            arr[i][j] = [arr[i][j], 'none']
        elif arr[i][j] == -1:
            arr[i][j] = [arr[i][j], 'wall']
        else:
            arr[i][j] = [arr[i][j], 'tree']


while True:
    if m == 0:
        print(killTree)
        break
    m -= 1

    # 나무 성장
    # 상하좌우 인접 개수 만큼 성장
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == -1: # 벽일 경우 패스
                continue
            # 상
            if i > 0 and arr[i][j][1] == 'tree' and arr[i-1][j][1] == 'tree': # i 가 0 보다크고 / 자기 해당 칸에 나무가 있어야하고 / 윗칸에도 나무가 있어야함 / 벽이 아니어야함
                arr[i][j][0] += 1
            # 하
            if i < n-1 and arr[i][j][1] == 'tree' and arr[i+1][j][1] =='tree':
                arr[i][j][0] +=1 
            # 좌
            if j > 0 and arr[i][j][1] == 'tree' and arr[i][j-1][1] =='tree':
                arr[i][j][0] +=1 
            # 우
            if j < n-1 and arr[i][j][1] == 'tree'and arr[i][j+1][1] =='tree':
                arr[i][j][0] +=1 
    # print(arr)

    # 나무 번식
    # print('나무번식',m)
    # for i in arr:
    #     print(i)

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j][1] == 'tree':
                # print(i,j,arr[i][j])
                count = 0 # 나무 심을 개수를 정해야함
                if i > 0 and arr[i-1][j][1] == 'none': # 상에 나무 없을때
                    count += 1
                if i < n-1 and arr[i+1][j][1] == 'none': # 하에 나무 없을때
                    count += 1
                if j > 0 and arr[i][j-1][1] == 'none': # 좌에 나무 없을때
                    count += 1
                if j < n-1 and arr[i][j+1][1] == 'none':
                    count += 1 
                if count == 0 :
                    continue
                count = arr[i][j][0] // count # 번식하여 심을 나무 수
                if i > 0 and arr[i-1][j][1] == 'none': # 상에 나무 없을때
                    arr[i-1][j][0] += count
                if i < n-1 and arr[i+1][j][1] == 'none': # 하에 나무 없을때
                    arr[i+1][j][0] += count
                if j > 0 and arr[i][j-1][1] == 'none': # 좌에 나무 없을때
                    arr[i][j-1][0] += count
                if j < n-1 and arr[i][j+1][1] == 'none':
                    arr[i][j+1][0] += count
    # print('-----------------')
    # print(arr)

    #제초제 놓을 자리 찾기
    # 정리
    killarr = [[0]*n for _ in range(n)]
    # print(killarr)

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j][0] == 0:
                arr[i][j] = [arr[i][j][0], 'none']
            elif arr[i][j][0] == -1:
                arr[i][j] = [arr[i][j][0], 'wall']
            else:
                arr[i][j] = [arr[i][j][0], 'tree']
    # print('-----------------')
    # print(arr)

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j][1] == 'tree':
                # print(i,j,arr[i][j][0], '제초제 대상')
                kill = [arr[i][j][0]]
                for k in range(1,K+1): #왼쪽 위
                    if i-k < 0 or j-k <0 or arr[i-k][j-k][1] == 'wall' or arr[i-k][j-k][1]=='none':
                        break
                    kill.append(arr[i-k][j-k][0])
                for k in range(1,K+1): #오른쪽 위
                    if i-k < 0 or j+k > n-1 or arr[i-k][j+k][1] == 'wall' or arr[i-k][j+k][1]=='none':
                        break
                    kill.append(arr[i-k][j+k][0])
                for k in range(1,K+1): #왼쪽 아래
                    if i+k > n-1 or j-k < 0 or arr[i+k][j-k][1] == 'wall' or arr[i+k][j-k][1]=='none':
                        break
                    kill.append(arr[i+k][j-k][0])
                for k in range(1,K+1): #오른쪽 아래
                    if i+k > n-1 or j+k > n-1 or arr[i+k][j+k][1] == 'wall' or arr[i+k][j+k][1]=='none':
                        break
                    kill.append(arr[i+k][j+k][0])
                killarr[i][j] = sum(kill)
                # print(i,j,arr[i][j], kill)

    # 가장 큰 제초제 제거
    maxkill = [0,0,0]
    for i in range(len(killarr)):
        for j in range(len(killarr[i])):
            if maxkill[0] < killarr[i][j]:
                maxkill = [killarr[i][j],i,j]
    # print(maxkill)
    killTree += maxkill[0]

    # for i in arr:
    #     print(i)

    # 제초제 기한 기한 다되면 0 none / 아니면 c-1
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j][1] == 'kill':
                if c-1 == 0:
                    arr[i][j] = [0,none]
                else:
                    arr[i][j] = [0,kill,arr[i][j][2]-1]



    # 제초제에 걸린 나무 제거
    i = maxkill[1]
    j = maxkill[2]
    arr[i][j] = [0,'kill',c]
    for k in range(1,K+1): #왼쪽 위
        if i-k < 0 or j-k <0 or arr[i-k][j-k][1] == 'wall':
            break
        if arr[i-k][j-k][1]=='none':
            arr[i-k][j-k] = [0,'kill',c]
            break
        arr[i-k][j-k] = [0,'kill',c]

    for k in range(1,K+1): #오른쪽 위
        if i-k < 0 or j+k > n-1 or arr[i-k][j+k][1] == 'wall':
            break
        if arr[i-k][j+k][1]=='none':
            arr[i-k][j+k] = [0,'kill',c]
            break
        arr[i-k][j+k] = [0,'kill',c]

    for k in range(1,K+1): #왼쪽 아래
        if i+k > n-1 or j-k < 0 or arr[i+k][j-k][1] == 'wall':
            break
        if arr[i+k][j-k][1]=='none':
            arr[i+k][j-k] = [0,'kill',c]
            break
        arr[i+k][j-k] = [0,'kill',c]

    for k in range(1,K+1): #오른쪽 아래
        if i+k > n-1 or j+k > n-1 or arr[i+k][j+k][1] == 'wall':
            break
        if arr[i+k][j+k][1]=='none':
            arr[i+k][j+k] = [0,'kill',c]
            break
        arr[i+k][j+k] = [0,'kill',c]

    # print('+++++++++++++++')
    # for i in arr:
    #     print(i)
