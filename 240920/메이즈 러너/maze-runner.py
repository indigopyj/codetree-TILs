import copy
from itertools import product
N, M, K = map(int, input().split())
grid = [[0] * (N+1) for _ in range(N+1)]
for i in range(1, N+1):
    line = map(int, input().split())
    grid[i][1:] = line

people = dict()
for i in range(1, M+1):
    x,y = map(int, input().split())
    people[i] = (x,y)

exit_x, exit_y = map(int, input().split())

def rotate(square, x1, y1, ppl):
    global exit_x, exit_y
    new_square = copy.deepcopy(square)
    n = len(square) # square
    for r in range(n):
        for c in range(n):
            new_square[c][n-1-r] = max(square[r][c]-1, 0)
    for p in ppl:
        px, py = people[p]
        px -= x1
        py -= y1
        people[p] = py+x1, n-1-px+y1
        
    exit_x -= x1
    exit_y -= y1
    exit_x, exit_y = exit_y+x1, n-1-exit_x+y1
    # print(exit_x, exit_y)
    return new_square

dirs = [(1,0), (-1,0), (0,-1), (0,1)]

def move():
    total = 0
    delete_ppl = []
    for p in people:
        px, py = people[p]
        min_dist = 999999
        min_d = (0,0)
        origin_dist = abs(exit_x - px) + abs(exit_y - py)
        for d in dirs:
            new_px, new_py = px + d[0], py + d[1]
            if new_px < 1 or new_px > N or new_py < 1 or new_py > N:
                continue
            if grid[new_px][new_py] > 0:
                continue
            dist = abs(exit_x - new_px) + abs(exit_y - new_py)
            if dist >= origin_dist:
                continue
            if min_dist > dist:
                min_dist = dist
                min_d = d
        new_px, new_py = px + min_d[0], py + min_d[1]
        total += abs(min_d[0] + min_d[1])
        people[p] = (new_px, new_py)
        if (new_px, new_py) == (exit_x, exit_y):
            delete_ppl.append(p)
    for p in delete_ppl:
        del people[p]
    # print("move: ", total)

    return total

def find_small_square():
    square_n = 20
    square_x, square_y = (20,20)
    
    for k in range(2, N+1):# size of square
        for i1 in range(1, N-k+2):
            for j1 in range(1, N-k+2):
                people_list = set()
                i2, j2 = i1+k-1, j1+k-1
                if not (i1 <= exit_x <= i2 and j1 <= exit_y <= j2):
                    continue
                flag = False
                tmp_people_list = set()
                for p, (px, py) in people.items():
                    if i1 <= px <= i2 and j1 <= py <= j2 :
                        flag = True
                        people_list.add(p)
                
                if flag:
                    return (i1, j1), (i2, j2), people_list 


total_move = 0
for t in range(K):
    total_move += move()
    if len(people) == 0:
        break
    (sq_x1, sq_y1), (sq_x2, sq_y2), ppl = find_small_square()
    sliced_sq = []
    for x in range(sq_x1, sq_x2+1):
        sliced_sq.append(grid[x][sq_y1:sq_y2+1])
    
    rotated_sq = rotate(sliced_sq, sq_x1, sq_y1, ppl)
    for i in range(sq_x2+1-sq_x1):
        grid[i+sq_x1][sq_y1:sq_y2+1] = rotated_sq[i]


    
    
print(total_move)
print(exit_x, exit_y)