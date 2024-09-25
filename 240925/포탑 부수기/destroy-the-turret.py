from collections import deque 

N, M, K = map(int, input().split())
grid = []
dirs = [(0, 1), (1,0), (0, -1), (-1,0)]
neighbors = [(-1,-1), (-1, 0), (-1,1), (0, -1), (0, 1), (1,-1), (1, 0), (1,1)]
state = dict()
towers = []
powers = dict()
history = dict()
positions = dict()

def bfs(start_node, end_node):
    ti, tj = positions[end_node]
    queue = deque()
    visited = [False] * ((N*M) + 1)
    queue.append((start_node, 0, []))
    visited[start_node] = True
    while queue:
        node, dist, paths = queue.popleft()
        ni, nj = positions[node]
        if (ni, nj) == (ti, tj):
            return dist, paths
        for d in dirs:
            di, dj = (ni + d[0]) % N, (nj + d[1]) % M
            if 0 <= di < N and 0 <= dj < M and grid[di][dj] > 0:
                next_node = grid[di][dj]
                if powers[next_node] > 0 and not visited[next_node]:
                    visited[next_node] = True
                    new_paths = paths + [next_node]
                    queue.append((next_node, dist+1, new_paths))
    return -1, None

n = 0
for i in range(N):
    inputline = list(map(int, input().split()))
    row = []
    for j in range(M):
        n+= 1
        history[n] = 0
        
        positions[n] = (i,j)
        if inputline[j] == 0:
            state[n] = -1
            row.append(-1)
            continue
        powers[n] = inputline[j]
        row.append(n)
        state[n] =  0 
        towers.append((i, j, inputline[j], 0, n))
    grid.append(row)

for k in range(1, K+1):
    towers = sorted(towers, key=lambda item: (-item[2], item[3], item[0]+item[1], item[1]), reverse=True )
    # print("powers: ", powers)
    # print("positions: ", positions)
    # print("towers : ", towers)
    attacker = towers[0][-1]
    defenser = towers[-1][-1]
    # print("attacker: ", attacker)
    # print("defenser: ", defenser)
    
    powers[attacker] += N+M
    damage = powers[attacker]
    # powers[defenser] = max(powers[defenser] - powers[attacker], 0)

    d, paths = bfs(attacker, defenser)
    # print(d, paths)
    if d != -1 and paths is not None: # 포탄 공격
        for node in paths:
            state[node] = 2
            # powers[node] = max(powers[defenser] - powers[attacker] // 2, 0)
    else:
        i, j = positions[defenser]
        for ns in neighbors:
            ni, nj = (i + ns[0]) % N, (j + ns[1]) % M
            n_node = grid[ni][nj]
            if n_node != -1:
                state[n_node] = 2
            # powers[n_node] = max(powers[n_node] - powers[attacker] // 2, 0)
    state[attacker] = 1
    state[defenser] = 3
    history[attacker] = k
    towers = []
    for s in state:
        if state[s] == -1:
            continue
        i, j = positions[s]
        if state[s] == 0:
            powers[s] += 1
        elif state[s] == 2:
            powers[s] = max(powers[s] - damage // 2, 0)
        elif state[s] == 3:
            powers[s] = max(powers[s] - damage, 0)
        state[s] = 0 # first error
        if powers[s] <= 0:
            grid[i][j] = -1
            state[s] = -1
            del positions[s]
            del powers[s]
        else:
            towers.append((i, j, powers[s], history[s], s))
        
    # print(powers)
print(max(powers.values()))