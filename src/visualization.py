# visualization.py
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(relationships, title):
    G = nx.Graph()
    scale_factor = 4
    node_size = 7000
    for char_pair, score in relationships.items():
        char1, char2 = char_pair
        G.add_node(char1)
        G.add_node(char2)
        G.add_edge(char1, char2, weight=score)
    pos = nx.spring_layout(G, k=0.1)
    edges = G.edges(data=True)
    edge_colors = ['green' if edge_data['weight'] > 0 else 'red' for _, _, edge_data in edges]
    edge_widths = [min(10, max(2, abs(edge_data['weight']) * scale_factor)) for _, _, edge_data in edges]
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, edge_color=edge_colors, width=edge_widths, with_labels=True,
            node_size=node_size, node_color='skyblue', font_size=12, font_color='black')
    plt.title(title)
    plt.show()
