"""
E-Commerce Recommendation Engine
Integrates all data structures for comprehensive product recommendations

This module demonstrates how the individual data structures work together
to create a sophisticated recommendation system.
"""

from data_structures.hash_table import UserItemHashTable
from data_structures.similarity_graph import ProductSimilarityGraph
from data_structures.behavior_tree import UserBehaviorTree
from data_structures.category_tree import CategoryHierarchyTree
from datetime import datetime, timedelta
import random


class RecommendationEngine:
    """
    Main recommendation engine that integrates all data structures.
    
    Provides multiple recommendation strategies:
    - Collaborative filtering (user-item interactions)
    - Content-based filtering (product similarities)
    - Category-based recommendations (hierarchical categories)
    - Behavior-based recommendations (temporal patterns)
    """
    
    def __init__(self):
        """Initialize the recommendation engine with all data structures."""
        self.user_item_table = UserItemHashTable()
        self.similarity_graph = ProductSimilarityGraph()
        self.behavior_tree = UserBehaviorTree()
        self.category_tree = CategoryHierarchyTree("E-commerce Store")
        
        # Cache for performance optimization
        self.recommendation_cache = {}
        self.cache_expiry = {}
        self.cache_duration = timedelta(hours=1)
    
    def add_user_interaction(self, user_id, item_id, rating, action_type="rating"):
        """
        Add a user interaction across all relevant data structures.
        
        Args:
            user_id (str): User identifier
            item_id (str): Item identifier
            rating (float): User rating (1-5 scale)
            action_type (str): Type of interaction
        """
        timestamp = datetime.now()
        
        # Store in hash table
        interaction_data = {
            "rating": rating,
            "timestamp": timestamp.isoformat(),
            "action": action_type
        }
        self.user_item_table.insert(user_id, item_id, interaction_data)
        
        # Store in behavior tree
        self.behavior_tree.insert(user_id, item_id, timestamp, 
                                 action_type, {"rating": rating})
        
        # Invalidate cache for this user
        self._invalidate_user_cache(user_id)
    
    def add_product_similarity(self, product1, product2, similarity_score):
        """Add product similarity relationship."""
        self.similarity_graph.add_similarity_edge(product1, product2, 
                                                 similarity_score)
    
    def add_product_to_category(self, product_id, category_id):
        """Add product to category hierarchy."""
        self.category_tree.add_product_to_category(product_id, category_id)
    
    def get_collaborative_recommendations(self, user_id, num_recommendations=5):
        """
        Generate recommendations based on collaborative filtering.
        
        Finds users with similar preferences and recommends items they liked.
        
        Args:
            user_id (str): Target user
            num_recommendations (int): Number of recommendations to return
            
        Returns:
            list: List of (item_id, predicted_rating) tuples
        """
        # Get user's interactions
        user_interactions = self.user_item_table.get_user_interactions(user_id)
        if not user_interactions:
            return []
        
        user_items = {item_id: data["rating"] 
                     for item_id, data in user_interactions}
        
        # Find similar users
        similar_users = self._find_similar_users(user_id, user_items)
        
        # Generate recommendations from similar users
        recommendations = {}
        
        for similar_user, similarity_score in similar_users[:10]:
            similar_user_interactions = self.user_item_table.get_user_interactions(similar_user)
            
            for item_id, data in similar_user_interactions:
                if item_id not in user_items:  # User hasn't interacted with this item
                    predicted_rating = data["rating"] * similarity_score
                    if item_id in recommendations:
                        recommendations[item_id] += predicted_rating
                    else:
                        recommendations[item_id] = predicted_rating
        
        # Sort by predicted rating
        sorted_recommendations = sorted(recommendations.items(), 
                                      key=lambda x: x[1], reverse=True)
        
        return sorted_recommendations[:num_recommendations]
    
    def get_content_based_recommendations(self, user_id, num_recommendations=5):
        """
        Generate recommendations based on content similarity.
        
        Recommends items similar to those the user has liked.
        
        Args:
            user_id (str): Target user
            num_recommendations (int): Number of recommendations
            
        Returns:
            list: List of (item_id, similarity_score) tuples
        """
        # Get user's highly rated items
        user_interactions = self.user_item_table.get_user_interactions(user_id)
        if not user_interactions:
            return []
        
        liked_items = [item_id for item_id, data in user_interactions 
                      if data["rating"] >= 4.0]
        
        recommendations = {}
        
        # Find items similar to liked items
        for liked_item in liked_items:
            similar_items = self.similarity_graph.get_similar_products(
                liked_item, min_similarity=0.3)
            
            for similar_item, similarity_score in similar_items:
                # Check if user hasn't interacted with this item
                if not self.user_item_table.get(user_id, similar_item):
                    if similar_item in recommendations:
                        recommendations[similar_item] = max(
                            recommendations[similar_item], similarity_score)
                    else:
                        recommendations[similar_item] = similarity_score
        
        # Sort by similarity score
        sorted_recommendations = sorted(recommendations.items(), 
                                      key=lambda x: x[1], reverse=True)
        
        return sorted_recommendations[:num_recommendations]
    
    def get_category_based_recommendations(self, user_id, num_recommendations=5):
        """
        Generate recommendations based on category preferences.
        
        Args:
            user_id (str): Target user
            num_recommendations (int): Number of recommendations
            
        Returns:
            list: List of recommended item IDs
        """
        # Analyze user's category preferences
        user_interactions = self.user_item_table.get_user_interactions(user_id)
        if not user_interactions:
            return []
        
        category_scores = {}
        
        # Calculate category preferences based on ratings
        for item_id, data in user_interactions:
            # Find item's categories and weight by rating
            for category_id, category_node in self.category_tree.category_index.items():
                if item_id in category_node.products:
                    rating_weight = data["rating"] / 5.0  # Normalize to 0-1
                    category_scores[category_id] = category_scores.get(category_id, 0) + rating_weight
        
        # Get recommendations from preferred categories
        recommendations = []
        
        # Sort categories by preference
        sorted_categories = sorted(category_scores.items(), 
                                 key=lambda x: x[1], reverse=True)
        
        for category_id, score in sorted_categories[:3]:  # Top 3 categories
            category_products = self.category_tree.get_products_in_category(
                category_id, include_subcategories=True)
            
            # Filter out items user has already interacted with
            user_items = {item_id for item_id, _ in user_interactions}
            new_items = category_products - user_items
            
            recommendations.extend(list(new_items))
            
            if len(recommendations) >= num_recommendations:
                break
        
        return recommendations[:num_recommendations]
    
    def get_behavior_based_recommendations(self, user_id, num_recommendations=5):
        """
        Generate recommendations based on recent behavior patterns.
        
        Args:
            user_id (str): Target user
            num_recommendations (int): Number of recommendations
            
        Returns:
            list: List of recommended item IDs
        """
        # Get recent user activity
        recent_activity = self.behavior_tree.get_recent_activity(
            user_id=user_id, hours=168)  # Last week
        
        if not recent_activity:
            return []
        
        # Analyze behavior patterns
        viewed_items = set()
        cart_items = set()
        purchased_items = set()
        
        for interaction in recent_activity:
            if interaction.action_type == "view":
                viewed_items.add(interaction.item_id)
            elif interaction.action_type == "cart_add":
                cart_items.add(interaction.item_id)
            elif interaction.action_type == "purchase":
                purchased_items.add(interaction.item_id)
        
        recommendations = []
        
        # Recommend similar items to recently viewed but not purchased
        interested_items = (viewed_items | cart_items) - purchased_items
        
        for item_id in interested_items:
            similar_items = self.similarity_graph.get_similar_products(
                item_id, min_similarity=0.4)
            
            for similar_item, _ in similar_items:
                if (similar_item not in viewed_items and 
                    similar_item not in recommendations):
                    recommendations.append(similar_item)
                    
                    if len(recommendations) >= num_recommendations:
                        break
            
            if len(recommendations) >= num_recommendations:
                break
        
        return recommendations
    
    def get_hybrid_recommendations(self, user_id, num_recommendations=10):
        """
        Generate hybrid recommendations combining multiple strategies.
        
        Args:
            user_id (str): Target user
            num_recommendations (int): Number of recommendations
            
        Returns:
            list: List of (item_id, combined_score, strategy_breakdown) tuples
        """
        # Check cache first
        cache_key = f"hybrid_{user_id}_{num_recommendations}"
        if self._is_cache_valid(cache_key):
            return self.recommendation_cache[cache_key]
        
        # Get recommendations from each strategy
        collaborative = self.get_collaborative_recommendations(user_id, 15)
        content_based = self.get_content_based_recommendations(user_id, 15)
        category_based = self.get_category_based_recommendations(user_id, 15)
        behavior_based = self.get_behavior_based_recommendations(user_id, 15)
        
        # Combine recommendations with weights
        combined_scores = {}
        strategy_breakdown = {}
        
        # Collaborative filtering (weight: 0.3)
        for item_id, score in collaborative:
            combined_scores[item_id] = combined_scores.get(item_id, 0) + score * 0.3
            if item_id not in strategy_breakdown:
                strategy_breakdown[item_id] = {}
            strategy_breakdown[item_id]["collaborative"] = score
        
        # Content-based (weight: 0.25)
        for item_id, score in content_based:
            combined_scores[item_id] = combined_scores.get(item_id, 0) + score * 0.25
            if item_id not in strategy_breakdown:
                strategy_breakdown[item_id] = {}
            strategy_breakdown[item_id]["content_based"] = score
        
        # Category-based (weight: 0.25)
        for item_id in category_based:
            combined_scores[item_id] = combined_scores.get(item_id, 0) + 0.25
            if item_id not in strategy_breakdown:
                strategy_breakdown[item_id] = {}
            strategy_breakdown[item_id]["category_based"] = 1.0
        
        # Behavior-based (weight: 0.2)
        for item_id in behavior_based:
            combined_scores[item_id] = combined_scores.get(item_id, 0) + 0.2
            if item_id not in strategy_breakdown:
                strategy_breakdown[item_id] = {}
            strategy_breakdown[item_id]["behavior_based"] = 1.0
        
        # Sort by combined score
        final_recommendations = []
        for item_id, combined_score in sorted(combined_scores.items(), 
                                            key=lambda x: x[1], reverse=True):
            final_recommendations.append((item_id, combined_score, 
                                        strategy_breakdown[item_id]))
        
        result = final_recommendations[:num_recommendations]
        
        # Cache the result
        self.recommendation_cache[cache_key] = result
        self.cache_expiry[cache_key] = datetime.now() + self.cache_duration
        
        return result
    
    def _find_similar_users(self, target_user, target_user_items):
        """Find users with similar preferences using cosine similarity."""
        similar_users = []
        
        # Get all users (simplified - in practice, you'd sample)
        all_users = set()
        for bucket in self.user_item_table.buckets:
            for user_id, _, _ in bucket:
                all_users.add(user_id)
        
        for user_id in all_users:
            if user_id == target_user:
                continue
            
            user_interactions = self.user_item_table.get_user_interactions(user_id)
            user_items = {item_id: data["rating"] 
                         for item_id, data in user_interactions}
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(target_user_items, user_items)
            if similarity > 0.1:  # Threshold for similarity
                similar_users.append((user_id, similarity))
        
        return sorted(similar_users, key=lambda x: x[1], reverse=True)
    
    def _cosine_similarity(self, items1, items2):
        """Calculate cosine similarity between two item rating dictionaries."""
        common_items = set(items1.keys()) & set(items2.keys())
        if not common_items:
            return 0.0
        
        sum_product = sum(items1[item] * items2[item] for item in common_items)
        sum_sq1 = sum(items1[item] ** 2 for item in common_items)
        sum_sq2 = sum(items2[item] ** 2 for item in common_items)
        
        denominator = (sum_sq1 ** 0.5) * (sum_sq2 ** 0.5)
        return sum_product / denominator if denominator != 0 else 0.0
    
    def _invalidate_user_cache(self, user_id):
        """Invalidate cache entries for a specific user."""
        keys_to_remove = [key for key in self.recommendation_cache.keys() 
                         if user_id in key]
        for key in keys_to_remove:
            del self.recommendation_cache[key]
            del self.cache_expiry[key]
    
    def _is_cache_valid(self, cache_key):
        """Check if a cache entry is valid and not expired."""
        return (cache_key in self.recommendation_cache and 
                cache_key in self.cache_expiry and
                datetime.now() < self.cache_expiry[cache_key])
    
    def get_system_statistics(self):
        """Get comprehensive statistics about the recommendation system."""
        hash_stats = self.user_item_table.get_statistics()
        graph_stats = self.similarity_graph.get_graph_statistics()
        tree_stats = self.behavior_tree.get_statistics()
        category_stats = self.category_tree.get_tree_statistics()
        
        return {
            "user_item_interactions": hash_stats,
            "product_similarities": graph_stats,
            "behavior_tracking": tree_stats,
            "category_hierarchy": category_stats,
            "cache_size": len(self.recommendation_cache)
        }


# Example usage demonstration
if __name__ == "__main__":
    print("E-Commerce Recommendation Engine Demo")
    print("=" * 50)
    
    # Create recommendation engine
    engine = RecommendationEngine()
    
    # Setup sample data (this would typically come from a database)
    # Add categories
    electronics = engine.category_tree.add_category("electronics", "Electronics")
    computers = engine.category_tree.add_category("computers", "Computers", "electronics")
    phones = engine.category_tree.add_category("phones", "Mobile Phones", "electronics")
    laptops = engine.category_tree.add_category("laptops", "Laptops", "computers")
    
    # Add products to categories
    products = ["laptop_001", "laptop_002", "phone_001", "phone_002", "tablet_001"]
    for i, product in enumerate(products):
        if "laptop" in product:
            engine.add_product_to_category(product, "laptops")
        elif "phone" in product:
            engine.add_product_to_category(product, "phones")
        else:
            engine.add_product_to_category(product, "electronics")
    
    # Add product similarities
    similarities = [
        ("laptop_001", "laptop_002", 0.8),
        ("phone_001", "phone_002", 0.9),
        ("laptop_001", "tablet_001", 0.6),
    ]
    for p1, p2, score in similarities:
        engine.add_product_similarity(p1, p2, score)
    
    # Add user interactions
    interactions = [
        ("user_001", "laptop_001", 4.5, "purchase"),
        ("user_001", "phone_001", 3.0, "view"),
        ("user_002", "laptop_001", 5.0, "purchase"),
        ("user_002", "laptop_002", 4.0, "cart_add"),
        ("user_003", "phone_001", 4.5, "purchase"),
    ]
    for user_id, item_id, rating, action in interactions:
        engine.add_user_interaction(user_id, item_id, rating, action)
    
    # Generate recommendations
    print("\\nHybrid Recommendations for user_001:")
    recommendations = engine.get_hybrid_recommendations("user_001", 5)
    for item_id, score, breakdown in recommendations:
        print(f"  {item_id}: score={score:.3f}, strategies={breakdown}")
    
    print("\\nSystem Statistics:")
    stats = engine.get_system_statistics()
    for component, component_stats in stats.items():
        print(f"  {component}: {component_stats}")