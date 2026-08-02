 # Streamlit app

 
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from data_loader import load_data, preprocess_data, filter_by_time_window
from graph_builder import build_temporal_graphs
from analysis import (
    degree_centrality_analysis,
    betweenness_centrality_analysis,
    closeness_centrality_analysis,
    pagerank_analysis,
    community_detection,
    community_map,
    top_nodes
)
from statistics import network_statistics
from user_features import node_details, shortest_path

st.set_page_config(page_title="Communication Network Analytics", layout="wide")
st.markdown("""
<style>

.main {
    background-color:  #2B2D31;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stMetricValue"] {
    color: #38bdf8;
    font-size: 30px;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: white;
}

div[data-testid="stMetric"]{
    background-color:#1e293b;
    border:1px solid #334155;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.3);
}

.stDataFrame{
    border-radius:12px;
}

.stButton>button{
    background:#2563eb;
    color:white;
    border-radius:10px;
    border:none;
}

.stButton>button:hover{
    background:#1d4ed8;
}

</style>
""", unsafe_allow_html=True)
st.title("Communication Network Analytics Platform")


# Sidebar
st.sidebar.header("Controls")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
window = st.sidebar.selectbox("Time Window", ["Daily", "Weekly", "Monthly"])

if uploaded:
    df = load_data(uploaded)
else:
    df = load_data("data/communication_data_5000_records.csv")

df = preprocess_data(df)
groups = filter_by_time_window(df, window)
periods = list(groups.keys())
st.caption(
    f"{len(df):,} communication records | {len(periods)} time windows"
)

selected = st.sidebar.selectbox("Select Period", periods)
graphs = build_temporal_graphs(groups, directed=True)
G = graphs[selected]

# Analysis
degree = degree_centrality_analysis(G)
between = betweenness_centrality_analysis(G)
close = closeness_centrality_analysis(G)
rank = pagerank_analysis(G)
communities = community_detection(G)
cmap = community_map(communities)
stats = network_statistics(G)

# Statistics
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Nodes", stats["Nodes"])
c2.metric("Edges", stats["Edges"])
c3.metric("Density", stats["Density"])
c4.metric("Components", stats["Connected Components"])
c5.metric("Avg Degree", stats["Average Degree"])

# Plotly graph
pos = nx.spring_layout(G, seed=42)
edge_x=[]; edge_y=[]
for u,v in G.edges():
    x0,y0=pos[u]; x1,y1=pos[v]
    edge_x += [x0,x1,None]
    edge_y += [y0,y1,None]

edge_trace = go.Scatter(
    x=edge_x,y=edge_y,
    mode="lines",
    line=dict(width=0.6,color="#888"),
    hoverinfo="none"
)

palette=["red","blue","green","orange","purple","cyan","magenta","gold","brown","pink"]

node_x=[]; node_y=[]; colors=[]; texts=[]
for node in G.nodes():
    x,y=pos[node]
    node_x.append(x); node_y.append(y)
    cid=cmap.get(node,1)
    colors.append(palette[(cid-1)%len(palette)])
    texts.append(f"{node}<br>Community {cid}")

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=[n for n in G.nodes()],
    textposition="top center",
    hovertext=texts,
    hoverinfo="text",
    marker=dict(size=10,color=colors,line=dict(width=1,color="black"))
)

fig = go.Figure(data=[edge_trace,node_trace])
fig.update_layout(
    title=f"Communication Network ({selected})",
    showlegend=False,
    margin=dict(l=20,r=20,t=40,b=20),
    xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
    yaxis=dict(showgrid=False,zeroline=False,showticklabels=False)
)
st.plotly_chart(fig, use_container_width=True)

# Centrality tables
st.header("Top 10 Central Nodes")
tabs = st.tabs(["Degree","Betweenness","Closeness","PageRank"])

metrics = [
    ("Degree", degree),
    ("Betweenness", between),
    ("Closeness", close),
    ("PageRank", rank)
]

for tab,(name,data) in zip(tabs,metrics):
    with tab:
        df_top = pd.DataFrame(top_nodes(data,10), columns=["Node",name])
        st.dataframe(df_top, use_container_width=True)

# Node search
st.header("Node Search")
node = st.text_input("Enter Node ID (e.g. U025)")
if st.button("Search"):
    details = node_details(G,node,degree,between,close,rank,cmap)
    if details is None:
        st.error("Node not found")
    else:
        st.json(details)

# Shortest path
st.header("Shortest Path")
col1,col2 = st.columns(2)
src = col1.text_input("Source Node").strip().upper()
dst = col2.text_input("Destination Node").strip().upper()
if st.button("Find Shortest Path"):
    res = shortest_path(G,src,dst)
    if res is None:
        st.error("No path found.")
    else:
        st.success(" -> ".join(res["Path"]))
        st.write(f"Path Length: {res['Length']}")
        