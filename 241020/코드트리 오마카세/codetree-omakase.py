from collections import defaultdict
L, Q = map(int, input().split())

def update_eattime(name):
    p_t, p_x = people_time[name]
    for i, s in enumerate(sushi[name]):
        if name not in people:
            continue
        s_t = s[0] # 스시가 처음 도착한 시간
        s_x = s[1]
        
        if s_t < p_t:
            curr_pos = ((p_t - s_t) + s_x ) % L
            eat_time = (p_t + (p_x - curr_pos+L) % L) # 스시가 먹히는 시간
        else:
            eat_time = (p_x - s_x + L) % L + s_t
        sushi[name][i] = [s_t, s_x, eat_time]
    
def eat_sushi(t):
    n_sushi = 0
    n_people = 0
    
    for name, s_list in sushi.items():
        eaten_sushi = 0
        p_t, p_x = people_time[name]
        # if p_t > t: # 그 사람이 오기전인 경우 -> 아무것도 안먹힌 상태
        #     n_sushi += sum([1 for s in s_list if s[0] <= t])
        # 그 사람이 온 상태
        n_eat = people[name]
        for s in s_list:
            if s[0] > t: # 스시가 생기기 전
                continue
            if s[-1] > t: # 스시가 먹히기 전
                n_sushi += 1
                continue
            if p_t <= t:
                n_eat -= 1
        if p_t <= t and n_eat > 0:
            n_people += 1

    return n_people, n_sushi
            
                
class Query:
    def __init__(self, cmd, t, x=-1, name=None, n=None):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n
              
    
names = []
people_in = dict()
people_out = dict()
people_pos = dict()
Queries = []
sushi_queries = dict()

for _ in range(Q):
    line = input().split()
    cmd = int(line[0])
    if cmd == 100:
        t, x, name = line[1:]
        t, x = int(t), int(x)
        q = Query(cmd, t, x, name)
        Queries.append(q)
        if name not in sushi_queries:
            sushi_queries[name] = []
        sushi_queries[name].append(q)
        
        
    elif cmd == 200:
        t, x, name, n = line[1:]
        t, x, n = int(t), int(x), int(n)
        Queries.append(Query(cmd, t, x, name, n))
        names.append(name)
        people_pos[name] = x
        people_in[name] = t
        
    elif cmd == 300:
        t = int(line[1])
        Queries.append(Query(cmd, t))

for name in names: # 각자 떠나는 시간 구하기
    people_out[name] = 0
    for q in sushi_queries[name]:
        p_t = people_in[name]
        p_x = people_pos[name]
        
        s_t = q.t
        s_x = q.x
        if s_t < p_t:
            curr_pos = ((p_t - s_t) + s_x ) % L
            eat_time = (p_t + (p_x - curr_pos+L) % L) # 스시가 먹히는 시간
        else:
            eat_time = (p_x - s_x + L) % L + s_t
        
        people_out[name] = max(people_out[name], eat_time)
        Queries.append(Query(111, eat_time, name=name))

for name in names:
    Queries.append(Query(222, people_out[name], name=name))
    
total_sushi = 0
total_people = 0
Queries.sort(key=lambda x:(x.t, x.cmd))
for q in Queries:
    if q.cmd == 100:
        total_sushi+= 1
    elif q.cmd == 200:
        total_people += 1
    elif q.cmd == 111:
        total_sushi -= 1
    elif q.cmd == 222:
        total_people -= 1
    else:
        print(total_people, total_sushi)