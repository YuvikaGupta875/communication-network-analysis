import networkx as nx
import matplotlib.pyplot as plt

from data_loader import (
    load_data,
    preprocess_data,
    filter_by_time_window
)


# -------------------------------------------------
# Build Graph
# -------------------------------------------------

def build_graph(df, directed=True):
    """
    Build a weighted graph from the dataframe.

    Parameters:
        df : Communication dataframe
        directed : True -> DiGraph
                   False -> Graph

    Returns:
        NetworkX Graph
    """

    G = nx.DiGraph() if directed else nx.Graph()

    for _, row in df.iterrows():

        sender = row["sender"]
        receiver = row["receiver"]
        weight = row["weight"]

        # Aggregate communication weights
        if G.has_edge(sender, receiver):
            G[sender][receiver]["weight"] += weight
        else:
            G.add_edge(sender, receiver, weight=weight)

    return G


# -------------------------------------------------
# Build Temporal Graphs
# -------------------------------------------------

def build_temporal_graphs(grouped_data, directed=True):
    """
    Build graphs for each time window.

    Returns:
        {
            period : graph
        }
    """

    graphs = {}

    for period, data in grouped_data.items():
        graphs[period] = build_graph(data, directed)

    return graphs


# -------------------------------------------------
# Graph Summary
# -------------------------------------------------

def graph_summary(G):
    """
    Display basic graph statistics.
    """

    print("\n========== GRAPH SUMMARY ==========")

    print(f"Nodes                 : {G.number_of_nodes()}")
    print(f"Edges                 : {G.number_of_edges()}")
    print(f"Density               : {nx.density(G):.4f}")

    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
    print(f"Average Degree        : {avg_degree:.2f}")

    if G.is_directed():
        components = nx.number_weakly_connected_components(G)
    else:
        components = nx.number_connected_components(G)

    print(f"Connected Components  : {components}")

    print("===================================\n")


# -------------------------------------------------
# Top Degree Nodes
# -------------------------------------------------

def top_degree_nodes(G, top_n=5):
    """
    Display top nodes by degree.
    """

    print(f"Top {top_n} Nodes by Degree")

    degree = sorted(
        G.degree(),
        key=lambda x: x[1],
        reverse=True
    )

    for node, deg in degree[:top_n]:
        print(f"{node} : {deg}")

    print()


# -------------------------------------------------
# Draw Graph
# -------------------------------------------------

def draw_graph(G):
    """
    Draw communication graph.
    """

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(
        G,
        seed=42
    )

    edge_weights = [
        G[u][v]["weight"]
        for u, v in G.edges()
    ]

    # Normalize edge width
    max_weight = max(edge_weights) if edge_weights else 1

    edge_widths = [
        (w / max_weight) * 4
        for w in edge_weights
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=300
    )

    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        arrows=G.is_directed(),
        alpha=0.7
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=8
    )

    plt.title("Communication Network")

    plt.axis("off")

    plt.tight_layout()

    plt.show()


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    # Load dataset
    df = load_data("data/communication_data_5000_records.csv")

    # Preprocess
    df = preprocess_data(df)

    # Select time window
    weekly_data = filter_by_time_window(df, "Weekly")

    print(f"Total Weeks : {len(weekly_data)}")

    # Build graphs
    graphs = build_temporal_graphs(
        weekly_data,
        directed=True
    )

    # Select first graph
    first_week = list(graphs.keys())[0]

    print(f"Selected Week : {first_week}")

    G = graphs[first_week]

    # Graph summary
    graph_summary(G)

    # Top degree nodes
    top_degree_nodes(G)

    # Draw graph
    draw_graph(G)