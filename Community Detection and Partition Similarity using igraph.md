# Overview

This project demonstrates the implementation of various **community detection algorithms** using the **igraph** library in Python. It evaluates the similarity between detected communities using partition similarity measures. 

# Installation

Ensure you have the required dependencies installed:
`pip install igraph numpy matplotlib`

- igraph: A Python library for creating and analyzing graphs and network structures.

- numpy: A powerful numerical computing library for handling arrays and mathematical operations.

- matplotlib: A plotting library for creating static, animated, and interactive visualizations.

# 1. Follow any one method to load graph data

### 1.1 Generate a Random Graph
```
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt

# Generate a Random Graph
G = ig.Graph.Erdos_Renyi(n=30, m=50)  # 30 nodes, 50 edges
G.vs["label"] = [str(i) for i in range(G.vcount())]  # Assign labels
```

### 1.2 Load the Karate Club Graph (Famous Graph)
```
G = ig.Graph.Famous("Zachary")
```

### 1.3 Load a Graph from an Adjacency Matrix
```
adj_matrix = np.random.randint(0, 2, (10, 10))  # Random adjacency matrix
G = ig.Graph.Adjacency((adj_matrix > 0).tolist())
```

### 1.4 Load a Graph from an Edge List
```
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
G = ig.Graph(edges=edges, directed=False)
```
### 1.5 Load a Graph from a File (Edge List Format)
```
G = ig.Graph.Read_Edgelist("graph_edges.txt", directed=False)
````

### 1.6 Load a Graph from a GraphML File
```
G = ig.Graph.Read_GraphML("network.graphml")
```

## Famous Graphs supported by igraph

| Graph Name                | Description |
|---------------------------|------------|
| Zachary            | Social network of friendships between 34 members of a karate club. |
| Dolphins   | Social network of bottlenose dolphins, based on frequent association. |
| Les Miserables	        | Co-occurrence network of characters in Les Misérables (based on book scenes). |
| Polbooks	| Network of books about US politics sold on Amazon, where edges indicate frequent co-purchases. |
| LCF | Graph	A class of circulant graphs defined by n, d, and k. |
| Florentine Families	| A marriage and business network of Renaissance Florentine families.|

# 2. Apply Community Detection Methods
The following algorithms are applied:

- **Louvain Method** (Modularity optimization):

  A hierarchical clustering algorithm that optimizes modularity to detect 
  communities efficiently in large networks. The Louvain method works by repeating two phases. In phase one, nodes are sorted into communities based on how the modularity of the graph changes when a node moves communities. In phase two, the graph is reinterpreted so that communities are seen as individual nodes.

  The Louvain method is assumed to have a time complexity of $O(n\log(n))$
  
- **Edge Betweenness Method** (Girvan-Newman):

  The Girvan–Newman algorithm detects communities by progressively removing edges from the original network. The connected components of the remaining network are the communities. Instead of trying to construct a measure that tells us which edges are the most central to communities, the Girvan–Newman algorithm focuses on edges that are most likely "between" communities.
  
  The algorithm's steps for community detection are summarized below
  
  - The betweenness of all existing edges in the network is calculated first.
  - The edge(s) with the highest betweenness are removed.
  - The betweenness of all edges affected by the removal is recalculated.
  - Steps 2 and 3 are repeated until no edges remain.


- **Fast Greedy Method** (Agglomerative clustering):

  Uses hierarchical agglomerative clustering to merge nodes and optimize modularity. This is a "bottom-up" approach: Each observation starts in its own cluster, and pairs of clusters are merged as one moves up the hierarchy.

```
# Louvain Method
louvain_communities = G.community_multilevel()

# Edge Betweenness Method
edge_betweenness_communities = G.community_edge_betweenness().as_clustering()

# Fast Greedy Method
fast_greedy_communities = G.community_fastgreedy().as_clustering()
```

# 3. Assign Colors for Clusters
A function is created to assign distinct colors to each community.
```
def get_cluster_colors(communities):
    num_clusters = len(set(communities.membership))
    colors = plt.cm.get_cmap("tab10", num_clusters)  # Use 'tab10' colormap
    return [colors(i)[:3] for i in communities.membership]
```

# 4. Visualizing Detected Communities
Each graph is plotted with distinct community coloring.
```
def plot_graph(graph, communities, title):
    node_colors = get_cluster_colors(communities)
    fig, ax = plt.subplots(figsize=(7, 5))
    ig.plot(graph, target=ax, vertex_color=node_colors, bbox=(300, 300), margin=50)
    plt.title(title)
    plt.show()

plot_graph(G, louvain_communities, "Louvain Community Detection")
plot_graph(G, edge_betweenness_communities, "Edge Betweenness Community Detection")
plot_graph(G, fast_greedy_communities, "Fast Greedy Community Detection")
```

# 5. Partition Similarity Measures

To compare different community detection methods, we compute Normalized Mutual Information (NMI), Variation of Information (VI), and Rand Index (RI).

### Defination of H(X), H(X|Y) and I(X,Y)


- Mutual information
  
  $I(X, Y) = H(X) - H(X|Y)$

- Shannon entropy of X
  
  $H(X) = - \sum_{x} P(x) \log P(x)$

- Conditional entropy of X given Y
  
  $H(X|Y) = - \sum_{x,y} P(x,y) \log P(x|y)$

## Normalized Mutual Information (NMI)

Measures the mutual dependence between two partitions, normalized to [0,1].

![Screenshot 2025-03-24 at 11 25 48 PM](https://github.com/user-attachments/assets/3d50d8be-906a-40cb-9739-7efcfc060e48)


## Variation of Information (VI)

Measures the distance between two partitions based on entropy.

![Screenshot 2025-03-24 at 11 20 17 PM](https://github.com/user-attachments/assets/3f8c24cd-ac78-46df-bb2d-747685d6b7d3)


## Rand Index (RI)

Evaluates the similarity between two partitions based on pairwise agreements.

![Screenshot 2025-03-24 at 11 17 37 PM](https://github.com/user-attachments/assets/e3ccfe0e-4179-4a7d-ae06-80e829d67bfe)

- a11 indicate the number of pairs of vertices which are in the same community in both partitions.
- a01 (a10) the number of pairs of elements which are in the same community in X (Y) and in different communities in Y (X).
- a00 the number of pairs of vertices that are in different communities in both partitions. 

```
def get_membership(communities):
    return communities.membership

# Compute Similarity Measures
louvain_membership = get_membership(louvain_communities)
edge_betweenness_membership = get_membership(edge_betweenness_communities)
fast_greedy_membership = get_membership(fast_greedy_communities)

# Normalized Mutual Information (NMI)
nmi_eb_louvain = ig.compare_communities(louvain_membership, edge_betweenness_membership, method="nmi")
nmi_fg_louvain = ig.compare_communities(louvain_membership, fast_greedy_membership, method="nmi")

# Variation of Information (VI)
vi_eb_louvain = ig.compare_communities(louvain_membership, edge_betweenness_membership, method="vi")
vi_fg_louvain = ig.compare_communities(louvain_membership, fast_greedy_membership, method="vi")

# Rand Index (RI)
ri_eb_louvain = ig.compare_communities(louvain_membership, edge_betweenness_membership, method="rand")
ri_fg_louvain = ig.compare_communities(louvain_membership, fast_greedy_membership, method="rand")
```

# 6. Results
```
print("\nPartition Similarity Measures:")
print(f"NMI (Louvain vs Edge Betweenness): {nmi_eb_louvain:.4f}")
print(f"NMI (Louvain vs Fast Greedy): {nmi_fg_louvain:.4f}")

print(f"VI (Louvain vs Edge Betweenness): {vi_eb_louvain:.4f}")
print(f"VI (Louvain vs Fast Greedy): {vi_fg_louvain:.4f}")
print(f"Rand Index (Louvain vs Edge Betweenness): {ri_eb_louvain:.4f}")
print(f"Rand Index (Louvain vs Fast Greedy): {ri_fg_louvain:.4f}")
```

# 7. Conclusion
This project systematically analyzes community detection algorithms and evaluates their performance using partition similarity metrics. 
