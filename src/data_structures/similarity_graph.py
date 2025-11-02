"""
Product Similarity Graph Implementation
Represents relationships between products for content-based recommendations

This module implements an adjacency list-based graph structure to store
and efficiently query product similarity relationships.
"""

from collections import defaultdict, deque
import heapq

class ProductSimilarityGraph:
    """
    Graph implementation for storing product similarity relationships.
    
    Uses adjacency list representation for efficient storage and traversal.
    Supports weighted edges to represent similarity scores.
    """
    
    def __init__(self):
        """Initialize the graph with empty adjacency lists."""
        self.graph = defaultdict(list)  # product_id -> [(similar_product_id, similarity_score)]
        self.products = set()  # Set of all product IDs
        self.edge_count = 0
    
    def add_product(self, product_id, metadata=None):
        """
        Add a product to the graph.
        
        Args:
            product_id (str/int): Unique product identifier
            metadata (dict): Optional product metadata (name, category, etc.)
        """
        self.products.add(product_id)
        if product_id not in self.graph:
            self.graph[product_id] = []
    
    def add_similarity_edge(self, product1, product2, similarity_score):
        """
        Add a similarity relationship between two products.
        
        Args:
            product1 (str/int): First product ID
            product2 (str/int): Second product ID
            similarity_score (float): Similarity score (0.0 to 1.0)
        
        Time Complexity: O(1) for insertion
        """
        # Ensure products exist in the graph
        self.add_product(product1)
        self.add_product(product2)
        
        # Add bidirectional edge (undirected graph)
        self.graph[product1].append((product2, similarity_score))
        self.graph[product2].append((product1, similarity_score))
        
        self.edge_count += 1
    
    def get_similar_products(self, product_id, min_similarity=0.0, max_results=10):
        """
        Get products similar to the given product.
        
        Args:
            product_id (str/int): Product to find similarities for
            min_similarity (float): Minimum similarity threshold
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of (product_id, similarity_score) tuples, sorted by similarity
            
        Time Complexity: O(k log k) where k is the number of similar products
        """
        if product_id not in self.graph:
            return []
        
        similar_products = []
        
        for similar_product, similarity_score in self.graph[product_id]:
            if similarity_score >= min_similarity:
                similar_products.append((similar_product, similarity_score))
        
        # Sort by similarity score in descending order
        similar_products.sort(key=lambda x: x[1], reverse=True)
        
        return similar_products[:max_results]
    
    def find_recommendation_path(self, start_product, target_product, max_depth=3):
        """
        Find a path of similar products from start to target product.
        
        Uses BFS to find the shortest path of product similarities.
        Useful for finding recommendation chains.
        
        Args:
            start_product (str/int): Starting product
            target_product (str/int): Target product
            max_depth (int): Maximum path length to search
            
        Returns:
            list: Path of product IDs if found, empty list otherwise
            
        Time Complexity: O(V + E) where V is vertices and E is edges
        """
        if start_product not in self.graph or target_product not in self.graph:
            return []
        
        if start_product == target_product:
            return [start_product]
        
        queue = deque([(start_product, [start_product])])
        visited = {start_product}
        
        while queue:
            current_product, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            for neighbor_product, similarity_score in self.graph[current_product]:
                if neighbor_product == target_product:
                    return path + [neighbor_product]
                
                if neighbor_product not in visited:
                    visited.add(neighbor_product)
                    queue.append((neighbor_product, path + [neighbor_product]))
        
        return []  # No path found
    
    def get_top_k_similar_products_advanced(self, product_id, k=5, use_transitive=True):
        """
        Advanced similarity search using transitive relationships.
        
        Considers not just direct similarities but also products similar
        to similar products (2-hop similarity).
        
        Args:
            product_id (str/int): Product to find similarities for
            k (int): Number of top similar products to return
            use_transitive (bool): Whether to consider 2-hop similarities
            
        Returns:
            list: List of (product_id, combined_similarity_score) tuples
            
        Time Complexity: O(d² log k) where d is average degree
        """
        if product_id not in self.graph:
            return []
        
        similarity_scores = {}
        
        # Direct similarities (1-hop)
        for similar_product, similarity_score in self.graph[product_id]:
            similarity_scores[similar_product] = similarity_score
        
        # Transitive similarities (2-hop)
        if use_transitive:
            for similar_product, sim1 in self.graph[product_id]:
                for second_hop_product, sim2 in self.graph[similar_product]:
                    if second_hop_product != product_id and second_hop_product not in similarity_scores:
                        # Combine similarities using geometric mean
                        transitive_score = (sim1 * sim2) ** 0.5 * 0.7  # Damping factor
                        similarity_scores[second_hop_product] = transitive_score
        
        # Use heap to get top-k efficiently
        top_k = heapq.nlargest(k, similarity_scores.items(), key=lambda x: x[1])
        
        return top_k
    
    def get_product_clusters(self, min_similarity=0.8):
        """
        Find clusters of highly similar products using connected components.
        
        Args:
            min_similarity (float): Minimum similarity for cluster membership
            
        Returns:
            list: List of product clusters (lists of product IDs)
            
        Time Complexity: O(V + E) where V is vertices and E is edges
        """
        visited = set()
        clusters = []
        
        def dfs_cluster(product_id, current_cluster):
            """DFS to find all products in the same cluster."""
            visited.add(product_id)
            current_cluster.append(product_id)
            
            for similar_product, similarity_score in self.graph[product_id]:
                if similarity_score >= min_similarity and similar_product not in visited:
                    dfs_cluster(similar_product, current_cluster)
        
        for product_id in self.products:
            if product_id not in visited:
                cluster = []
                dfs_cluster(product_id, cluster)
                if len(cluster) > 1:  # Only include clusters with multiple products
                    clusters.append(cluster)
        
        return clusters
    
    def get_graph_statistics(self):
        """
        Get comprehensive statistics about the similarity graph.
        
        Returns:
            dict: Graph statistics including density, clustering, etc.
        """
        total_products = len(self.products)
        total_edges = self.edge_count
        
        if total_products == 0:
            return {"products": 0, "edges": 0, "density": 0}
        
        # Calculate density
        max_possible_edges = total_products * (total_products - 1) // 2
        density = total_edges / max_possible_edges if max_possible_edges > 0 else 0
        
        # Calculate degree distribution
        degrees = [len(self.graph[product]) for product in self.products]
        avg_degree = sum(degrees) / len(degrees) if degrees else 0
        max_degree = max(degrees) if degrees else 0
        
        return {
            "products": total_products,
            "edges": total_edges,
            "density": density,
            "average_degree": avg_degree,
            "max_degree": max_degree,
            "degree_distribution": degrees
        }

# Example usage and testing
if __name__ == "__main__":
    # Create similarity graph
    similarity_graph = ProductSimilarityGraph()
    
    # Sample product data
    products = [
        "laptop_001", "laptop_002", "phone_001", "phone_002", 
        "tablet_001", "headphones_001", "mouse_001", "keyboard_001"
    ]
    
    # Add products
    for product in products:
        similarity_graph.add_product(product)
    
    # Add similarity relationships
    similarities = [
        ("laptop_001", "laptop_002", 0.9),      # Very similar laptops
        ("phone_001", "phone_002", 0.8),        # Similar phones
        ("laptop_001", "tablet_001", 0.6),      # Moderate similarity
        ("phone_001", "headphones_001", 0.4),   # Complementary products
        ("mouse_001", "keyboard_001", 0.7),     # Related accessories
        ("laptop_001", "mouse_001", 0.5),       # Laptop accessories
        ("laptop_002", "mouse_001", 0.5),
        ("tablet_001", "headphones_001", 0.3),
    ]
    
    for product1, product2, score in similarities:
        similarity_graph.add_similarity_edge(product1, product2, score)
    
    # Demonstrate functionality
    print("Product Similarity Graph Demo")
    print("=" * 40)
    
    # Find similar products
    similar = similarity_graph.get_similar_products("laptop_001", min_similarity=0.5)
    print(f"Products similar to laptop_001: {similar}")
    
    # Advanced similarity search
    advanced_similar = similarity_graph.get_top_k_similar_products_advanced("laptop_001", k=3)
    print(f"Advanced similarity for laptop_001: {advanced_similar}")
    
    # Find recommendation path
    path = similarity_graph.find_recommendation_path("laptop_001", "headphones_001")
    print(f"Recommendation path from laptop_001 to headphones_001: {path}")
    
    # Get clusters
    clusters = similarity_graph.get_product_clusters(min_similarity=0.7)
    print(f"Product clusters (min_similarity=0.7): {clusters}")
    
    # Graph statistics
    stats = similarity_graph.get_graph_statistics()
    print(f"Graph statistics: {stats}")