# Communication Network Analytics Platform

## Overview

The Communication Network Analytics Platform is a graph-based analytics application that analyzes temporal communication data to uncover interaction patterns, influential users, and hidden communities.

The project models communication records as weighted temporal graphs and provides interactive visualizations through a Streamlit dashboard.

---

## Features

- Temporal Graph Construction (Daily / Weekly / Monthly)
- Community Detection
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- PageRank Analysis
- Network Statistics
- Interactive Network Visualization
- Node Search
- Shortest Path Analysis

---

## Tech Stack

- Python
- Pandas
- NetworkX
- Plotly
- Streamlit
- Matplotlib

---

## Dataset

Synthetic Communication Dataset

- 5000 Communication Records
- 200 Users
- January – March 2025

Columns

- sender
- receiver
- timestamp
- weight

---

## Project Structure

communication-network-analysis/

```
data/
    communication_data_5000_records.csv

data_loader.py
graph_builder.py
analysis.py
statistics.py
user_features.py
app.py

requirements.txt
README.md
```

---

## Installation

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

## Dashboard Features

- Interactive Graph Visualization
- Community Coloring
- Network Statistics
- Top Influential Users
- Node Explorer
- Shortest Communication Path

---

## Future Improvements

- Louvain Community Detection
- Neo4j Integration
- Real-world Communication Dataset
- Edge Filtering
- Dynamic Community Evolution
