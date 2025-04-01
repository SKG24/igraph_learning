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

## Animation
```
# Add Zachary's original factions manually
    faction_mapping = {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 0,
        10: 0, 11: 0, 12: 0, 13: 0, 14: 1, 15: 1, 16: 0, 17: 0, 18: 1, 19: 0,
        20: 1, 21: 0, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1,
        30: 1, 31: 1, 32: 1, 33: 1
    }
    graph.vs["Faction"] = [faction_mapping[i] for i in range(len(graph.vs))]
    
    # Configuration
    cmap = ListedColormap(["#1f77b4", "#ff7f0e"])  # Two colors for factions
    cluster_cmap = ListedColormap(["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                                 "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"])
    
    layout = graph.layout("fruchterman_reingold")
    positions = np.array(layout.coords)

    # Clustering algorithms
    clustering_algorithms = {
        "Fastgreedy": graph.community_fastgreedy().as_clustering(),
        "Walktrap": graph.community_walktrap().as_clustering(),
        "Louvain": graph.community_multilevel(),
        "LabelProp": graph.community_label_propagation()
    }
    
    # Precompute cluster metrics
    cluster_data = {}
    for name, clusters in clustering_algorithms.items():
        cluster_data[name] = {
            "clusters": clusters,
            "modularity": graph.modularity(clusters.membership),
            "num_clusters": len(clusters),
            "ground_truth_accuracy": np.mean(np.array(clusters.membership) == np.array(graph.vs["Faction"]))
        }
```
```
# Phase: Algorithm visualization
        elif frame < discovery_duration + len(clustering_algorithms)*algorithm_duration:
            phase_frame = frame - discovery_duration
            alg_index = phase_frame // algorithm_duration
            if alg_index < len(clustering_algorithms):
                alg_name = list(clustering_algorithms.keys())[alg_index]
                clusters = cluster_data[alg_name]["clusters"]
                edge_progress = min(phase_frame % algorithm_duration, len(graph.es))
                
                # Update node colors based on clustering
                node_colors = [cluster_cmap(c % 8) for c in clusters.membership]
                
                # Update edges
                for i, edge in enumerate(graph.es):
                    if i < edge_progress:
                        if clusters.membership[edge.source] == clusters.membership[edge.target]:
                            edge_colors[i] = cluster_cmap(clusters.membership[edge.source] % 8)
                            edge_widths[i] = 2.5
                        else:
                            edge_colors[i] = "gray"
                            edge_widths[i] = 0.8
                            edge_styles[i] = "dashed"
                
                # Highlight key nodes
                node_colors[0] = "black"  # Instructor
                node_colors[33] = "white"  # President
                
                # Add annotations
                algorithm_text = get_algorithm_description(alg_name)
                metrics_text = (f"Modularity: {cluster_data[alg_name]['modularity']:.2f}\n"
                               f"Clusters: {cluster_data[alg_name]['num_clusters']}\n"
                               f"Accuracy: {cluster_data[alg_name]['ground_truth_accuracy']:.1%}")
                ax.set_title(f"{alg_name} Clustering Process", pad=20)
```
```
# Draw network elements
        if frame < total_frames - comparison_duration:
            # Draw edges
            for i, edge in enumerate(graph.es):
                if edge_colors[i] != "white":  # Skip hidden edges
                    ax.plot(
                        [positions[edge.source][0], positions[edge.target][0]],
                        [positions[edge.source][1], positions[edge.target][1]],
                        color=edge_colors[i],
                        linewidth=edge_widths[i],
                        linestyle=edge_styles[i],
                        alpha=0.7,
                        zorder=1
                    )
            
            # Draw nodes
            sc = ax.scatter(
                positions[:,0], positions[:,1],
                c=node_colors,
                s=200,
                edgecolors="black",
                linewidths=1.5,
                zorder=2
            )
```
```
# Create and save animation
ani = animation.FuncAnimation(
        fig,
        update,
        frames=total_frames,
        interval=1000//fps  # Convert fps to interval in ms
    )
    
    try:
        writer = animation.FFMpegWriter(
            fps=fps,
            bitrate=5000,
            extra_args=['-preset', 'slow', '-crf', '18']
        )
        ani.save(save_path, writer=writer)
        print(f"Animation successfully saved to {save_path}")
    except Exception as e:
        print(f"Error saving animation: {e}")
        print("Showing animation preview instead...")
        plt.show()
```

# References Used:
https://igraph.org/c/html/latest/igraph-Community.html

[1608.00163v2.pdf](https://github.com/user-attachments/files/19415758/160

[0906.0612v2.pdf](https://github.com/user-attachments/files/19415761/0906.0612v2.pdf)
8.00163v2.pdf)

