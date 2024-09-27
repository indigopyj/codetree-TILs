from collections import deque, defaultdict
import math
MAX_M = 100001
MAX_N = 100001
q = int(input())

inputline = list(map(int, input().split()))

n, m = inputline[1:3]
prevs = [0] * MAX_M
nexts = [0] * MAX_M
heads = [0] * MAX_N
tails = [0] * MAX_N
n_boxes = [0] * MAX_N
belts = dict()

for i in range(1, n+1):
    belts[i] = []

for s_id in range(1, m+1):
    b_id = inputline[2+s_id]
    belts[b_id].append(s_id)

for i in range(1, n+1):
    heads[i] = belts[i][0] if len(belts[i]) > 0 else 0
    tails[i] = belts[i][-1] if len(belts[i]) > 0 else 0
    n_boxes[i] = len(belts[i])
    for j in range(n_boxes[i]-1):
        box = belts[i][j]
        nexts[box] = belts[i][j+1]
        next_box = belts[i][j+1]
        prevs[next_box] = box
        

def move(m_src, m_dst):
    if n_boxes[m_src] == 0:
        print(n_boxes[m_dst])
        return
    
    origin_dst_head = heads[m_dst]
    origin_src_tail = tails[m_src]
    heads[m_dst] = heads[m_src]
    nexts[origin_src_tail] = origin_dst_head
    prevs[origin_dst_head] = origin_src_tail
    n_boxes[m_dst] += n_boxes[m_src]

    n_boxes[m_src] = 0
    heads[m_src], tails[m_src] = 0, 0

    print(n_boxes[m_dst])

def remove_head(b_id):
    if n_boxes[b_id] == 0:
        return 0
    if n_boxes[b_id] == 1:
        heads[b_id] = 0
        origin_head = heads[b_id]
        nexts[origin_head] = prevs[origin_head] = 0
        n_boxes[b_id] = 0
        return origin_head
    origin_head = heads[b_id]
    new_head = nexts[origin_head]
    heads[b_id] = new_head
    nexts[origin_head] = 0
    prevs[new_head] = 0
    n_boxes[b_id] -= 1
    return origin_head

def push_head(b_id, new_head):
    if new_head == 0:
        return
    if n_boxes[b_id] == 0:
        heads[b_id] = new_head
        tails[b_id] = new_head
        n_boxes[b_id] += 1
        return

    origin_head = heads[b_id]
    prevs[origin_head] = new_head
    nexts[new_head] = origin_head
    heads[b_id] = new_head
    n_boxes[b_id] += 1
 
def change_head(m_src, m_dst):
    src_head = heads[m_src] # 0
    dst_head = heads[m_dst] # 2
    # print(src_head, dst_head)
    remove_head(m_src)
    remove_head(m_dst)
    # print(heads[m_src], heads[m_dst])

    push_head(m_src, dst_head)
    push_head(m_dst, src_head)
    # print(heads[m_src], heads[m_dst])
    print(n_boxes[m_dst])
    
def divide(m_src, m_dst):
    if n_boxes[m_src] == 1:
        print(n_boxes[m_dst])
        return

    N = math.floor(n_boxes[m_src] / 2)
    boxes = []
    for i in range(N):
        elem = remove_head(m_src)
        boxes.append(elem)
    for box in boxes:
        push_head(m_dst, box)
    print(n_boxes[m_dst])


for _ in range(q-1):
    inputline = list(map(int, input().split()))
    cmd = inputline[0]
    if cmd == 200:
        m_src, m_dst = inputline[1:]
        move(m_src, m_dst)
    elif cmd == 300:
        m_src, m_dst = inputline[1:]
        change_head(m_src, m_dst)
    elif cmd == 400:
        m_src, m_dst = inputline[1:]
        divide(m_src, m_dst)
    elif cmd == 500:
        p_num = inputline[1]
        a = prevs[p_num] if prevs[p_num] != 0 else -1
        b = nexts[p_num] if nexts[p_num] != 0 else -1
        res = a + 2*b
        print(res)
    else:
        b_num = inputline[1]
        if n_boxes[b_num] == 0:
            res = -3
        else:
            # a = heads[p_num] if prevs[p_num] != 0 else -1
            # b = nexts[p_num] if nexts[p_num] != 0 else -1
            # print(heads[b_num], tails[b_num], n_boxes[b_num])
            res = heads[b_num] + 2*tails[b_num] + 3*n_boxes[b_num]
        print(res)