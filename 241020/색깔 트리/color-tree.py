class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        # self.diff_color = set()
        self.children = []
        # self.diff_color.add(color)
        self.value = 1

def getValue(id):
    node = node_dict[id]       
    curr_color_list = [0] * 5
    curr_color_list[node.color - 1] = 1
    value = 0
    for c in node.children:
        c_val, c_colorlist = getValue(c)
        for i in range(5):
            curr_color_list[i] += c_colorlist[i]
        value += c_val
    curr_val = sum([1 for c in curr_color_list if c > 0])
    value += curr_val**2
    #print(f"{id}: {curr_val}")
    return value, curr_color_list
    
        
        
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
    #update_value(m_id)

def change_color(m_id, color):
    node = node_dict[m_id]
    node.color = color
    # node.diff_color = set([color])
    node.value = 1
    for child in node.children:
        change_color(child, color)

def calculate_value(root_id):
    total = 0
    for root_id in trees:
        val, _ =  getValue(root_id)
        total += val
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
        #print(node_dict)
    elif cmd == 200:
        m_id, color = line[1:]
        change_color(m_id, color)
        #update_value(m_id)
    elif cmd == 300:
        m_id = line[1]
        print(node_dict[m_id].color)
    else:
        print(calculate_value(trees))
    # print("here: ", node_dict[root_id].value)