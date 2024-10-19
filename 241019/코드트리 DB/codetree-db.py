class Node:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sum = 0
        self.left = None
        self.right = None


class Tree:
    def __init__(self, start, end):
        self.root = Node(start, end)
        
    def update(self, node, idx, value):
        
        if node.start == node.end:
            node.sum = value
            return
        
        mid = (node.start + node.end) // 2
        if idx <= mid:
            if node.left is None:
                node.left = Node(node.start, mid)
            self.update(node.left, idx, value)
        else:
            if node.right is None:
                node.right = Node(mid+1, node.end)
            self.update(node.right, idx, value)
        
        node.sum = 0
        if node.right is not None:
            node.sum += node.right.sum
        if node.left is not None:
            node.sum += node.left.sum
        
    def range_sum(self, node, left, right):
        
        if node is None or node.end < left or node.start > right:
            return 0
        
        if node.start >= left and node.end <= right:
            return node.sum
        
        total = 0
        if node.left:
            total +=  self.range_sum(node.left, left, right)
            ##print("left : ", total)
        if node.right:
            total +=  self.range_sum(node.right, left, right)
            #print("right : ", total)
        return total

def insert(name, value):
    for n, v in data_info.items():
        if name == n:
            return 0
        if value == v:
            return 0
    
    data_info[name] = value
    tree.update(tree.root, value, value)
    return 1
    
def delete(name):
    flag = False
    value = 0
    for n, v in data_info.items():
        if name == n:
            flag = True
            value = v
            break
    if not flag:
        return 0
    del data_info[name]
    tree.update(tree.root, value, 0)
    return value

def rank(k):
    if k > len(data_info):
        return None
    sort_dict = sorted(data_info.items(), key=lambda x:x[1])
    k, v = sort_dict[k-1]
    return k

def sum(k):
    return tree.range_sum(tree.root, 0, k)

Q = int(input())

for _ in range(Q):
    line = input().split()
    cmd = line[0]
    
    if cmd == 'init':
        tree = Tree(start=0, end=10**9)
        data_info = dict()
        
    elif cmd == 'insert':
        name, value = line[1], int(line[2])
        print(insert(name, value))
                
    elif cmd == 'delete':
        name = line[1]
        print(delete(name))
    elif cmd == 'rank':
        k = int(line[1])
        print(rank(k))
            
    elif cmd == 'sum':
        k = int(line[1])
        print(sum(k))