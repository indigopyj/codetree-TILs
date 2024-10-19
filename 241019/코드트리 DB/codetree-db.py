class Node:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sum = 0
        self.count = 0
        self.id = 0
        self.left = None
        self.right = None


class Tree:
    def __init__(self, start, end):
        self.root = Node(start, end)
        
    def update(self, node, idx, id, sum, count):
        #print(node.start, node.end, node.left, node.right, node.id, node.count)
        if node.start == node.end:
            node.sum = sum
            node.id = id
            node.count = count
            
            return
        
        mid = (node.start + node.end) // 2
        if idx <= mid:
            if node.left is None:
                node.left = Node(node.start, mid)
            self.update(node.left, idx, id, sum, count)
            # if node.left.sum == 0:
            #     node.left = None
        else:
            if node.right is None:
                node.right = Node(mid+1, node.end)
            self.update(node.right, idx, id, sum, count)
            # if node.right.sum == 0:
            #     node.right = None
        node.sum = 0
        node.count = 0
        if node.right is not None:
            node.sum += node.right.sum
            node.count += node.right.count
        if node.left is not None:
            node.sum += node.left.sum
            node.count += node.left.count
            
        
    def range_sum(self, node, left, right):
        if node is None or node.end < left or node.start > right:
            return 0
        if node.start >= left and node.end <= right:
            return node.sum
        total = 0
        if node.left:
            total +=  self.range_sum(node.left, left, right)
        if node.right:
            total +=  self.range_sum(node.right, left, right)
        return total
    
    def rank(self, k, node):
        # print(k, node.start, node.end, node.left, node.right, node.count, node.sum, node.id)
        if node.count < k:
            return None
        if node.left:
            # print(node.left.count, node.left.left, node.left.right, node.left.sum)
            if node.left.count >= k:
                # print(f"left, {k}")
                return self.rank(k, node.left)
            elif node.right:
                # print(node.right.count)
                # print(f"right, {k-node.left.count}")
                return self.rank(k-node.left.count, node.right)
        if node.right:
            # print(f"right, {k}")
            return self.rank(k, node.right)
        
        return node.id
        
        
            

def insert(name, value):
    global entry_count
    if name in name_to_index or value in used_vals:
        return 0
    entry_count += 1
    name_to_index[name] = entry_count
    names[entry_count] = name
    values[entry_count] = value
    used_vals.add(value)

    tree.update(tree.root, value, entry_count, value, 1)
    return 1
    
def delete(name):
    if name not in name_to_index:
        return 0
    if names[name_to_index[name]] == '':
        return 0
    
    idx = name_to_index[name]
    #print(name, idx, values)
    names[idx] = ''
    val = values[idx]
    used_vals.discard(val)
    values[idx] = 0
    
    tree.update(tree.root, val, idx, 0, 0)
    return val

def rank(k):
    
    if k > tree.root.count:
        return None
    # print(names[:10])
    idx = tree.rank(k, tree.root)
    if idx == None:
        return None
    return names[idx]

def sum(k):
    return tree.range_sum(tree.root, 0, k)

Q = int(input())
tree = Tree(start=0, end=10**9)
for _ in range(Q):
    line = input().split()
    cmd = line[0]
    # print(line)
    if cmd == 'init':
        tree = Tree(start=0, end=10**9)
        name_to_index = {}
        used_vals = set()
        entry_count = 0
        names = ["" for _ in range(100002)]
        values = [0 for _ in range(100002)]
        
    elif cmd == 'insert':
        name, value = line[1], int(line[2])
        # insert(name, value)
        print(insert(name, value))
        # print(name_to_index)
                
    elif cmd == 'delete':
        name = line[1]
        # delete(name)
        print(delete(name))
    elif cmd == 'rank':
        k = int(line[1])
        # rank(k)
        print(rank(k))
            
    elif cmd == 'sum':
        k = int(line[1])
        print(sum(k))