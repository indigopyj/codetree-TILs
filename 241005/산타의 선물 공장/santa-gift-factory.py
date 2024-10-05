q = int(input())
heads, tails, fronts, backs, which_belt, broken = None, None, None, None, None, None


def pop_head(b_id):
    global heads, tails, fronts, backs, which_belt, broken
    pop_head = heads[b_id]
    heads[b_id] = backs[pop_head]
    fronts[backs[pop_head]] = 0
    if backs[pop_head] == 0:
        tails[b_id] = 0
    backs[pop_head] = 0
    which_belt[pop_head] = -1
    return pop_head

def push_head(b_id, item):
    old_head = heads[b_id]
    which_belt[item] = b_id
    if old_head == 0:
        heads[b_id] = item
        tails[b_id] = item
        fronts[item] = 0 
        backs[item] = 0
        return
    fronts[old_head] = item
    backs[item] = old_head
    heads[b_id] = item
    fronts[item] = 0
    
    return

for _ in range(q):
    line = list(map(int, input().split()))
    # print(line)
    cmd = line[0]
    if cmd == 100:
        n,m = line[1:3]
        id_list = line[3:3+n]
        w_list = line[3+n:]
        belts = dict()
        weights = dict()
        heads = [0] * (m+1)
        tails = [0] * (m+1)
        fronts = [0] * (n+1)
        backs = [0] * (n+1)
        which_belt = [-1] * (n+1)
        broken = [False] * (m+1)
        i_to_iid = dict()
        iid_to_i = dict()
        for i in range(1,m+1):
            belts[i] = []
        for i in range(n):
            iid = id_list[i]
            i_to_iid[i+1] = iid
            iid_to_i[iid] = i+1
            b_id = i // (n // m) + 1
            belts[b_id].append(i+1)
            weights[i+1] = w_list[i]

        for b_id, belt in belts.items():
            if len(belt) != 0:
                heads[b_id] = belt[0]
                tails[b_id] = belt[-1]
                which_belt[belt[0]] = b_id
                for j in range(1, len(belt)):
                    fronts[belt[j]] = belt[j-1]
                    backs[belt[j-1]] = belt[j]
                    which_belt[belt[j]] = b_id
        # print(i_to_iid)
        # print(heads, tails)
        # print(fronts, backs)

    elif cmd == 200:
        w_max = line[1]
        popped_list = []
        total_sum = 0
        # print(i_to_iid)
        # print(heads, tails)
        for i in range(1,m+1):
            if heads[i] == 0 or broken[i]:
                continue
            head_weight = weights[heads[i]]
            if head_weight <= w_max:
                item = pop_head(i)
                # print("here")
                # print(heads, tails)
                total_sum += weights[item]
            else:
                head = pop_head(i)
                which_belt[head] = i
                old_tail = tails[i]
                fronts[head] = old_tail
                backs[old_tail] = head
                tails[i] = head
                # print("there")
                # print(heads, tails)
        print(total_sum)

    elif cmd == 300:
        r_id = line[1]
        if r_id not in iid_to_i:
            print(-1)
            continue
        box_i = iid_to_i[r_id]
        belt_i = which_belt[box_i]

        if belt_i == -1:
            print(-1)
            continue
        print(r_id)
        which_belt[box_i] = -1
        front = fronts[box_i]
        back = backs[box_i]
        if heads[belt_i] == box_i:
            heads[belt_i] = back
        if tails[belt_i] == box_i:
            tails[belt_i] = front
        if front != 0:
            backs[front] = back
        if back != 0:
            fronts[back] = front
        fronts[box_i] = backs[box_i] = 0
        # print(i_to_iid)
        # print(heads, tails)
        # print(fronts, backs)

    elif cmd == 400:
        f_id = line[1]
        if f_id not in iid_to_i:
            print(-1)
            continue
        box_i = iid_to_i[f_id]
        belt_i = which_belt[box_i]
        if belt_i == -1:
            print(-1)
            continue
        print(belt_i)
        origin_tail = tails[belt_i]
        origin_head = heads[belt_i]
        if origin_head == box_i:
            continue
        elif origin_tail == box_i:
            new_tail = fronts[origin_tail]
            backs[new_tail] = 0
            tails[belt_i] = new_tail
            push_head(belt_i, box_i)
        else:
            new_tail = fronts[origin_tail]
            fronts[origin_head] = origin_tail
            backs[origin_tail] = origin_head

            heads[belt_i] = box_i
            tails[belt_i] = new_tail
            backs[new_tail] = 0
            fronts[box_i] = 0
        # print(i_to_iid)
        # print(heads, tails)
        # print(fronts, backs)


    else:
        b_num = line[1]
        if broken[b_num] :
            print(-1)
            continue
        candidates= list(range(b_num+1, m+1)) + list(range(1, m+1))
        broken[b_num] = True
        
        for belt_i in candidates:
            if broken[belt_i] == False:
                break
        
        if heads[belt_i] == 0:
            heads[belt_i] = heads[b_num]
            tails[belt_i] = tails[b_num]
            item = backs[heads[b_num]]
            which_belt[heads[b_num]] = belt_i
            
            while item != 0:
                which_belt[item] = belt_i
                item = backs[item]
            heads[b_num] = tails[b_num] = 0

        else:
            broken_head = heads[b_num]
            broken_tail = tails[b_num]
            origin_tail = tails[belt_i]

            item = backs[broken_head]
            which_belt[broken_head] = belt_i
            
            while item != 0:
                which_belt[item] = belt_i
                item = backs[item]        
            backs[origin_tail] = broken_head
            fronts[broken_head] = origin_tail
            tails[belt_i] = broken_tail
            heads[b_num] = tails[b_num] = 0
        # print(heads, tails)
        
        print(b_num)