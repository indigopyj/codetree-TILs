from collections import deque, defaultdict
import math

q = int(input())

inputline = list(map(int, input().split()))

n, m = inputline[1:3]
fronts = dict()
backs = dict()
n_stuff = defaultdict(int)
stuff_info = dict()
belts = dict()
for i in range(1, n+1):
    belts[i] = []

# for i in range(1, n+1):
#     belts[i] = deque()
for i in range(1, m+1):
    n_belt = inputline[2+i]
    stuff_info[i] = -3
    belts[n_belt].append(i)
    
    if len(belts[n_belt]) >= 2:
        a = belts[n_belt][-2]
        stuff_info[i] = a - 2
        stuff_info[a] += 2 
        stuff_info[a] += 2*belts[n_belt][-1]

# for n_belt, belt in belts.items():
#     n_stuff[n_belt] = len(belt)
#     if len(belt) != 0:
#         fronts[n_belt] = belts[0]
#         backs[n_belt] = belts[-1]

def update_info(src, new_before=-1, new_behind=-1):
    stuff_info[src] = new_before+ 2*new_behind

# print(belts)
# print(stuff_info)

for _ in range(q-1):
    inputline = list(map(int, input().split()))
    # print("cmd: ", inputline)
    if inputline[0] == 200:
        # move stuff
        m_src, m_dst = inputline[1:]
        if len(belts[m_src]) != 0:
            
            src_last = belts[m_src][-1] 
            trg_first = belts[m_dst][0] if len(belts[m_dst]) != 0 else -1
            update_info(src_last, belts[m_src][-2] if len(belts[m_src]) >= 2 else -1, trg_first)
            update_info(trg_first, src_last, belts[m_dst][1] if len(belts[m_dst]) >= 2 else -1)
            
            belts[m_dst] = belts[m_src] + belts[m_dst]
            belts[m_src] = []
            # fronts[m_src] = -1
            # backs[m_src] = -1
            # fronts[m_trg] = belts[0]
            print(len(belts[m_dst]))
            

    elif inputline[0] == 300:
        # change front stuff
        # print("before change")
        # print(belts[m_src])
        # print(belts[m_dst])
        m_src, m_dst = inputline[1:]
        
        src_first = belts[m_src][0] if len(belts[m_src]) != 0 else -1
        trg_first = belts[m_dst][0] if len(belts[m_dst]) != 0 else -1

        if len(belts[m_src]) > 0:
            del belts[m_src][0]
        if len(belts[m_dst]) > 0:
            del belts[m_dst][0]
        if src_first != -1:
            belts[m_dst].insert(0, src_first)
        if trg_first != -1:
            belts[m_src].insert(0, trg_first)
        if len(belts[m_dst]) != 0:
            update_info(belts[m_dst][0], -1, belts[m_dst][1] if len(belts[m_dst]) >= 2 else -1)
        if len(belts[m_src]) != 0:
            update_info(belts[m_src][0], -1, belts[m_src][1] if len(belts[m_src]) >= 2 else -1)
        # print("after change")
        # print(belts[m_src])
        # print(belts[m_dst])
        print(len(belts[m_dst]))
        
        

    elif inputline[0] == 400:
        # split stuff
        m_src, m_dst = inputline[1:]
        n = len(belts[m_src])
        if n == 1:
            print(len(belts[m_dst]))
            continue
        slice_idx = math.floor(n / 2)
        sliced_src = belts[m_src][:slice_idx]
        rest_src = belts[m_src][slice_idx:]
        src_last = sliced_src[-1]
        trg_first = belts[m_dst][0] if len(belts[m_dst]) != 0 else -1
        update_info(src_last, sliced_src[-2] if len(sliced_src) >= 2 else -1, trg_first)
        update_info(trg_first, src_last, belts[m_dst][1] if len(belts[m_dst]) >= 2 else -1)
        if len(rest_src) > 0:
            update_info(rest_src[0], -1, rest_src[1] if len(rest_src) >= 2 else -1)
        belts[m_dst] = sliced_src + belts[m_dst]   
        belts[m_src] = rest_src


        print(len(belts[m_dst]))

    elif inputline[0] == 500:
        # get stuff info
        p_num = inputline[1]
        print(stuff_info[p_num])
    else:
        # get belt info
        b_num = inputline[1]
        a,b,c = -1,-1,0
        if len(belts[b_num]) > 0 :
            a = belts[b_num][0]
            b = belts[b_num][-1]
            c = len(belts[b_num])
        res = a + 2*b + 3*c
        print(res)
    # print(stuff_info)