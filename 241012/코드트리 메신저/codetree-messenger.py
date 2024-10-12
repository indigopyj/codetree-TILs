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
    DP[node] = max(DP[node] + value, 0)
    if state[node]:
        up_dfs(parents[node], power-1, value)

def get_all_children(node):
    # visited = [False] * (N+1)
    q = [(node, 0)]
    node_child = []
    while q:
        node, depth = q.pop(0)
        node_child.append((node, depth))
        # visited[node] = True
        # if powers[node] >= depth:
        #     count += 1
        for child in children[node]:
            if state[child]:
                q.append((child, depth+1))
    return node_child

def up_dfs_2(node, power, value, child_list):
    if node == 0:
        return
    count = 0
    for c_node, depth in child_list:
        if powers[c_node] >= power + depth:
            count += 1
    DP[node] = max(DP[node] + count * value, 0)
    if state[node]:
        up_dfs_2(parents[node], power+1, value, child_list)

def change_state(c):
    # print(DP)
    child_list = get_all_children(c)
    #print("child_list ", child_list)
    state[c] = not state[c]
    if state[c]:
        value = 1
    else:
        value = -1
    up_dfs_2(parents[c], 1, value, child_list)
    # print(DP)
    # if state[c]:
    #     up_dfs(parents[c], powers[c], count)
    # else:
    #     up_dfs(parents[c], powers[c], -count)
    

def change_power(c, power):
    up_dfs(parents[c], powers[c]-1, -1)
    powers[c] = power
    up_dfs(parents[c], powers[c]-1, 1)

def change_parents(c1, c2):
    # print("before off: ", DP)
    p1 = parents[c1]
    p2 = parents[c2]
    c1_state = state[c1]
    c2_state = state[c2]
    if state[c1]:
        # print("C1 true to false")
        change_state(c1)
    if state[c2]:
        # print("C2 true to false")
        change_state(c2)
    # up_dfs(p1, powers[c1]-1, -1)
    # up_dfs(p2, powers[c2]-1, -1)
    # print("after off: ", DP)

    child_1 = children[p1]
    child_2 = children[p2]
    child_1.remove(c1)
    child_2.remove(c2)
    child_1.append(c2)
    child_2.append(c1)
    parents[c1] = p2
    parents[c2] = p1
    if c1_state:
        change_state(c1)
    if c2_state:
        change_state(c2)
    # print("final: ", DP)
    # up_dfs(parents[c1], powers[c1]-1, 1)
    # up_dfs(parents[c2], powers[c2]-1, 1)
    # print(DP)
    

N, Q = map(int, input().split())
children = [[] for _ in range(N+1)]
state = [True] * (N+1)
DP = [0] * (N+1)
for _ in range(Q):
    line = list(map(int, input().split()))
    # print(line)
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
        
    elif cmd == 400:
        c1, c2 = line[1:]
        change_parents(c1, c2)
        # print(parents, children)
    elif cmd == 500:
        c = line[1]
        print(DP[c])
    # print(DP)