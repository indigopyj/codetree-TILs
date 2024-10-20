from collections import defaultdict
L, Q = map(int, input().split())

def update_eattime(name):
    p_t, p_x = people_time[name]
    for i, s in enumerate(sushi[name]):
        if name not in people:
            continue
        s_t = s[0]
        s_x = s[1]
        
        if s_t < p_t:
            curr_pos = ((p_t - s_t) + s_x ) % L
            eat_time = (p_t + (p_x - curr_pos+L) % L)
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
            
                
          
    

sushi = defaultdict(list)
people = dict()
people_time = dict()
photo_time = []
for _ in range(Q):
    line = input().split()
    cmd = int(line[0])
    if cmd == 100:
        t, x, name = line[1:]
        sushi[name].append([int(t), int(x), -1])
        
    elif cmd == 200:
        t, x, name, n = line[1:]
        people[name] = int(n)
        people_time[name] = (int(t),int(x))
        
    elif cmd == 300:
        t = int(line[1])
        photo_time.append(t)

for name in people:
    update_eattime(name)
#print(sushi, people, people_time)

for t in photo_time:
    res = eat_sushi(t)
    print(res[0], res[1])