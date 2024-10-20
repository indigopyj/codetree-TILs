from collections import defaultdict
class Query:
    def __init__(self, cmd, t, x=-1, name=None, n=-1):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n

L, Q = map(int, input().split())
queries = []
sushi_queries = defaultdict(list)
people_in = dict()
people_pos = dict()
people_out = dict()
names = []
for _ in range(Q):
    line = input().split()
    cmd = int(line[0])
    if cmd == 100:
        t, x = map(int, line[1:-1])
        name = line[-1]
        queries.append(Query(cmd, t, x, name))
        sushi_queries[name].append(Query(cmd, t, x, name))
    elif cmd == 200:
        t, x = map(int, line[1:3])
        name = line[3]
        n = int(line[4])
        queries.append(Query(cmd, t, x, name, n))
        people_in[name] = t
        people_pos[name] = x
        names.append(name)
    elif cmd == 300:
        t = int(line[1])
        queries.append(Query(cmd, t))

for name in names:
    people_out[name] = 0
    for q in sushi_queries[name]:
            
        p_t = people_in[name]
        p_x = people_pos[name]
        s_t = q.t
        s_x = q.x
        if p_t < s_t: # 사람이 먼저 도착
            eat_time = s_t + (p_x - s_x + L) % L
            
        else: # 사람이 나중에 도착
            moved_dist = (p_t - s_t)
            need_time = (p_x - (s_x + moved_dist) % L) % L
            eat_time = p_t + need_time
        #print(name, eat_time)
        queries.append(Query(111, eat_time, name=name))
        people_out[name] = max(people_out[name], eat_time)

for name, time in people_out.items():
    queries.append(Query(222, time, name=name))
    
queries.sort(key=lambda x:(x.t, x.cmd))

# for q in queries:
#     print("Query")
#     print(q.cmd, q.t, q.x, q.name, q.n)

n_people = 0
n_sushi = 0
for q in queries:
    if q.cmd == 100:
        n_sushi += 1
    elif q.cmd == 200:
        n_people += 1
    elif q.cmd == 111:
        n_sushi -= 1
    elif q.cmd == 222:
        n_people -= 1
    else:
        print(n_people, n_sushi)