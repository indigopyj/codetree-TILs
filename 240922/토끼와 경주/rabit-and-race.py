import heapq

dirs = [(-1,0), (1,0), (0,-1), (0,1)]
total_score = 0
scores = []
class Rabbit():
    def __init__(self, pid, d):
        self.pid = pid
        self.d = d
        self.row = 0
        self.col = 0
        self.n_jump=0
        self.score=0
    
    def move_rabbit(self, N, M):
        d = self.d
        positions = []
        # 상
        new_pos = self.row - d
        if new_pos < 0:
            q, r = divmod(-new_pos, N-1)
            if q % 2 == 0:
                x = r
            else:
                x = N - 1 - r
        else:
            x = new_pos
        y = self.col
        #print(x,y)
        heapq.heappush(positions, (-(x+y), -x, -y))
        # 하
        new_pos = self.row + d
        if new_pos > N-1:
            q, r = divmod(new_pos - N+1, N-1)
            if q % 2 == 0:
                x = N-1 - r
            else:
                x = r
        else:
            x = new_pos
        y = self.col
        #print(x,y)
        heapq.heappush(positions, (-(x+y), -x, -y))
        # 좌
        new_pos = self.col - d
        if new_pos < 0:
            q, r = divmod(-new_pos, M-1)
            if q % 2 == 0:
                y = r
            else:
                y = M - 1 - r
        else:
            y = new_pos
        x = self.row
        #print(x,y)
        heapq.heappush(positions, (-(x+y), -x, -y))
        # 하
        new_pos = self.col + d
        if new_pos > M-1:
            q, r = divmod(new_pos - M+1, M-1)
            if q % 2 == 0:
                y = M-1 - r
            else:
                y = r
        else:
            y = new_pos
        x = self.row
        #print(x,y)
        heapq.heappush(positions, (-(x+y), -x, -y))

        _, x, y = heapq.heappop(positions)
        #print("rabbit move to ", -x, -y)
        self.n_jump += 1
        self.row, self.col = -x, -y



Q = int(input())
rabbit_dict = dict()

def race(K, S, N, M):
    global total_score
    chosen_rabbit = set()
    for k in range(K):
        first_jump = []
        for pid, rabbit in rabbit_dict.items():
            elem = (rabbit.n_jump, rabbit.row+rabbit.col, rabbit.row, rabbit.col, rabbit.pid)
            heapq.heappush(first_jump, elem)
        r_id = heapq.heappop(first_jump)[-1]
        chosen_rabbit.add(r_id)
        #print("choose ", r_id)
        rabbit_dict[r_id].move_rabbit(N, M)
        score = rabbit_dict[r_id].row + 1 + rabbit_dict[r_id].col + 1
        
        scores[r_id] -= score
        total_score += score
        #print(score)

        # for pid in rabbit_dict:
        #     if pid == r_id:
        #         #print(f"{pid} score : {rabbit_dict[pid].score}")
        #         print(f"{pid} scores  : {scores[pid]}")
        #         continue
        #     rabbit_dict[pid].score += score
        #     print(f"{pid} score : {rabbit_dict[pid].score}")
            
        #     print()
    
    rabbits = []
    for pid in list(chosen_rabbit):
        rabbit = rabbit_dict[pid]
        elem = (-rabbit.row - rabbit.col, -rabbit.row, -rabbit.col, -rabbit.pid)
        heapq.heappush(rabbits, elem)
    best_rabbit = -heapq.heappop(rabbits)[-1]
    scores[best_rabbit] += S
    #rabbit_dict[best_rabbit].score += S
    #print(f"best rabbit {best_rabbit} score {rabbit_dict[best_rabbit].score}")
    return

for _ in range(Q):
    inputline = list(map(int, input().split()))
    if inputline[0] == 100:
        N, M, P = inputline[1:4]
        pids = inputline[4::2]
        ds = inputline[5::2]
        scores = {}
        for p in range(P):
            rabbit_dict[pids[p]] = Rabbit(pids[p], ds[p])
            scores[pids[p]] = 0

    elif inputline[0] == 200: # race
        K, S = inputline[1:]
        race(K, S, N, M)
    elif inputline[0] == 300: # change d
        pid_t, L = inputline[1:]
        rabbit_dict[pid_t].d *= L

    elif inputline[0] == 400: # choose best rabbit
        max_score = max(scores.values())
        max_score += total_score
        print(max_score)
        # max_score = 0
        # for pid, rabbit in rabbit_dict.items():
        #     print(rabbit.score)
        #     max_score = max(-rabbit.score, max_score)
        # print(max_score, total_score)
        # print(max_score+total_score)