def search(arr, item, total):
    if total == 0:
        return 0,0
    if total == 1:
        if arr[0][1] > item:
            return 0,0
        elif arr[0][1] < item:
            return 0,1
        else:
            return -1,0
            
    start = 0    
    end = total - 1
    

    while True:
        mid = (start+end) // 2
        # print(start, mid, end, total)
        if arr[mid][1] > item:
            end = mid-1
        elif arr[mid][1] < item:
            start = mid+1
        else:
            return -1, mid
        if end < start:
            return 0, start
        

def insert_item(r_id, name, value, total):

    flag, name_pos = search(names, name, total)
    if flag < 0:
        return False
    flag, val_pos = search(values, value, total)
    if flag < 0:
        return False
    
    names.insert(name_pos, (r_id, name))
    values.insert(val_pos, (r_id, value))
    item_info[r_id] = (name, value)
    # print(names, values)
    return True

def delete_item(r_id, name, total):
    flag, name_pos = search(names, name, total)
    if flag == 0:
        return False
    r_id = names[name_pos][0]
    value = item_info[r_id][1]
    names.remove((r_id, name))
    values.remove((r_id, value))
    del item_info[r_id]
    # print(names, values)
    return value
    
def rank_item(k):
    r_id, val = values[k-1]
    return item_info[r_id][0]
    
def sum_item(k, total):
    flag, val_pos = search(values, k, total)
    if flag < 0:
        return 0
    return sum([item[1] for item in values[:val_pos]])
        

Q = int(input())
for _ in range(Q):
    line = input().split()
    cmd = line[0]
    if cmd == 'init':
        names = []
        values = []
        item_info = dict()
        r_id = 0
        total = 0
    elif cmd == 'insert':
        name, value = line[1], int(line[2])
        result = insert_item(r_id, name, value, total)
        if result == 1:
            total += 1
            r_id += 1
            print(1)
        else:
            print(0)
    elif cmd == 'delete':
        name = line[1]
        result = delete_item(r_id, name, total)
        if result is False:
            print(0)
            continue
        total -= 1
        print(result)
    elif cmd == 'rank':
        k = int(line[1])
        if total < k:
            print("None")
        else:
            print(rank_item(k))
            
    elif cmd == 'sum':
        k = int(line[1])
        print(sum_item(k, total))