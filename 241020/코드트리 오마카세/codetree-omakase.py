from collections import defaultdict
L, Q = map(int, input().split())

def update_eattime(name):
    if name not in people_time:
        return
    p_t, p_x = people_time[name]
    for i, s in enumerate(sushi[name]):
        if name not in people or s[2] >= 0:
            continue
        s_t = s[0]
        s_x = s[1]
        
        if s_t < p_t:
            curr_pos = ((p_t - s_t+L)%L + s_x ) % L
            eat_time = (p_t + p_x - curr_pos)
        else:
            eat_time = (p_x - s_x + L) % L + s_t
        sushi[name][i] = [s_t, s_x, eat_time]
    
def eat_sushi(t):
    n_sushi = 0
    n_people = len(people)
    for name, s_list in sushi.items():
        eaten_sushi = 0
        n_sushi += len(s_list)
        
        if len(s_list) != 0 and name in people:
            count = 0
            total_s = len(s_list)
            while count < total_s:
                s = s_list.pop(0)
                #print(s)
                if s[-1] <= t:
                    eaten_sushi += 1
                else:
                    s_list.append(s)
                count += 1
            people[name] -= eaten_sushi
            n_sushi -= eaten_sushi
            
            
            if people[name] == 0:
                n_people -= 1
                del people[name]
    return n_people, n_sushi
            
                
          
    

sushi = defaultdict(list)
people = dict()
people_time = dict()
for _ in range(Q):
    line = input().split()
    cmd = int(line[0])
    if cmd == 100:
        t, x, name = line[1:]
        sushi[name].append([int(t), int(x), -1])
        update_eattime(name)
    elif cmd == 200:
        t, x, name, n = line[1:]
        people[name] = int(n)
        people_time[name] = (int(t),int(x))
        update_eattime(name)
    elif cmd == 300:
        t = int(line[1])
        res = eat_sushi(t)
        print(res[0], res[1])
    #print(sushi, people)