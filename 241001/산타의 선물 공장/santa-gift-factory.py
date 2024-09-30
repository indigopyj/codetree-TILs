import copy
q = int(input())
MAX_N = 100000+1
MAX_M = 10+1

belts = dict()
boxes = dict()
weights = dict()
arrid_to_boxid = dict()
boxid_to_arrid = dict()
heads = [-1] * MAX_M
tails = [-1] * MAX_M
prevs = [-1] * MAX_N
nexts = [-1] * MAX_N
for _ in range(q):
    inputline = list(map(int, input().split()))
    cmd = inputline[0]
    # print(inputline)
    if cmd == 100:
        n, m = inputline[1:3]
        ids = inputline[3:3+n]
        ws = inputline[3+n:]
        # print(len(ids), len(weights))
        for i in range(1,m+1):
            belts[i] = []
        for i, (box_id, w) in enumerate(zip(ids, ws)):
            b_id = i // (n//m) + 1
            arrid_to_boxid[i+1] = box_id
            boxid_to_arrid[box_id] = i+1
            belts[b_id].append(i+1)
            weights[i+1] = w
            boxes[i+1] = b_id
        # print(belts)
        for b_id, belt in belts.items():
            for i in range(1, len(belt)):
                prevs[belt[i]] = belt[i-1]
                nexts[belt[i-1]] = belt[i]
            heads[b_id] = belt[0]
            tails[b_id] = belt[-1]
        # print(prevs[:n+1])
        # print(nexts[:n])
        # print(heads)
        # print(tails)
        # print(arrid_to_boxid)
        # print(belts)
        # print(boxes)
        # print(weights)

    elif cmd == 200: # box out
        w_max = inputline[1]
        total_sum = 0
        for i in range(1, m+1):
            item = heads[i]
            
            if item == -1:
                continue
            if weights[item] <= w_max:
                # print("pop ", weights[item])
                total_sum += weights[item]
                heads[i] = nexts[item]
                # print(heads[i], item, nexts[:n+1])
                prevs[item] = -1
                nexts[item] = -1
                del boxes[item]
            else:
                heads[i] = nexts[item]
                prevs[item] = tails[i]
                nexts[item] = -1
                tails[i] = item
        # print(heads, tails)
        # for b_id, belt in belts.items():
        #     # print(b_id, belt)
        #     if belt is None or len(belt) == 0:
        #         continue
            
        #     if weights[belt[0]] > w_max:
        #         item = belt[0]
        #         belt.append(item)
        #     else:
        #         total_sum += weights[belt[0]]
        #         # print("pop box", belt[0])
        #         del boxes[belt[0]]
        #     del belt[0]
        print(total_sum)
    elif cmd == 300: # remove box
        r_id = inputline[1]
        if r_id not in boxid_to_arrid:
            print(-1)
            continue
        i = boxid_to_arrid[r_id]
        prev_item = prevs[i]
        next_item = nexts[i]
            
        if prev_item == -1 and next_item == -1: # 존재하지 않음
            print(-1)
            continue
        elif prev_item != -1: # 앞에 노드 존재
            nexts[prev_item] = next_item
            if next_item == -1: # 맨 뒤
                tails[boxes[i]] = prev_item
        elif next_item != -1: # 뒤에 노드 존재
            prevs[next_item] = prev_item
            if prev_item == -1: # 맨 앞
                heads[boxes[i]] = next_item
        
        prevs[i] = -1
        nexts[i] = -1
        del boxes[i]
        print(r_id)
        # print(heads, tails)

    elif cmd == 400: # check box
        f_id = inputline[1]
        if f_id not in boxid_to_arrid:
            print(-1)
            continue
        i = boxid_to_arrid[f_id]
        if prevs[i] == -1 and nexts[i] == -1 and i not in boxes:
            print(-1)
            continue
        belt_id = boxes[i]
        print(belt_id)
        prev_item = prevs[i]
        tail = tails[belt_id]
        nexts[tail] = heads[belt_id]
        heads[belt_id] = i
        tails[belt_id] = prev_item
        prevs[i] = -1 # 맨 앞
        # print(heads, tails)

    else: # break belt
        b_num = inputline[1]
        if b_num not in belts or (heads[b_num] == -1 and tails[b_num] == -1):
            print(-1)
            continue
        
        belt_list = list(range(b_num+1, m+1)) + list(range(1,m+1))
        new_b_id = b_num
        for b in belt_list:
            if b_num!= b and heads[b] != -1:
                new_b_id = b
                break
        # print("before")
        # print(heads, tails)
        head = heads[b_num]
        tail = tails[b_num]
        new_head = heads[new_b_id]
        new_tail = tails[new_b_id]
        prevs[head] = new_tail
        nexts[new_tail] = head
        tails[new_b_id] = tail
        heads[b_num] = -1
        tails[b_num] = -1
        # print("after")
        # print(heads, tails)
        for b in belts[b_num]:
            if b in boxes:
                boxes[b] = new_b_id
        
        print(b_num)
        # print(belts[new_b_id])
        # print(boxes)