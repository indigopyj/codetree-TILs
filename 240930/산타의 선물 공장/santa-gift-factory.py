import copy
q = int(input())

belts = dict()
boxes = dict()
for _ in range(q):
    inputline = list(map(int, input().split()))
    cmd = inputline[0]
    # print(inputline)
    if cmd == 100:
        n, m = inputline[1:3]
        ids = inputline[3:3+n]
        weights = inputline[3+n:]
        # print(len(ids), len(weights))
        for i in range(1,m+1):
            belts[i] = []
        for i, (box_id, w) in enumerate(zip(ids, weights)):
            b_id = i // (n//m) + 1
            belts[b_id].append((box_id, w))
            boxes[box_id] = b_id
        # print(belts)
        # print(boxes)

    elif cmd == 200: # box out
        w_max = inputline[1]
        total_sum = 0
        for b_id, belt in belts.items():
            # print(b_id, belt)
            if belt is None or len(belt) == 0:
                continue
            if belt[0][1] > w_max:
                item = belt[0]
                belt.append(item)
            else:
                total_sum += belt[0][1]
                # print("pop box", belt[0])
                boxes[belt[0][0]] = -1
            del belt[0]
        print(total_sum)
    elif cmd == 300: # remove box
        r_id = inputline[1]
        if r_id not in boxes or boxes[r_id] == -1:
            print(-1)
            continue
        belt_id = boxes[r_id]
        new_belt = []
        for b in belts[belt_id]:
            if b[0] == r_id:
                continue
            new_belt.append(b)
        belts[belt_id] = new_belt
        boxes[r_id] = -1
        print(r_id)

    elif cmd == 400: # check box
        f_id = inputline[1]
        if f_id not in boxes:
            print(-1)
            continue
        belt_id = boxes[f_id]
        print(belt_id)
        if belt_id != -1 and belts[belt_id] is not None:
            new_belt = []
            idx = 0
            for i, (box_id, _) in enumerate(belts[belt_id]):
                if box_id == f_id:
                    idx = i
            new_belt = belts[belt_id][idx:] + belts[belt_id][:idx]
            belts[belt_id] = new_belt
            # print(new_belt)
        

    else: # break belt
        b_num = inputline[1]
        if b_num not in belts or belts[b_num] is None:
            print(-1)
            continue
        tmp = copy.deepcopy(belts[b_num])
        belts[b_num] = None
        belt_list = list(range(b_num+1, m+1)) + list(range(1,m+1))
        new_b_id = b_num
        for b in belt_list:
            if belts[b] is not None:
                new_b_id = b
                break
        # print(belts[new_b_id])
        belts[new_b_id] = belts[new_b_id] + tmp
        for b in tmp:
            boxes[b[0]] = new_b_id
        print(b_num)
        # print(belts[new_b_id])
        # print(boxes)