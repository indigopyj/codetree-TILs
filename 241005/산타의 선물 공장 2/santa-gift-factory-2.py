from collections import defaultdict

fronts, backs, heads, tails = None, None, None, None
which_belts = None
n_boxes = None

def pop_head(b_id):
    pop_head = heads[b_id]
    heads[b_id] = backs[pop_head]
    fronts[backs[pop_head]] = 0
    backs[pop_head] = 0
    n_boxes[b_id] -= 1
    which_belts[pop_head] = 0
    if n_boxes[b_id] == 0:
        tails[b_id] = 0
    return pop_head

def push_head(b_id, new_item):
    if heads[b_id] != 0:
        old_head = heads[b_id]
        fronts[old_head] = new_item
        backs[new_item] = old_head
    heads[b_id] = new_item
    n_boxes[b_id] += 1
    which_belts[new_item] = b_id
    if n_boxes[b_id] == 1:
        tails[b_id] = new_item


q = int(input())
for _ in range(q):
    line = list(map(int, input().split()))
    cmd = line[0]
    if cmd == 100:
        n,m = line[1:3]
        boxes = line[3:]
        belts = dict()
        for i in range(n):
            belts[i+1] = []
        which_belts = [0] * (m+1)
        fronts = [0] * (m+1)
        backs = [0] * (m+1)
        heads = [0] * (n+1)
        tails = [0] * (n+1)
        n_boxes = [0] * (n+1)

        for i in range(m):
            b_id = boxes[i]
            belts[b_id].append(i+1)
            which_belts[i+1] = b_id
        
        for b_id, belt in belts.items():
            if len(belt) != 0:
                heads[b_id] = belt[0]
                tails[b_id] = belt[-1]
                n_boxes[b_id] = len(belt)
                for j in range(1, len(belt)):
                    fronts[belt[j]] = belt[j-1]
                    backs[belt[j-1]] = belt[j]
            
        # print(heads, tails)
        # print(fronts, backs)

    elif cmd == 200:
        m_src, m_dst = line[1:]
        if n_boxes[m_src] == 0:
            print(n_boxes[m_dst])
            continue
        
        tmp = []
        n_src = n_boxes[m_src]
        for _ in range(n_src):
            item = pop_head(m_src)
            tmp.append(item)

        for item in tmp[::-1]:
            push_head(m_dst, item)
        # print(n_boxes[m_src], n_boxes[m_dst])
        # print(fronts, backs)
        # print(heads, tails)
        print(n_boxes[m_dst])
    
    elif cmd == 300:
        m_src, m_dst = line[1:]
        dst_head = heads[m_dst]
        src_head = heads[m_src]
        if src_head == 0 and dst_head != 0:
            dst_head = pop_head(m_dst)
            push_head(m_src, dst_head)
        elif src_head != 0 and dst_head == 0:
            src_head = pop_head(m_src)
            push_head(m_dst, src_head)
        elif src_head != 0 and dst_head != 0:
            dst_head = pop_head(m_dst)
            src_head = pop_head(m_src)
            push_head(m_src, dst_head)
            push_head(m_dst, src_head)
        print(n_boxes[m_dst])
        # print(n_boxes[m_src], n_boxes[m_dst])
        # print(fronts, backs)
        # print(heads, tails)
    elif cmd == 400:
        m_src, m_dst = line[1:]
        if n_boxes[m_src] <= 1:
            print(n_boxes[m_dst])
            continue
        move_boxes = n_boxes[m_src] // 2
        tmp = []
        for i in range(move_boxes):
            item = pop_head(m_src)
            tmp.append(item)
        for item in tmp[::-1]:
            push_head(m_dst, item)

        print(n_boxes[m_dst])
        # print(n_boxes[m_src], n_boxes[m_dst])
        # print(fronts, backs)
        # print(heads, tails)

    elif cmd == 500:
        p_num = line[1]
        a = fronts[p_num] if fronts[p_num] != 0 else -1
        b = backs[p_num] if backs[p_num] != 0 else -1
        print(a + 2*b)
    else:
        b_num = line[1]
        a = heads[b_num] if heads[b_num] != 0 else -1
        b = tails[b_num] if tails[b_num] != 0 else -1
        c = n_boxes[b_num]
        print(a + 2*b + 3*c)