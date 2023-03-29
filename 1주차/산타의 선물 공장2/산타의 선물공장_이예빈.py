``````
23.03.29 
이예빈

Lined List로 구현을 하지 않았더니 시간 초과가 뜨네요.
해설을 다시 확인해보니 링크드 리스트로만 해결할 수 있는 문제라고 뒤늦게 알게 되어, LList로 도전하고 추가 업로드하겠습니다.
``````

import sys
from collections import deque
# sys.stdin=open("input.txt")
input=sys.stdin.readline


# 물건 모두 옮기기
def move_all(info: list, src, dst):
    n = len(info[src-1])
    for i in range(len(info[src-1])):
        info[dst-1].appendleft(info[src-1].pop())
    return len(info[dst-1])
    
# 앞 물건만 교체하기
def change_front(info: list, src, dst):
    src_flag=False 
    dst_flag=False
    if len(info[src-1])>0:
        src_p = info[src-1].popleft()
        src_flag=True
    if len(info[dst-1])>0:
        dst_p = info[dst-1].popleft()
        dst_flag=True 
        
    if src_flag:
        info[dst-1].appendleft(src_p)
    if dst_flag:
        info[src-1].appendleft(dst_p)
    return len(info[dst-1])
    
# 물건 나누기
def divide(info: list, src, dst):
    n = len(info[src-1])//2
    for _ in range(n):
        info[dst-1].appendleft(info[src-1].popleft())
    return len(info[dst-1])
    
# 선물 정보 얻기
def get_present_info(info: list, p_num):
    a=-1
    b=-1
    for q in info:
        for i in range(len(q)):
            if q[i]==p_num:
                if i>0:
                    a=q[i-1]
                if i<len(q)-1:
                    b=q[i+1]
                return (a+2*b)
            
# 벨트 정보 얻기
def get_belt_info(info: list, b_num):
    a=-1
    b=-1
    c=len(info[b_num-1])
    
    if c>0:
        a=info[b_num-1][0]
        b=info[b_num-1][-1]
    return a+2*b+3*c
    

if __name__=='__main__':
    q=int(input())
    
    # 공장 설립
    arr = list(map(int, input().split()))
    info = [deque([]) for _ in range(arr[1])]
    for i in range(3, len(arr)):
        info[arr[i]-1].append(i-2) # right에 append
        
    # 각 케이스
    for _ in range(q-1):
        tmp = list(map(int, input().split())) # 명령어 입력
        
        if tmp[0]==200:
            print(move_all(info, tmp[1], tmp[2]))
        elif tmp[0]==300:
            print(change_front(info, tmp[1], tmp[2]))
        elif tmp[0]==400:
            print(divide(info, tmp[1], tmp[2]))
        elif tmp[0]==500:
            print(get_present_info(info, tmp[1]))
        elif tmp[0]==600:
            print(get_belt_info(info, tmp[1]))
        