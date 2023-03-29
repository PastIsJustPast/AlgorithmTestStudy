'''
Linked List 구현

물건 나누기 에서 일정 수만큼 list 앞부분의 요소들을 가져와 그대로 붙이는 부분만 수정하면 될 것 같아요
'''

from collections import deque
import sys 
input=sys.stdin.readline 

class Node:
    def __init__(self, num):
        self.num = num
        self.prev = None
        self.next = None

# 물건 모두 옮기기
def move_all(belt, m_src, m_dst):
    while belt[m_src]:
        node = belt[m_src].pop()
        if belt[m_dst]:
            next_node = belt[m_dst][0]
            next_node.prev = node
            node.next = next_node 
        belt[m_dst].appendleft(node)
    else:
        if belt[m_dst]:
            belt[m_dst][0].prev=None 
            belt[m_dst][-1].next=None 
            
    return len(belt[m_dst])
   
''' 앞 물건만 교체하기 
- src와 dst의 첫번째 값(src_node, dst_node)을 받아온 후 (popleft)
- 각 값을 dst, src 앞에 추가하기 (appendleft)
'''
def change_front(belt, m_src, m_dst):
    if belt[m_src]:
        src_node = belt[m_src].popleft()
    else:
        src_node = None 
        
    if belt[m_dst]:
        dst_node = belt[m_dst].popleft() 
    else:
        dst_node = None 
        
    if src_node and dst_node:
        if belt[m_src]:
            next_node=belt[m_src][0]
            next_node.prev = dst_node
            dst_node.next = next_node
        if belt[m_dst]:
            next_node=belt[m_dst][0]
            next_node.prev = src_node
            dst_node.next = next_node
        belt[m_src].appendleft(dst_node)
        belt[m_dst].appendleft(src_node)      
    elif src_node:
        src_node.next=None
        belt[m_dst].appendleft(src_node)
    elif dst_node:
        dst_node.next=None 
        belt[m_src].appendleft(dst_node)
        
    if belt[m_src]:
        belt[m_src][0].prev=None
        belt[m_src][-1].next=None    
    if belt[m_dst]:
        belt[m_dst][0].prev=None
        belt[m_dst][-1].next=None 
        
    return len(belt[m_dst])

'''물건 나누기
- m_src의 길이를 2로 몫을 나눈 값만큼 src에서 dst로 옮기기
- 이때, 첫번째 인덱스부터 마지막 인덱스까지의 리스트 그대로를 옮기는 것이 관건
'''
def divide(belt, m_src, m_dst):
    length = len(belt[m_src])//2
    for _ in range(length):
        node = belt[m_src].popleft()
        if belt[m_dst]:
            next_node = belt[m_dst][0]
            next_node.prev = node
            node.next = next_node
        belt[m_dst].appendleft(node)
    else:
        if belt[m_src]:
            belt[m_src][0].prev = None
            belt[m_src][-1].next = None
        if belt[m_dst]:
            belt[m_dst][0].prev = None
            belt[m_dst][-1].next = None
        return len(belt[m_dst])
            
         
'''선물 정보 얻기
beltInfo 접근하여 p_num 노드의 앞 뒤 연결 노드 정보 접근
'''
def get_present_info(beltInfo, p_num):
    node = beltInfo[p_num]
    prev_node, next_node = node.prev, node.next
    if prev_node==None:
        prev_val=-1
    else:
        prev_val=prev_node.num
    if next_node==None:
        next_val=-1
    else:
        next_val=next_node.num
    return prev_val+2*next_val
  
# 벨트 정보 얻기
def get_belt_info(belt, b_num):
    c = len(belt[b_num])
    if not c:
        return -3
    else:
        a, b = belt[b_num][0], belt[b_num][-1]
        return a.num+b.num*2+c*3



if __name__=='__main__':
    q=int(input())
    _, n, m, *nums = map(int, input().split())
    belt = [deque() for i in range(n+1)]
    beltInfo={}
    
    # 공장 설립
    for i, num in enumerate(nums, start=1):
        node = Node(i)
        beltInfo[i]=node 
        if belt[num]:
            prev=belt[num][-1]
            prev.next=node 
            node.prev=prev 
        belt[num].append(node)
        
    # 각 명령 수행
    for _ in range(q-1):
        com, *tmp=list(map(int, input().split()))
        
        if com==200:
            print(move_all(belt, tmp[0], tmp[1]))
        elif com==300:
            print(change_front(belt, tmp[0], tmp[1]))
        elif com==400:
            print(divide(belt, tmp[0], tmp[1]))
        elif com==500:
            print(get_present_info(beltInfo, tmp[0]))
        elif com==600:
            print(get_belt_info(belt, tmp[0]))
        print(get_belts(belt))
