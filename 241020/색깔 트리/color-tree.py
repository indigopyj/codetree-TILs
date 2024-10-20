class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        self.diff_color = set()
        self.children = []
        self.diff_color.add(color)
        self.value = 1
        
        
def update_value(m_id):
    node = node_dict[m_id]
    if node.p_id == -1:
        return
    nnode = node_dict[node.p_id]
    # print(nnode.diff_color, nnode.value)
    while True:
        nnode.diff_color = set([nnode.color])
        for c in nnode.children:
            nnode.diff_color = nnode.diff_color.union(node_dict[c].diff_color)
        nnode.value = len(nnode.diff_color)
        # print(nnode.diff_color, nnode.value)
        if nnode.p_id == -1:
            break
        nnode = node_dict[nnode.p_id]
        
def add_node(m_id, p_id, color, depth):
    node = Node(m_id, p_id, color, depth)
    if p_id == -1:
        node_dict[m_id] = node
        return
    depth_count = 1
    p_index = p_id
    while True:
        if p_index == -1:
            break
        p_node = node_dict[p_index]
        depth_count += 1
        if p_node.max_depth < depth_count:
            # print("failed", m_id)
            return
        p_index = p_node.p_id
    
    node_dict[m_id] = node
    node_dict[p_id].children.append(m_id)
    update_value(m_id)

def change_color(m_id, color):
    node = node_dict[m_id]
    node.color = color
    node.diff_color = set([color])
    node.value = 1
    for child in node.children:
        change_color(child, color)

def calculate_value(trees):
    total = 0
    for root_id in trees:
        q = [root_id]
        while q:
            id = q.pop(0)
            node = node_dict[id]
            # print(id, "value: ", node.value)
            total += node.value**2
            if len(node.children) != 0:
                q.extend(node.children)
    return total
            

Q = int(input())
node_dict = {}
trees = []
for _ in range(Q):
    line = list(map(int, input().split()))
    cmd = line[0]
    
    if cmd == 100:
        m_id, p_id, color, depth = line[1:]
        add_node(m_id, p_id, color, depth)
        if p_id == -1:
            trees.append(m_id)
        # print(node_dict)
    elif cmd == 200:
        m_id, color = line[1:]
        change_color(m_id, color)
        update_value(m_id)
    elif cmd == 300:
        m_id = line[1]
        print(node_dict[m_id].color)
    else:
        print(calculate_value(trees))
    # print("here: ", node_dict[root_id].value)