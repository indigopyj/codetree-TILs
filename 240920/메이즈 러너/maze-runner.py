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
# grid[exit_x][exit_y] = -1

def rotate(square, x1, y1, ppl):
    global exit_x, exit_y
    new_square = copy.deepcopy(square)
    n = len(square) # square
    for r in range(n):
        for c in range(n):
            new_square[c][n-1-r] = max(square[r][c]-1, 0)
    # print(ppl)
    for p in ppl:
        px, py = people[p]
        #print("old px, py: ", px, py)
        px -= x1
        py -= y1
        people[p] = py+x1, n-1-px+y1
        #print("new px, py: ", people[p])
        
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
        # print(f"{px} {py} -> {new_px} {new_py}")
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
    people_list = set()
    for i in range(1, N+1):
        for j in range(1, N+1):
            for k in range(1, N-max(i,j)):
                nx = [n for n in range(i, i+k+1)]
                ny = [n for n in range(j, j+k+1)]
                coords = list(product(*[nx, ny]))
                #print(coords)
                flag = False
                tmp_people_list = set()
                #print(people)
                #print(i,j,k)
                for p, (px, py) in people.items():
                    if (px, py) in coords:
                        flag = True
                        tmp_people_list.add(p)
                flag = flag and ((exit_x, exit_y) in coords)
                if flag:
                    #print(square_x, square_y, square_n)
                    if square_n == k:
                        if square_x == i:
                            if square_y <= j:
                                continue
                        elif square_x < i:
                            continue
                    elif square_n < k:
                        continue
                    square_x = i
                    square_y = j
                    square_n = k
                    people_list = copy.deepcopy(tmp_people_list)
    # print("final: ", (square_x, square_y, square_n))
    sq_x1, sq_y1 = square_x, square_y
    sq_x2, sq_y2 = square_x + square_n, square_y + square_n
    return (sq_x1, sq_y1), (sq_x2, sq_y2), people_list

total_move = 0
for t in range(K):
    total_move += move()
    (sq_x1, sq_y1), (sq_x2, sq_y2), ppl = find_small_square()
    sliced_sq = []
    for x in range(sq_x1, sq_x2+1):
        sliced_sq.append(grid[x][sq_y1:sq_y2+1])
    
    rotated_sq = rotate(sliced_sq, sq_x1, sq_y1, ppl)
    for i in range(sq_x2+1-sq_x1):
        grid[i+sq_x1][sq_y1:sq_y2+1] = rotated_sq[i]
    # for r in grid:
    #     print(r)

    
    
print(total_move)
print(exit_x, exit_y)