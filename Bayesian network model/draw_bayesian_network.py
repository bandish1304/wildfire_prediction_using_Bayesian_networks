import matplotlib.pyplot as plt
import networkx as nx

def draw_bayesian_network():
    G = nx.DiGraph()
    G.add_node('TAVG_CAT')
    G.add_node('TMAX_CAT')
    G.add_node('TMIN_CAT')
    G.add_node('PRCP_CAT')
    G.add_node('SEASON')
    G.add_node('WILDFIRE_OCCURRENCE')
    G.add_edge('TAVG_CAT', 'WILDFIRE_OCCURRENCE')
    G.add_edge('TMAX_CAT', 'WILDFIRE_OCCURRENCE')
    G.add_edge('TMIN_CAT', 'WILDFIRE_OCCURRENCE')
    G.add_edge('PRCP_CAT', 'WILDFIRE_OCCURRENCE')
    G.add_edge('SEASON', 'WILDFIRE_OCCURRENCE')
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', arrowsize=20)
    plt.title('Bayesian Network Structure for Wildfire Prediction')
    plt.show()

if __name__ == "__main__":
    draw_bayesian_network()
