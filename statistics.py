import networkx as nx


# -------------------------------------------------
# Number of Nodes
# -------------------------------------------------

def get_number_of_nodes(G):
    """
    Returns total number of nodes.
    """
    return G.number_of_nodes()


# -------------------------------------------------
# Number of Edges
# -------------------------------------------------

def get_number_of_edges(G):
    """
    Returns total number of edges.
    """
    return G.number_of_edges()


# -------------------------------------------------
# Connected Components
# -------------------------------------------------

def get_connected_components(G):
    """
    Returns number of connected components.

    For directed graphs,
    weakly connected components are used.
    """

    if G.is_directed():
        return nx.number_weakly_connected_components(G)

    return nx.number_connected_components(G)


# -------------------------------------------------
# Graph Density
# -------------------------------------------------

def get_density(G):
    """
    Returns graph density.
    """

    return nx.density(G)


# -------------------------------------------------
# Average Degree
# -------------------------------------------------

def get_average_degree(G):
    """
    Returns average degree.
    """

    if G.number_of_nodes() == 0:
        return 0

    return (
        sum(dict(G.degree()).values())
        / G.number_of_nodes()
    )


# -------------------------------------------------
# Network Statistics
# -------------------------------------------------

def network_statistics(G):
    """
    Returns all graph statistics.
    """

    nodes = get_number_of_nodes(G)

    edges = get_number_of_edges(G)

    components = get_connected_components(G)

    density = get_density(G)

    average_degree = get_average_degree(G)

    graph_type = (
        "Directed"
        if G.is_directed()
        else "Undirected"
    )

    return {

        "Graph Type": graph_type,

        "Nodes": nodes,

        "Edges": edges,

        "Connected Components": components,

        "Density": round(
            density,
            4
        ),

        "Average Degree": round(
            average_degree,
            2
        )
    }


# -------------------------------------------------
# Display Statistics
# -------------------------------------------------

def print_statistics(stats):
    """
    Prints graph statistics.
    """

    print("\n========== NETWORK STATISTICS ==========\n")

    for key, value in stats.items():

        print(f"{key:<22}: {value}")

    print("\n========================================\n")


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    from data_loader import (
        load_data,
        preprocess_data,
        filter_by_time_window
    )

    from graph_builder import (
        build_temporal_graphs
    )

    # Load data
    df = load_data(
        "data/communication_data_5000_records.csv"
    )

    # Clean data
    df = preprocess_data(df)

    # Weekly graphs
    weekly = filter_by_time_window(
        df,
        "Weekly"
    )

    graphs = build_temporal_graphs(
        weekly,
        directed=True
    )

    first_week = list(graphs.keys())[0]

    print(f"Selected Week : {first_week}")

    G = graphs[first_week]

    stats = network_statistics(G)

    print_statistics(stats)