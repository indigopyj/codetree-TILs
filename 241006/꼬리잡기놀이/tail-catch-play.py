from collections import deque

class Team():
    def __init__(self, team_id):
        self.team_id = team_id
        self.head = (0,0)
        self.tail = (0,0)
        

n,m,k = map(int, input().split())
grid = []
dirs = [(0,1), (-1,0), (0,-1), (1,0)]
start_point = [(0,0), (n-1,0), (n-1,n-1), (0,n-1)]
visited = [[False] * n for _ in range(n)]
team_pos = [[] for _ in range(m+1)]
team_grid = [[0] * n for _ in range(n)]
tails = dict()
team_points = [0] * (m+1)


def dfs(i,j,team): 
    visited[i][j] = True
    team_pos[team].append((i,j))
    if grid[i][j] == 3:
        tails[team] = len(team_pos[team])-1
    team_grid[i][j] = team
    for dx, dy in dirs:
        nx, ny = i + dx, j + dy
        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
            if grid[nx][ny] == 0:
                continue
            if len(team_pos[team]) == 1 and grid[nx][ny] != 2:
                continue
            dfs(nx,ny,team)

            


                
        




for i in range(n):
    line = list(map(int, input().split()))
    grid.append(line)

# define team path
team_i = 1
for i in range(n):
    for j in range(n):
        if grid[i][j] == 1:
            dfs(i,j,team_i)
            team_i += 1
# print(team_pos)
# print(tails)
    
def go():
    for team_i in range(len(team_pos)):
        if len(team_pos[team_i]) == 0:
            continue
        new_head = team_pos[team_i][-1]
        new_pos = [new_head]
        for pos in team_pos[team_i][:-1]:
            new_pos.append(pos)
        team_pos[team_i] = new_pos
    
    for i, team in enumerate(team_pos):
        flag = False
        for j in range(len(team)):
            x,y = team[j]
            if not flag:
                if j == 0:
                    grid[x][y] = 1
                elif j == tails[i]:
                    grid[x][y] = 3
                    flag = True
                else:
                    grid[x][y] = 2
            else:
                grid[x][y] = 4
        
def get_ball(rnd):
    q,r = divmod(rnd, n)
    ball_dx, ball_dy = dirs[q % 4]
    start_x, start_y = start_point[q % 4]
    if q % 4 == 0:
        start_x += r
    elif q % 4 == 1:
        start_y += r
    elif q % 4 == 2:
        start_x -= r
    else:
        start_y -= r
    return (start_x, start_y), (ball_dx, ball_dy)

def throw_ball(rnd):
    (bx, by), (dx, dy) = get_ball(rnd)
    for i in range(n):
        nx, ny = bx + dx*i, by + dy*i
        if 0 < grid[nx][ny] < 4:
            team_i = team_grid[nx][ny]
            k = team_pos[team_i].index((nx,ny)) + 1
            team_points[team_i] += k**2
            change_head_tail(team_i)
            break

def change_head_tail(team_i):
    head = team_pos[team_i][0]
    tail = team_pos[team_i][tails[team_i]]
    team_pos[team_i][0] = tail
    team_pos[team_i][tails[team_i]] = head

for rnd in range(k):
    go()
    throw_ball(rnd)

print(sum(team_points))