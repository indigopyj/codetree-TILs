import copy
q = int(input())

belts = dict()
boxes = dict()
weights = dict()
heads = dict()
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
            belts[b_id].append(box_id)
            weights[box_id] = w
            boxes[box_id] = b_id
        # print(belts)
        # print(boxes)
        # print(weights)

    elif cmd == 200: # box out
        w_max = inputline[1]
        total_sum = 0
        for b_id, belt in belts.items():
            # print(b_id, belt)
            if belt is None or len(belt) == 0:
                continue
            
            if weights[belt[0]] > w_max:
                item = belt[0]
                belt.append(item)
            else:
                total_sum += weights[belt[0]]
                # print("pop box", belt[0])
                del boxes[belt[0]]
            del belt[0]
        print(total_sum)
    elif cmd == 300: # remove box
        r_id = inputline[1]
        if r_id not in boxes:
            print(-1)
            continue
        belt_id = boxes[r_id]
        new_belt = []
        # for b in belts[belt_id]:
        #     if b == r_id:
        #         continue
        #     new_belt.append(b)
        # belts[belt_id] = new_belt
        belts[belt_id].remove(r_id)
        del boxes[r_id]
        print(r_id)

    elif cmd == 400: # check box
        f_id = inputline[1]
        if f_id not in boxes:
            print(-1)
            continue
        belt_id = boxes[f_id]
        print(belt_id)
        if belts[belt_id] is not None:
            # new_belt = []
            # idx = 0
            idx = belts[belt_id].index(f_id)
            # for i, (box_id, _) in enumerate(belts[belt_id]):
            #     if box_id == f_id:
            #         idx = i
            new_belt = belts[belt_id][idx:] + belts[belt_id][:idx]
            belts[belt_id] = new_belt
            # print(new_belt)
        

    else: # break belt
        b_num = inputline[1]
        if b_num not in belts or belts[b_num] is None:
            print(-1)
            continue
        # tmp = copy.deepcopy(belts[b_num])
        
        belt_list = list(range(b_num+1, m+1)) + list(range(1,m+1))
        new_b_id = b_num
        for b in belt_list:
            if b_num!= b and belts[b] is not None:
                new_b_id = b
                break
        # print(belts[new_b_id])
        
        belts[new_b_id] = belts[new_b_id] + belts[b_num]
        for b in belts[b_num]:
            boxes[b] = new_b_id
        belts[b_num] = None
        print(b_num)
        # print(belts[new_b_id])
        # print(boxes)