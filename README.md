# Community Detection and Clustering using igraph
This repository demonstrates various community detection and clustering techniques using the igraph library in Python. The focus is on partition similarity measures, consensus clustering, and hierarchical clustering.

## Partition Similarity Measures

Partition similarity measures help compare different community detection methods. The igraph package provides various similarity metrics to evaluate clusterings.

### Functions Used:

- `igraph.compare_communities(comm1, comm2, method="nmi") `→ Computes Normalized Mutual Information (NMI) to compare two community partitions.

- `igraph.compare_communities(comm1, comm2, method="adjusted_rand")` → Computes the Adjusted Rand Index (ARI) for partition similarity.

- `igraph.compare_communities(comm1, comm2, method="vi")` → Computes the Variation of Information (VI) between two clusterings.

## Consensus Clustering

Consensus clustering aggregates multiple clustering results to form a robust partitioning. It combines different community detection methods to enhance clustering stability.

### Functions Used:

- Applies four community detection algorithms (Louvain, Edge Betweenness, Fast Greedy, Walktrap) to Zachary's Karate Club Graph.

- Computes a consensus matrix, where each entry (i,j) represents the fraction of partitions where nodes i and j belong to the same community.

- Thresholding: Removes weak links in the consensus matrix.

- Applies hierarchical clustering (using scipy.linkage and fcluster) to determine final cluster assignments.

- Assigns colors based on the final clusters and plots:

## Hierarchical Clustering

Hierarchical clustering builds a hierarchy of clusters using different linkage strategies.

### Functions Used:

- `G.community_fastgreedy()` → Implements agglomerative clustering based on modularity optimization.

- `dendrogram.as_clustering(k)` → Converts dendrogram into k clusters.


# References Used:
https://igraph.org/c/html/latest/igraph-Community.html

[1608.00163v2.pdf](https://github.com/user-attachments/files/19415758/160

[0906.0612v2.pdf](https://github.com/user-attachments/files/19415761/0906.0612v2.pdf)
8.00163v2.pdf)

