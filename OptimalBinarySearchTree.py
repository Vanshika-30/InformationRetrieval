"""
    Name: Vanshika Jain
    Roll No.: BT18CSE107
    prerequiste - conda install ghraviz
"""
from collections import defaultdict
import graphviz

# For making tree
class Node:
    def __init__(self, id, freq=0, left=None, right=None):
        self.id = id
        self.freq = freq
        self.left = left
        self.right = right


# For OBST
class OBST:
    def __init__(self, root = None):
        self.root = None
        self.cost = defaultdict(dict)    # cost matrix
        self.weight = defaultdict(dict)  # weight matrix
        self.r_mat = defaultdict(dict)   # root matrix

    # Compute cost based on frequency and find optimal tree
    def compute_cost_weight(self, adj):
        no_of_keys = len(adj["key"])

        for i in range(0, no_of_keys + 1):
            self.weight[i][i] = 0
            self.r_mat[i][i] = 0
            
            for j in range(i + 1, no_of_keys + 1):
                self.weight[i][j] = self.weight[i][j - 1] + adj["val"][j - 1]
        
        for i in range(0, no_of_keys + 1):
            self.cost[i][i] = self.weight[i][i]
        
        for i in range(0, no_of_keys):
            j = i + 1
            self.cost[i][j] = self.cost[i][i] + self.cost[j][j] + self.weight[i][j]
            self.r_mat[i][j] = j
        
        for h in range(2, no_of_keys + 1):
            for i in range(0, no_of_keys - h + 1):
                j = i + h
                temp = self.r_mat[i][j - 1]
                min_val = self.cost[i][temp - 1] + self.cost[temp][j]
                for k in range(temp + 1, self.r_mat[i + 1][j] + 1):
                    x = self.cost[i][k - 1] + self.cost[k][j]
                    if x < min_val:
                        temp = k
                        min_val = x
                self.cost[i][j] = self.weight[i][j] + min_val
                self.r_mat[i][j] = temp
        print(
            f"\nTotal cost = {self.cost[0][no_of_keys]} and Total weight = {self.weight[0][no_of_keys]} "
        )
        print(
            f"\n The cost per weight ratio = {self.cost[0][no_of_keys]/self.weight[0][no_of_keys]}"
        )

    # Construct the tree
    def construct_obst(self, adj, i, j):
        if i == j:
            return None
        temp = Node(adj["key"][self.r_mat[i][j] - 1], adj["val"][self.r_mat[i][j] - 1])
        temp.left = self.construct_obst(adj, i, self.r_mat[i][j] - 1)
        temp.right = self.construct_obst(adj, self.r_mat[i][j], j)
        return temp

# Displaying
def display(root, parent, li):
    if root:
        display(root.right, root, li)
        li.append((root, parent))
        display(root.left, root, li)

if __name__ == "__main__":

    # conda install graphviz to get proper image of the final tree 

    print("Reading from pgr1.txt")
    with open("prg1.txt", "r") as f:
        lines = f.readlines()
    adj = {}
    for i in range(len(lines)):
        line = lines[i]
        val = line.split()
        for word in val:
            word = word.lower()
            if word in adj.keys():
                adj[word] += 1
            else:
                adj[word] = 1
    
    # Creating key and value pair of word and its frequency
    key_val_list = {
        "key": [x for x in sorted(adj)],
        "val": [adj[x] for x in sorted(adj)],
    }

    # Creating OBST
    root = OBST()
    root.compute_cost_weight(key_val_list)
    root.root = root.construct_obst(key_val_list, 0, len(key_val_list["key"]))
    li = []
    
    # Temporary root node
    t = Node("#", 0) 

    # Displaying the tree formed
    display(root.root, t, li) 
    
    node_label = {}
    j = 0
    for i in li:
        v1 = i[0].id + " " + str(i[0].freq)
        v2 = i[1].id + " " + str(i[1].freq)
        if v1 not in node_label.values():
            node_label[j] = (v1)
            j+=1
        if v2 not in node_label.values():
            node_label[j] = (v2)
            j+=1

    G = graphviz.Digraph()

    for i in li:
        v1 = i[0].id + " " + str(i[0].freq)
        v2 = i[1].id + " " + str(i[1].freq)
        G.edge(v2, v1)
    
    G.view()


   


