import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


# -------------------------------------------------
# Degree Centrality
# -------------------------------------------------

def degree_centrality_analysis(G):
    """
    Compute Degree Centrality.
    """
    return nx.degree_centrality(G)


# -------------------------------------------------
# Betweenness Centrality
# -------------------------------------------------

def betweenness_centrality_analysis(G):
    """
    Compute Betweenness Centrality.
    """
    return nx.betweenness_centrality(
        G,
        weight="weight"
    )


# -------------------------------------------------
# Closeness Centrality
# -------------------------------------------------

def closeness_centrality_analysis(G):
    """
    Compute Closeness Centrality.
    """
    return nx.closeness_centrality(G)


# -------------------------------------------------
# PageRank
# -------------------------------------------------

def pagerank_analysis(G):
    """
    Compute PageRank.
    """
    return nx.pagerank(
        G,
        weight="weight"
    )


# -------------------------------------------------
# Community Detection
# -------------------------------------------------

def community_detection(G):
    """
    Detect communities using Greedy Modularity.
    """

    if G.is_directed():
        H = G.to_undirected()
    else:
        H = G

    return list(greedy_modularity_communities(H))


# -------------------------------------------------
# Community Summary
# -------------------------------------------------

def community_summary(communities):
    """
    Display detected communities.
    """

    print("\n========= COMMUNITY DETECTION =========")

    print(f"Total Communities : {len(communities)}\n")

    for i, community in enumerate(communities, start=1):

        print(
            f"Community {i:<2}: {len(community)} nodes"
        )

    print()


# -------------------------------------------------
# Community Map
# -------------------------------------------------

def community_map(communities):
    """
    Returns:

    {
        node : community_id
    }
    """

    mapping = {}

    for idx, community in enumerate(communities, start=1):

        for node in community:

            mapping[node] = idx

    return mapping


# -------------------------------------------------
# Top N Nodes
# -------------------------------------------------

def top_nodes(scores, top_n=10):
    """
    Returns top N nodes.
    """

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]


# -------------------------------------------------
# Display Top Nodes
# -------------------------------------------------

def print_top(scores, title):
    """
    Display ranking.
    """

    print(f"\n========== {title.upper()} ==========\n")

    for node, score in scores:

        print(f"{node:<8} {score:.4f}")

    print()


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

    # -------------------------
    # Centrality Metrics
    # -------------------------

    degree = degree_centrality_analysis(G)
    between = betweenness_centrality_analysis(G)
    close = closeness_centrality_analysis(G)
    rank = pagerank_analysis(G)

    # -------------------------
    # Print Rankings
    # -------------------------

    print_top(
        top_nodes(degree),
        "Degree Centrality"
    )

    print_top(
        top_nodes(between),
        "Betweenness Centrality"
    )

    print_top(
        top_nodes(close),
        "Closeness Centrality"
    )

    print_top(
        top_nodes(rank),
        "PageRank"
    )

    # -------------------------
    # Communities
    # -------------------------

    communities = community_detection(G)

    community_summary(communities)

    node_to_community = community_map(
        communities
    )

    print("Sample Community Mapping\n")

    for node, community in list(node_to_community.items())[:10]:

        print(f"{node} -> Community {community}")