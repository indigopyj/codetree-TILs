class Node():
    def __init__(self, is_end=False):
        self.value = 0
        self.is_end = is_end
        self.children = dict()

class Trie():
    def __init__(self):
        self.root = Node() # root node
        self.values = []
        
    def insert(self, name, value):
        for n, v in self.values:
            if n == name or v == value:
                return 0
        curr = self.root
        for char in name:
            if char not in curr.children:
                curr.children[char] = Node()
            curr = curr.children[char]
        curr.is_end = True
        curr.value = value
        self.values.append((name, value))
        self.values.sort(key=lambda x:x[1])
        return 1
    
    def delete(self, name):
        curr = self.root
        node = []
        for char in name:
            if char in curr.children:
                node.append((curr, char)) 
                curr = curr.children[char]
            else:
                return 0
        if curr.is_end:
            value = curr.value
            curr.is_end = False
            curr.value = 0
            self.values = [item for item in self.values if item[0] != name]
            for n, c in node[::-1]: # 맨마지막노드는 포함안된 상태
                if not curr.is_end and len(curr.children) == 0:
                    del n.children[c]
                    curr = n
                else:
                    break
            return value
        return 0
                    
    def rank(self, k):
        if k <= len(self.values):
            return self.values[k-1][0]
        return None
    
    def sum(self, k):
        total = 0
        for n, v in self.values:
            if v <= k:
                total += v
            else:
                break
        return total
    
    def init(self):
        self.root = Node() # root node
        self.values = []
            
        

Q = int(input())
trie = Trie()
for _ in range(Q):
    line = input().split()
    cmd = line[0]
    
    if cmd == 'init':
        trie.init()
        
    elif cmd == 'insert':
        name, value = line[1], int(line[2])
        print(trie.insert(name, value))
        
    elif cmd == 'delete':
        name = line[1]
        print(trie.delete(name))
    elif cmd == 'rank':
        k = int(line[1])
        print(trie.rank(k))
            
    elif cmd == 'sum':
        k = int(line[1])
        print(trie.sum(k))