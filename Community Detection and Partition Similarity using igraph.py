"""
.. _tutorials-evaluate-communities:

=============================
Partition Similarity Measure
=============================

This example shows how to evaluates the similarity between detected communities using partition similarity measures. 

"""
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt

#%%
# First, we generate a graph. We use a famous graph here for simplicity:
G = ig.Graph.Famous("Zachary")

#%%
# Louvain method is a popular modularity-based approach for detecting communities in a network.
louvain_communities = G.community_multilevel()

#%%
# Edge betweenness is a standard way to detect communities. We then covert into
# a :class:`igraph.VertexClustering` object for subsequent ease of use:
edge_betweenness_communities = G.community_edge_betweenness().as_clustering()

#%%
# Fast greedy is a hierarchical agglomerative approach that merges nodes to optimize modularity and is converted into 
# a :class:`igraph.VertexClustering` object.
fast_greedy_communities = G.community_fastgreedy().as_clustering()

#%%
# Next, we color each vertex and edge based on its community membership:
def get_cluster_colors(communities):
    num_clusters = len(set(communities.membership))
    colors = plt.cm.get_cmap("tab10", num_clusters)  # Use 'tab10' colormap
    return [colors(i)[:3] for i in communities.membership]

#%%
# Plots the graph with nodes colored based on their community assignments for clear visualization.
def plot_graph(graph, communities, title):
    node_colors = get_cluster_colors(communities)
    fig, ax = plt.subplots(figsize=(7, 5))
    ig.plot(graph, target=ax, vertex_color=node_colors, bbox=(300, 300), margin=50)
    plt.title(title)
    plt.show()

plot_graph(G, louvain_communities, "Louvain Community Detection")
plot_graph(G, edge_betweenness_communities, "Edge Betweenness Community Detection")
plot_graph(G, fast_greedy_communities, "Fast Greedy Community Detection")

#%%
# Extracts community memberships as a list of cluster assignments for each node.
def get_membership(communities):
    return communities.membership
  
#%%
# Computes similarity measures (NMI, VI, RI) to compare detected community structures across methods.
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

#%%
# Last, we print the results
print("\nPartition Similarity Measures:")
print(f"NMI (Louvain vs Edge Betweenness): {nmi_eb_louvain:.4f}")
print(f"NMI (Louvain vs Fast Greedy): {nmi_fg_louvain:.4f}")

print(f"VI (Louvain vs Edge Betweenness): {vi_eb_louvain:.4f}")
print(f"VI (Louvain vs Fast Greedy): {vi_fg_louvain:.4f}")
print(f"Rand Index (Louvain vs Edge Betweenness): {ri_eb_louvain:.4f}")
print(f"Rand Index (Louvain vs Fast Greedy): {ri_fg_louvain:.4f}")


#%%
#This project systematically analyzes community detection algorithms and evaluates their performance using partition similarity metrics. 

