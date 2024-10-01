from collections import defaultdict
q = int(input())
MAX_N = 100000+1
MAX_M = 10+1

prevs = defaultdict(int)
nexts = defaultdict(int)
weights = dict()
heads = [0] * MAX_M
tails = [0] * MAX_M
broken = [0] * MAX_M
belt_num = defaultdict(lambda : -1)

def remove_item(item):
    b_id = belt_num[item]

    if heads[b_id] == tails[b_id]:
        heads[b_id] = tails[b_id] = 0
    elif item == heads[b_id]:
        next_item = nexts[item]
        heads[b_id] = next_item
        prevs[item] = 0
    elif item == tails[b_id]:
        prev_item = prevs[item]
        tails[b_id] = prev_item
        nexts[item] = 0
    else:
        prev_item = prevs[item]
        next_item = nexts[item]
        prevs[next_item] = prev_item
        nexts[prev_item] = next_item 

    prevs[item] = 0
    nexts[item] = 0

def push_item(tail, item):
    b_id = belt_num[item]
    nexts[item] = tail
    prevs[tail] = item

    if tail == tails[b_id]: # 같은 벨트의 tail에 붙은거라면
        tails[b_id] = item



for _ in range(q):
    inputline = list(map(int, input().split()))
    cmd = inputline[0]
    # print(inputline)
    if cmd == 100:
        n, m = inputline[1:3]
        ids = inputline[3:3+n]
        ws = inputline[3+n:]

        for i in range(n):
            weights[ids[i]] = ws[i]
        
        s = n//m

        for i in range(m):
            heads[i] = ids[s*i]
            tails[i] = ids[s*(i+1) - 1]

            for j in range(s):
                box_id = s*i + j
                belt_num[ids[box_id]] = i

                if j < s-1:
                    prevs[ids[box_id+1]] = ids[box_id]
                    nexts[ids[box_id]] = ids[box_id+1]
        # print(prevs, nexts)

    elif cmd == 200: # box out
        w_max = inputline[1]
        total_sum = 0
        for i in range(m):
            if broken[i] != 0: # if belt is broken
                continue
            item = heads[i]
            if item != 0:
                if weights[item] <= w_max:
                    total_sum += weights[item]
                    heads[i] = 0
                    remove_item(item)
                    belt_num[item] = -1
                elif nexts[id] != 0: # 원소가 하나만 있으면 그냥 유지
                    remove_item(item)
                    push_item(tails[i], item)            
        print(total_sum)

    elif cmd == 300: # remove box
        r_id = inputline[1]
        if belt_num[r_id] == -1: # 이미 사라진 상자
            print(-1)
            continue
        remove_item(r_id)
        belt_num[r_id] = -1
        print(r_id)

    elif cmd == 400: # check box
        f_id = inputline[1]
        ans = -1
        if belt_num[f_id] != -1:
            b_id = belt_num[f_id]
            ans = b_id + 1
            if heads[b_id] != f_id:
                origin_tail = tails[b_id]
                origin_head = heads[b_id]
                prev_item = prevs[f_id]
                next_item = nexts[f_id]

                nexts[prev_item] = 0
                heads[b_id] = f_id
                tails[b_id] = prev_item
                
                nexts[origin_tail] = origin_head
                prevs[origin_head] = origin_tail
            
        print(ans)
            

    else: # break belt
        b_num = inputline[1] - 1
        if broken[b_num] != 0:
            print(-1)
            continue
        broken[b_num] = 1

        if heads[b_num] == 0 and tails[b_num] == 0: # nothing
            continue
        
        b_list = list(range(b_num+1, m)) + list(range(m))

        for b_id in b_list:
            if broken[b_id] == 0:
                if heads[b_id] == 0 and tails[b_id] == 0:
                    heads[b_id] = heads[b_num]
                    tails[b_id] = tails[b_num]
                
                else:
                    push_item(tails[b_id], heads[b_num])
                    tails[b_num] = tails[b_id]
            
                id = heads[b_num]
                while id != 0:
                    belt_num[id] = b_num
                    id = nexts[id]
                break
        print(b_num+1)