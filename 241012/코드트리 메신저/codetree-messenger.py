def count_alarm(c):
    def bfs(node):
        visited = [False] * (N+1)
        q = []
        for child in children[node]:
            if state[child] and not visited[node]:
                q.append((child, 1))
        count = 0
        while q:
            node, depth = q.pop(0)
            # print(node, powers[node], depth)
            if powers[node] >= depth:
                count += 1
            for child in children[node]:
                if state[child] and not visited[node]:
                    q.append((child, depth+1))
        return count
    n_room = bfs(c)
    return n_room

def up_dfs(node, power, value):
    if node == 0 or power < 0:
        return
    DP[node] += value
    up_dfs(parents[node], power-1)

def down_bfs(node):
    visited = [False] * (N+1)
    q = [(node, 0)]
    count = 0
    while q:
        node, depth = q.pop(0)
        visited[node] = True
        if powers[node] >= depth:
            count += 1
        for child in children[node]:
            if state[child] and not visited[child]:
                q.append((child, depth+1))
    return count

def change_state(c):
    state[c] = not state[c]
    count = down_bfs(c)
    if state[c]:
        DP[parents[c]] += count
    else:
        DP[parents[c]] -= count
    

def change_power(c, power):
    powers[c] = power
    print(DP)
    up_dfs(parents[c], powers[c]-1, -1)
    print(DP)
    up_dfs(parents[c], powers[c]-1, 1)


N, Q = map(int, input().split())
children = [[] for _ in range(N+1)]
state = [True] * (N+1)
DP = [0] * (N+1)
for _ in range(Q):
    line = list(map(int, input().split()))
    cmd = line[0]
    if cmd == 100:
        parents = [-1] + line[1:1+N]
        powers = [-1] + line[1+N:]
        for i in range(1, N+1):
            children[parents[i]].append(i)
        for i in range(1, N+1):
            up_dfs(parents[i], powers[i]-1, 1)

    elif cmd == 200:
        c = line[1]
        change_state(c)

    elif cmd == 300:
        c, power = line[1:]
        change_power(c, power)
        break
        
    elif cmd == 400:
        c1, c2 = line[1:]
        p1 = parents[c1]
        p2 = parents[c2]
        child_1 = children[p1]
        child_2 = children[p2]
        child_1.remove(c1)
        child_2.remove(c2)
        child_1.append(c2)
        child_2.append(c1)
        parents[c1] = p2
        parents[c2] = p1
        # print(parents, children)
    elif cmd == 500:
        c = line[1]
        print(count_alarm(c))