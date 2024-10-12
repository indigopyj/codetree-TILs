N, Q = map(int, input().split())
parents = [0] * (N+1)
powers = [0] * (N+1)
children = [[] for _ in range(N+1)]
state = [True] * (N+1)
# 어떤 노드에 대해, 현재 남은 power가 n인 노드의 개수를 기록한 리스트
# left_powers[idx][3]: idx 노드에 대해 남은 파워가 3인 노드 개수
left_powers = [[0] * 21 for _ in range(N+1)]


def update(idx):
    left_powers[idx] = [0] * 21 # 초기화?
    print("idx: ", idx)
    left_powers[idx][powers[idx]] += 1
    for child in children[idx]:
        if not state[child]:
            continue
        for i, val in enumerate(left_powers[child][1:]):
            left_powers[idx][i] += val
    if parents[idx] != 0:
        update(parents[idx])
            
def change_state(c):
    state[c] = not state[c]
    update(c)

def change_power(c, power):
    powers[c] = min(power, 20)
    update(c)

def change_parents(c1, c2):
    p1 = parents[c1]
    p2 = parents[c2]
    if p1 == p2:
        return
    
    children[p1].remove(c1)
    children[p1].append(c2)
    children[p2].remove(c2)
    children[p2].append(c1)
    
    parents[c1], parents[c2] = p2, p1
    
    update(p1)
    update(p2)  
    

for q in range(Q):
    line = list(map(int, input().split()))
    cmd = line[0]
    if cmd == 100:
        for i in range(N):
            parents[i+1] = line[i+1]
            powers[i+1] = min(line[i+1+N], 20)
        for i in range(1, N+1):
            children[parents[i]].append(i)
            power, idx = powers[i], i
            left_powers[idx][power] += 1 # idx번째 노드에 대해 남은 권한이 power인 노드 추가
            while parents[idx] != 0:
                if power == 0:
                    break
                idx = parents[idx]
                power -= 1
                left_powers[idx][power] += 1
        

    elif cmd == 200:
        c = line[1]
        change_state(c)

    elif cmd == 300:
        c, power = line[1:]
        change_power(c, power)
        
    elif cmd == 400:
        c1, c2 = line[1:]
        change_parents(c1, c2)
        # print(parents, children)
    elif cmd == 500:
        c = line[1]
        res = sum(left_powers[c]) - 1
        print(res)