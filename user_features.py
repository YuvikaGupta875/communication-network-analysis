import networkx as nx


# -------------------------------------------------
# Search Node
# -------------------------------------------------

def search_node(G, node):
    """
    Returns True if node exists.
    """
    return node in G


# -------------------------------------------------
# Node Details
# -------------------------------------------------

def node_details(
    G,
    node,
    degree,
    betweenness,
    closeness,
    pagerank,
    community_map
):
    """
    Returns all information about a node.
    """

    if node not in G:
        return None

    return {

        "Node": node,

        "Degree": G.degree(node),

        "Neighbors": list(G.neighbors(node)),

        "Degree Centrality":
            round(degree[node], 4),

        "Betweenness Centrality":
            round(betweenness[node], 4),

        "Closeness Centrality":
            round(closeness[node], 4),

        "PageRank":
            round(pagerank[node], 4),

        "Community":
            community_map.get(node, "N/A")
    }


# -------------------------------------------------
# Display Node
# -------------------------------------------------

def print_node_details(details):
    """
    Displays node information.
    """

    if details is None:

        print("\nNode not found.\n")

        return

    print("\n========== NODE DETAILS ==========\n")

    for key, value in details.items():

        print(f"{key:<25}: {value}")

    print("\n==================================\n")


# -------------------------------------------------
# Shortest Path
# -------------------------------------------------

def shortest_path(G, source, target):
    """
    Returns the shortest communication path.

    Uses an undirected graph so that
    communication chains can be discovered
    regardless of message direction.
    """

    # Clean user input
    source = source.strip().upper()
    target = target.strip().upper()

    # Convert directed graph to undirected
    H = G.to_undirected()

    # Check whether nodes exist
    if source not in H:
        return None

    if target not in H:
        return None

    try:

        path = nx.shortest_path(
            H,
            source=source,
            target=target
        )

        return {

            "Path": path,

            "Length": len(path) - 1
        }

    except nx.NetworkXNoPath:

        return None


# -------------------------------------------------
# Display Shortest Path
# -------------------------------------------------

def print_shortest_path(result):

    print("\n========== SHORTEST PATH ==========\n")

    if result is None:

        print("No path found.")

    else:

        print(
            " -> ".join(result["Path"])
        )

        print(
            f"\nPath Length : {result['Length']}"
        )

    print("\n===================================\n")


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

    from analysis import (

        degree_centrality_analysis,

        betweenness_centrality_analysis,

        closeness_centrality_analysis,

        pagerank_analysis,

        community_detection,

        community_map
    )

    # Load data
    df = load_data(
        "data/communication_data_5000_records.csv"
    )

    df = preprocess_data(df)

    weekly = filter_by_time_window(
        df,
        "Weekly"
    )

    graphs = build_temporal_graphs(
        weekly,
        directed=True
    )

    first_week = list(graphs.keys())[0]

    G = graphs[first_week]

    # Compute once

    degree = degree_centrality_analysis(G)

    between = betweenness_centrality_analysis(G)

    close = closeness_centrality_analysis(G)

    rank = pagerank_analysis(G)

    communities = community_detection(G)

    mapping = community_map(
        communities
    )

    # Node Search

    node = "U025"

    details = node_details(
        G,
        node,
        degree,
        between,
        close,
        rank,
        mapping
    )

    print_node_details(details)

    # Shortest Path

    result = shortest_path(
        G,
        "U025",
        "U150"
    )

    print_shortest_path(result)