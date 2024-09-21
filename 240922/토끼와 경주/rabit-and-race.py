import heapq 
from collections import defaultdict

q = int(input())

MAX_P = 2000

n, m, p = -1,-1, -1

# id에 해당하는 이동거리 저장 
r_dist = {}
# id에 해당하는 index에 점수 저장 -> max score 구할 때 max(scores)로 구하기 위함 
scores = [0] * (MAX_P+1)

# 가장 우선 순위 높은 토끼 구할 때 사용할 힙 배열 
r_heap = []
# id에 해당하는 index 저장
r_index = {}
# index에 해당하는 id 저장 
r_id = {}

def build(data):
    global n,m,p
    
    n = data[1]
    m = data[2]
    p = data[3]
    
    data = data[4:]
    
    for i in range(p):
        id = data[i*2]
        d = data[i*2+1]
        
        # id 별 이동 거리 저장 
        r_dist[id] = d 
        # id 별 index 저장 
        r_index[id] = i
        # index 별 id 저장 
        r_id[i] = id 
        # 우선순위 조건에 따라 heap에 삽입 
        # 총 점프 횟수, 행+열, 행, 열, 고유번호
        heapq.heappush(r_heap, (0,0,0,0,id))
        
def get_point(r_id, r_score):
    index = r_index[r_id]
    # 이동한 토끼 제외한 토끼들 r+c 만큼 점수 더하기 
    for i in range(p):
        if i != index :
            scores[i] += r_score

def get_top_point(r_id,s):
    # 이동한 토끼 s 만큼 점수 더하기 
    index = r_index[r_id]
    scores[index] += s 
    
dx = [-1,1,0,0]
dy = [0,0,1,-1]

def run(data):
    global n,m 
    k = data[1]
    s = data[2]
    # k번의 턴 동안 뽑혔던 적이 있던 토끼를 고를 때 사용 
    r_select_heap = []
    
    for _ in range(k):
        r_jump, r_sum, r_x, r_y, r_id = heapq.heappop(r_heap)
        
        # 상하좌우 이동 후 위치 
        positions = []
        for i in range(4):
            nx = r_x + dx[i] * r_dist[r_id]
            ny = r_y + dy[i] * r_dist[r_id]
            # 격자를 벗어났을 때 
            if nx < 0 or nx >= n or ny < 0 or ny >= m :
                nx %= 2*(n-1)
                ny %= 2*(m-1)
                nx = min(nx, 2*(n-1)-nx) 
                ny = min(ny, 2*(m-1)-ny) 
            # 행+열, 행, 열 -> 큰 순이므로 마이너스로 변환해서 삽입 
            heapq.heappush(positions, (-(nx+ny), -nx, -ny))
            
        # 우선 순위가 높은 칸으로 이동 
        r_s, x, y = heapq.heappop(positions)
        
        # 해당 칸으로 이동 
        heapq.heappush(r_heap, (r_jump+1, -r_s, -x, -y, r_id))
        # 뽑혔던 토끼 리스트에 추가 
        # 행+열, 행, 열, 고유 번호 -> 큰 순이므로 그대로 마이너스
        heapq.heappush(r_select_heap, (x+y, x, y, -r_id))
        
        # 이동한 토끼 제외한 토끼들 점수 얻기 
        get_point(r_id,-(x+y) + 2)
    
    # k번의 턴 동안 한번이라도 뽑혔던 적이 있던 토끼 중 가장 우선순위가 높은 토끼 
    r_s, x, y, r_id = heapq.heappop(r_select_heap)
    r_id = -r_id 
    # s 만큼 점수 더하기 
    get_top_point(r_id,s)
    
def change_dist(data):
    pid = data[1]
    l = data[2]

    r_dist[pid] *= l

def top_score():
    print(max(scores))
    
for _ in range(q):
    data = list(map(int,input().split()))
    
    q_type = data[0]
    
    if q_type == 100 :
        build(data)
    if q_type == 200 :
        run(data)
    if q_type == 300 :
        change_dist(data)
    if q_type == 400 :
        top_score()