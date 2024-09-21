import heapq

dirs = [(-1,0), (1,0), (0,-1), (0,1)]
total_score = 0
scores = {}
dists = {}
rabbits = []

    
def move_rabbit(pid, row, col, N, M):
    d = dists[pid]
    positions = []
    # 상
    new_pos = row - d
    if new_pos < 0:
        q, r = divmod(-new_pos, N-1)
        if q % 2 == 0:
            x = r
        else:
            x = N - 1 - r
    else:
        x = new_pos
    y = col
    #print(x,y)
    heapq.heappush(positions, (-(x+y), -x, -y))
    # 하
    new_pos = row + d
    if new_pos > N-1:
        q, r = divmod(new_pos - N+1, N-1)
        if q % 2 == 0:
            x = N-1 - r
        else:
            x = r
    else:
        x = new_pos
    y = col
    #print(x,y)
    heapq.heappush(positions, (-(x+y), -x, -y))
    # 좌
    new_pos = col - d
    if new_pos < 0:
        q, r = divmod(-new_pos, M-1)
        if q % 2 == 0:
            y = r
        else:
            y = M - 1 - r
    else:
        y = new_pos
    x = row
    #print(x,y)
    heapq.heappush(positions, (-(x+y), -x, -y))
    # 하
    new_pos = col + d
    if new_pos > M-1:
        q, r = divmod(new_pos - M+1, M-1)
        if q % 2 == 0:
            y = M-1 - r
        else:
            y = r
    else:
        y = new_pos
    x = row
    #print(x,y)
    heapq.heappush(positions, (-(x+y), -x, -y))

    _, x, y = heapq.heappop(positions)
    return (-x, -y)



Q = int(input())

def race(K, S, N, M):
    global total_score, rabbits
    chosen_rabbit = []
    for k in range(K):
        n_jump, sum_rc, row, col, pid  = heapq.heappop(rabbits)
        chosen_rabbit.append((sum_rc, row, col, pid))
        #print("choose ", r_id)
        new_row, new_col = move_rabbit(pid, row, col, N, M)
        score = new_row + 1 + new_col + 1
        n_jump += 1
        
        scores[pid] -= score
        total_score += score
        heapq.heappush(rabbits, (n_jump, new_row+new_col, new_row, new_col, pid))
    
    chosen_rabbit.sort(reverse=True)

    best_rabbit = chosen_rabbit[0][-1] 
    scores[best_rabbit] += S
    
    return

for _ in range(Q):
    inputline = list(map(int, input().split()))
    if inputline[0] == 100:
        N, M, P = inputline[1:4]
        pids = inputline[4::2]
        ds = inputline[5::2]
        # (현재까지의 총 점프 횟수가 적은 토끼, 현재 서있는 행 번호 + 열 번호가 작은 토끼, 행 번호가 작은 토끼, 열 번호가 작은 토끼, 고유번호가 작은 토끼)
        for p in range(P):
            # rabbit_dict[pids[p]] = Rabbit(pids[p], ds[p])
            dists[pids[p]] = ds[p]
            scores[pids[p]] = 0
            heapq.heappush(rabbits, (0, 0+0, 0, 0, pids[p]))

    elif inputline[0] == 200: # race
        K, S = inputline[1:]
        race(K, S, N, M)
    elif inputline[0] == 300: # change d
        pid_t, L = inputline[1:]
        dists[pid_t] *= L

    elif inputline[0] == 400: # choose best rabbit
        max_score = max(scores.values())
        max_score += total_score
        print(max_score)