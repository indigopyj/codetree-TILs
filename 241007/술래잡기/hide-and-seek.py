from collections import deque
n,m,h,k = map(int, input().split())

r_dirs = [(0,1), (1,0)]
runner_pos = dict()
runner_dir = dict()
runner_grid = [[[] for _ in range(n)] for _ in range(n)]
tree_pos = []
is_tree = [[False] * n for _ in range(n)]
for i in range(1,m+1):
    x,y,d = map(int, input().split())
    runner_pos[i] = (x-1,y-1)
    runner_dir[i] = r_dirs[d-1]
    runner_grid[x-1][y-1].append(i)

for _ in range(h):
    x,y = map(int, input().split())
    tree_pos.append((x-1,y-1))
    is_tree[x-1][y-1] = True

t_dirs = [(-1,0), (0,1), (1,0), (0,-1)]
tagger_path = deque()
rev_tagger_path = deque()
px,py = (n//2, n//2)
tagger_path.append((px,py, 0))
d_idx = 0
for i in range(1,n):
    #px, py = point
    for j in range(d_idx, d_idx+2):
        dx,dy = t_dirs[j % 4]
        for l in range(i):
            px += dx
            py += dy
            if l == 0:
                rev_tagger_path.appendleft((px,py,((j+1)%4))) 
            else:
                rev_tagger_path.appendleft((px,py,((j+2)%4))) 
            
            if l < i-1:
                tagger_path.append((px,py,(j%4)))
            else:
                tagger_path.append((px,py,((j+1)%4)))
            
    d_idx += 2
for i in range(n-2, 0, -1):
    tagger_path.append((i, 0, 0))
    rev_tagger_path.appendleft((i,0,2))
rev_tagger_path.appendleft((0,0,2))
tagger_path = list(tagger_path)
rev_tagger_path = list(rev_tagger_path)
# print(tagger_path)
# print(len(tagger_path))
# print(rev_tagger_path)
# print(len(rev_tagger_path))

# rev_tagger_path = [(0,0,2)]


# for x,y,d in tagger_path[:0:-1]:
#     rev_tagger_path.append((x,y,(d+2)%4))


def move_runner(tx, ty):
    
    for r_i in runner_pos:
        rx, ry = runner_pos[r_i]
        runner_grid[rx][ry].remove(r_i)
        rd = runner_dir[r_i]
        dist = abs(tx - rx) + abs(ty - ry)
        if dist > 3:
            continue
        nx, ny = rx + rd[0], ry + rd[1]
        if not (0 <= nx < n and 0 <= ny <n):
            new_rd = (rd[0] * (-1), rd[1] * (-1))
            nx, ny = rx + new_rd[0], ry + new_rd[1]
            runner_dir[r_i] = new_rd
        if (tx,ty) == (nx,ny):
            continue

        
        runner_pos[r_i] = (nx,ny)
        # print(f"{r_i} move to {nx}, {ny}")

    for i, (rx, ry) in runner_pos.items():
        runner_grid[rx][ry].append(i)
    # print(runner_pos)

def seek_runner(tx,ty,td, turn):
    # print("turn: ", turn, tx, ty)
    count = 0
    if td == 0 or td == 2:
        delta_x = t_dirs[td][0]
        delta_y = 0
    else:
        delta_x = 0
        delta_y = t_dirs[td][1]
    for i in range(3):
        sx, sy = tx + delta_x * i, ty + delta_y * i
        if 0 <= sx < n and 0 <= sy < n and not is_tree[sx][sy] and len(runner_grid[sx][sy]) > 0:
            # print(runner_grid[sx][sy])
            for r_id in runner_grid[sx][sy]:
                count += 1
                if r_id in runner_pos:
                    del runner_pos[r_id]
                if r_id in runner_dir:
                    del runner_dir[r_id]
            runner_grid[sx][sy] = []

    # print(count)
    return count * turn



tx,ty,td = (n//2, n//2,0)
result = 0
for t in range(1,k+1):
    move_runner(tx,ty)

    if (t // (n*n-1)) % 2 == 0:
        tx, ty, td= tagger_path[t % (n*n-1)]
    else:
        tx, ty, td = rev_tagger_path[t % (n*n-1)]
    
    result += seek_runner(tx,ty,td, t)

print(result)