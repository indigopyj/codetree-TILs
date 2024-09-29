from collections import deque
dirs = [(-1,0), (0,-1), (0,1), (1,0)]

n, m = map(int, input().split())
grid = []
stores = dict()
base_camps = []
people = dict()
for i in range(n):
    inputline = list(map(int, input().split()))
    grid.append(inputline)
    for j in range(n):
        if inputline[j] == 1:
            base_camps.append((i,j))
        

for i in range(1, m+1):
    x,y = tuple(map(int, input().split()))
    stores[i] = (x-1, y-1)
    people[i] = (-1, -1)
    #grid[pos[0]][pos[1]] = i*100

def move_shortest(p_x, p_y, t_x, t_y):
    q = deque()
    visited = [[False] * n for _ in range(n)]
    q.append((p_x, p_y, []))
    visited[p_x][p_y] = True
    while q:
        x, y, d_list = q.popleft()
        if (x,y) == (t_x, t_y):
            break
        for i, d in enumerate(dirs):
            dx, dy = x + d[0], y + d[1]
            if 0 <= dx < n and 0 <= dy < n and grid[dx][dy] != -1 and not visited[dx][dy]:
                visited[dx][dy] = True
                q.append((dx, dy, d_list+[i]))
    # print(d_list)
    # print()
    final_dir = dirs[d_list[0]]
    nx, ny = p_x + final_dir[0], p_y + final_dir[1]
    return nx, ny, len(d_list)


def move(people):
    end_stores = []
    new_people = []

    for p_id, (p_x, p_y) in people.items():
        if (p_x, p_y) == (-1, -1):
            continue
        # print("move")
        tx, ty = stores[p_id]
        nx, ny, _ = move_shortest(p_x, p_y, tx, ty)
        # print(f"move {p_id} people {p_x}, {p_y} to {nx}, {ny} for {tx}, {ty}")
        new_people.append((p_id, nx, ny))
        if (nx, ny) == (tx, ty):
            end_stores.append((p_id, nx, ny))
    for item in new_people:
        p_id, nx, ny = item
        people[p_id] = (nx, ny)
    return end_stores 

def move_to_base(store):
    sx, sy = store
    min_dist = 99999999999
    tx, ty = 20, 20
    # for r in grid:
    #     print(r)
    # print()
    for cx, cy in base_camps:
        _, _, dist = move_shortest(sx, sy, cx, cy)
        # print("base info", cx, cy, dist)
        if min_dist >= dist:
            if min_dist == dist:
                if tx == cx:
                    if ty <= cy:
                        continue
                elif tx < cx:
                    continue
            tx, ty, min_dist = cx, cy, dist
    
    # print("move base ", tx, ty, sx, sy)
    return tx, ty


t = 0

done = 0
# print("stores: ", stores)
# print("people: ", people)
while done < m:
    t += 1
    store_pos = move(people)
    for s_id, x,y in store_pos:
        grid[x][y] = -1
        people[s_id] = (-1, -1)
        done += 1
    if t <= m:
        # print("time ", t)
        bx, by = move_to_base(stores[t])
        people[t] = (bx, by)
        base_camps.remove((bx, by))
        grid[bx][by] = -1

    
    
print(t)