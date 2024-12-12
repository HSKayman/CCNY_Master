import networkx as nx
import matplotlib.pyplot as plt
from random import shuffle, choice
import time

class ZKp3Coloring:
    def __init__(self):

        self.colors = {1: 'red', 2: 'green', 3: 'blue'}
        self.graph = nx.Graph()
        self.real_coloring = {}
        self.current_permuted_coloring = {}
        
    def create_sample_graph(self):
        self.graph.clear()
       
        edges = [('A','B'), ('B','C'), ('C','D'), ('D','E'), ('E','F'), ('F','A'),  
                 ('G','H'), ('H','I'), ('I','G'), ('A','G'), ('B','H'), ('C','I'), 
                 ('J','A'), ('J','F'), ('K','B'), ('K','C'), ('K','H'), ('L','D'), 
                 ('L','E'), ('L','I'), ('F','E'), ('D','C')  
        ]
        self.graph.add_edges_from(edges)
        
        self.real_coloring = {
            'A': 1, 'B': 2, 'C': 3,
            'D': 1, 'E': 2, 'F': 3,
            'G': 2, 'H': 3, 'I': 1,
            'J': 2, 'K': 1, 'L': 3
        }
        
    def display_graph(self, coloring=None):
        plt.clf()
        pos = nx.spring_layout(self.graph)
        
        if coloring:
            colors = [self.colors[coloring[node]] for node in self.graph.nodes()]
            nx.draw(self.graph, pos, with_labels=True, node_color=colors, 
                   node_size=500, font_size=16, font_weight='bold')
        else:
            nx.draw(self.graph, pos, with_labels=True, node_size=500, 
                   font_size=16, font_weight='bold')
        
        plt.show()

    def permute_colors(self):

        color_permutation = list(self.colors.keys())
        shuffle(color_permutation)
        
        self.current_permuted_coloring = {}
        for vertex in self.real_coloring:
            old_color = self.real_coloring[vertex]
            self.current_permuted_coloring[vertex] = color_permutation[old_color - 1]
        
        return self.current_permuted_coloring

    def verify_edge(self, edge):

        v1, v2 = edge
        return self.current_permuted_coloring[v1] != self.current_permuted_coloring[v2]

zkp = ZKp3Coloring()
zkp.create_sample_graph()

print("\nInitial graph (no coloring revealed):")
zkp.display_graph()

rounds = int(input("\nHow many verification rounds would you like to perform? "))

for round_num in range(rounds):
    print(f"\nRound {round_num + 1}:")
    print("Prover is creating a new random permutation of colors...")
    zkp.permute_colors()
    
    # Let verifier (user) choose an edge
    edges = list(zkp.graph.edges())
    print("\nAvailable edges:")
    for i, edge in enumerate(edges):
        print(f"{i+1}: {edge}")
    
    while True:
        try:
            choice = int(input("\nSelect an edge number to verify: ")) - 1
            if 0 <= choice < len(edges):
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    selected_edge = edges[choice]
    print(f"\nVerifying edge {selected_edge}...")
    time.sleep(1)
    
    if zkp.verify_edge(selected_edge):
        print("VERIFIED: The endpoints have different colors!")
        # Show only the selected edge's vertices with their colors
        temp_coloring = {v: zkp.current_permuted_coloring[v] if v in selected_edge else None 
                        for v in zkp.graph.nodes()}
        print(f"Colors of vertices {selected_edge[0]}: {zkp.colors[zkp.current_permuted_coloring[selected_edge[0]]]},"
                f" {selected_edge[1]}: {zkp.colors[zkp.current_permuted_coloring[selected_edge[1]]]}")
    else:
        print("✗ FAILED: The endpoints have the same color!")
        
    
    input("\nPress Enter to continue to next round...")

print("\nAll rounds completed successfully!")
print("The verifier is convinced that the graph is 3-colorable,")
print("but learned nothing about the actual coloring!")

