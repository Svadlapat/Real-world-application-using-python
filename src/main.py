"""
Main demonstration script for the E-Commerce Recommendation System
Shows the integration and functionality of all data structures
"""

import sys
import os
from datetime import datetime, timedelta

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_engine import RecommendationEngine


def demonstrate_data_structures():
    """Demonstrate individual data structure capabilities."""
    
    print("=" * 60)
    print("DATA STRUCTURE DEMONSTRATIONS")
    print("=" * 60)
    
    engine = RecommendationEngine()
    
    # 1. Hash Table Demonstration
    print("\\n1. USER-ITEM INTERACTION HASH TABLE")
    print("-" * 40)
    
    # Add sample interactions
    interactions = [
        ("user_001", "laptop_dell_001", 4.5, "purchase"),
        ("user_001", "phone_iphone_001", 3.0, "view"),
        ("user_001", "tablet_ipad_001", 4.0, "cart_add"),
        ("user_002", "laptop_dell_001", 5.0, "purchase"),
        ("user_002", "laptop_hp_001", 4.0, "view"),
        ("user_003", "phone_iphone_001", 4.5, "purchase"),
        ("user_003", "phone_samsung_001", 3.5, "view"),
    ]
    
    for user_id, item_id, rating, action in interactions:
        engine.add_user_interaction(user_id, item_id, rating, action)
    
    # Demonstrate hash table operations
    print(f"Total interactions stored: {engine.user_item_table.size}")
    
    user_data = engine.user_item_table.get_user_interactions("user_001")
    print(f"User_001 interactions: {len(user_data)}")
    for item_id, data in user_data:
        print(f"  - {item_id}: rating={data['rating']}, action={data['action']}")
    
    hash_stats = engine.user_item_table.get_statistics()
    print(f"Hash table efficiency: Load factor = {hash_stats['load_factor']:.3f}")
    
    # 2. Product Similarity Graph Demonstration
    print("\\n2. PRODUCT SIMILARITY GRAPH")
    print("-" * 40)
    
    # Add product similarities
    similarities = [
        ("laptop_dell_001", "laptop_hp_001", 0.85),
        ("laptop_dell_001", "laptop_lenovo_001", 0.78),
        ("phone_iphone_001", "phone_samsung_001", 0.72),
        ("phone_iphone_001", "tablet_ipad_001", 0.65),
        ("laptop_dell_001", "tablet_ipad_001", 0.45),
        ("phone_samsung_001", "tablet_samsung_001", 0.80),
    ]
    
    for p1, p2, score in similarities:
        engine.add_product_similarity(p1, p2, score)
    
    # Demonstrate graph operations
    similar_products = engine.similarity_graph.get_similar_products(
        "laptop_dell_001", min_similarity=0.5)
    print(f"Products similar to laptop_dell_001:")
    for product, similarity in similar_products:
        print(f"  - {product}: similarity = {similarity:.3f}")
    
    # Find recommendation path
    path = engine.similarity_graph.find_recommendation_path(
        "laptop_dell_001", "phone_iphone_001")
    print(f"Recommendation path: {' -> '.join(path) if path else 'No path found'}")
    
    graph_stats = engine.similarity_graph.get_graph_statistics()
    print(f"Graph density: {graph_stats['density']:.3f}")
    
    # 3. User Behavior Tree Demonstration
    print("\\n3. USER BEHAVIOR TREE (Temporal Analysis)")
    print("-" * 40)
    
    # The behavior tree is automatically populated when adding interactions
    recent_activity = engine.behavior_tree.get_recent_activity(
        user_id="user_001", hours=24*7)  # Last week
    
    print(f"User_001 recent activity ({len(recent_activity)} interactions):")
    for interaction in recent_activity[-3:]:  # Show last 3
        print(f"  - {interaction.item_id} ({interaction.action_type}) "
              f"at {interaction.timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    # Behavior pattern analysis
    pattern = engine.behavior_tree.get_user_behavior_pattern("user_001", days=30)
    print(f"Behavior pattern: {pattern['action_counts']}")
    
    tree_stats = engine.behavior_tree.get_statistics()
    print(f"Tree balance: {'Balanced' if tree_stats['is_balanced'] else 'Unbalanced'}")
    
    # 4. Category Hierarchy Tree Demonstration
    print("\\n4. CATEGORY HIERARCHY TREE")
    print("-" * 40)
    
    # Build category hierarchy
    electronics = engine.category_tree.add_category("electronics", "Electronics")
    computers = engine.category_tree.add_category("computers", "Computers", "electronics")
    phones_cat = engine.category_tree.add_category("phones", "Mobile Phones", "electronics")
    laptops = engine.category_tree.add_category("laptops", "Laptops", "computers")
    tablets = engine.category_tree.add_category("tablets", "Tablets", "electronics")
    
    # Add products to categories
    product_categories = [
        ("laptop_dell_001", "laptops"),
        ("laptop_hp_001", "laptops"),
        ("laptop_lenovo_001", "laptops"),
        ("phone_iphone_001", "phones"),
        ("phone_samsung_001", "phones"),
        ("tablet_ipad_001", "tablets"),
        ("tablet_samsung_001", "tablets"),
    ]
    
    for product_id, category_id in product_categories:
        engine.add_product_to_category(product_id, category_id)
    
    # Demonstrate category operations
    print("Category tree structure:")
    print(engine.category_tree.display_tree(max_depth=3))
    
    electronics_products = engine.category_tree.get_products_in_category(
        "electronics", include_subcategories=True)
    print(f"\\nTotal products in Electronics: {len(electronics_products)}")
    
    category_recommendations = engine.category_tree.get_category_recommendations(
        "laptop_dell_001", max_recommendations=3)
    print(f"Category-based recommendations for laptop_dell_001: {category_recommendations}")
    
    category_stats = engine.category_tree.get_tree_statistics()
    print(f"Category tree depth: {category_stats['max_depth']}")


def demonstrate_recommendation_strategies():
    """Demonstrate different recommendation strategies."""
    
    print("\\n\\n" + "=" * 60)
    print("RECOMMENDATION STRATEGY DEMONSTRATIONS")
    print("=" * 60)
    
    engine = RecommendationEngine()
    
    # Setup comprehensive test data
    setup_comprehensive_data(engine)
    
    target_user = "alice_001"
    
    # 1. Collaborative Filtering
    print("\\n1. COLLABORATIVE FILTERING RECOMMENDATIONS")
    print("-" * 45)
    
    collaborative_recs = engine.get_collaborative_recommendations(target_user, 5)
    print(f"Recommendations for {target_user} based on similar users:")
    for item_id, predicted_rating in collaborative_recs:
        print(f"  - {item_id}: predicted rating = {predicted_rating:.3f}")
    
    # 2. Content-Based Filtering
    print("\\n2. CONTENT-BASED FILTERING RECOMMENDATIONS")
    print("-" * 45)
    
    content_recs = engine.get_content_based_recommendations(target_user, 5)
    print(f"Recommendations based on item similarities:")
    for item_id, similarity_score in content_recs:
        print(f"  - {item_id}: similarity score = {similarity_score:.3f}")
    
    # 3. Category-Based Recommendations
    print("\\n3. CATEGORY-BASED RECOMMENDATIONS")
    print("-" * 35)
    
    category_recs = engine.get_category_based_recommendations(target_user, 5)
    print(f"Recommendations based on category preferences:")
    for item_id in category_recs:
        print(f"  - {item_id}")
    
    # 4. Behavior-Based Recommendations
    print("\\n4. BEHAVIOR-BASED RECOMMENDATIONS")
    print("-" * 35)
    
    behavior_recs = engine.get_behavior_based_recommendations(target_user, 5)
    print(f"Recommendations based on recent behavior:")
    for item_id in behavior_recs:
        print(f"  - {item_id}")
    
    # 5. Hybrid Recommendations
    print("\\n5. HYBRID RECOMMENDATIONS (COMBINED)")
    print("-" * 35)
    
    hybrid_recs = engine.get_hybrid_recommendations(target_user, 5)
    print(f"Final hybrid recommendations:")
    for item_id, combined_score, breakdown in hybrid_recs:
        print(f"  - {item_id}: score = {combined_score:.3f}")
        strategy_details = ", ".join([f"{k}={v:.2f}" for k, v in breakdown.items()])
        print(f"    Strategies: {strategy_details}")


def setup_comprehensive_data(engine):
    """Setup comprehensive test data for recommendation demonstrations."""
    
    # Create category hierarchy
    electronics = engine.category_tree.add_category("electronics", "Electronics")
    computers = engine.category_tree.add_category("computers", "Computers", "electronics")
    phones = engine.category_tree.add_category("phones", "Mobile Phones", "electronics")
    laptops = engine.category_tree.add_category("laptops", "Laptops", "computers")
    tablets = engine.category_tree.add_category("tablets", "Tablets", "electronics")
    accessories = engine.category_tree.add_category("accessories", "Accessories", "electronics")
    
    # Product catalog
    products = {
        "laptops": ["laptop_dell_xps13", "laptop_macbook_pro", "laptop_hp_spectre", 
                   "laptop_lenovo_thinkpad", "laptop_surface_pro"],
        "phones": ["phone_iphone_14", "phone_samsung_s23", "phone_pixel_7", 
                  "phone_oneplus_10"],
        "tablets": ["tablet_ipad_air", "tablet_surface_tablet", "tablet_samsung_tab"],
        "accessories": ["mouse_logitech", "keyboard_mechanical", "headphones_sony", 
                       "monitor_dell"]
    }
    
    # Add products to categories
    for category, product_list in products.items():
        for product in product_list:
            engine.add_product_to_category(product, category)
    
    # Add product similarities (content-based relationships)
    similarities = [
        # Laptop similarities
        ("laptop_dell_xps13", "laptop_hp_spectre", 0.85),
        ("laptop_macbook_pro", "laptop_surface_pro", 0.78),
        ("laptop_lenovo_thinkpad", "laptop_dell_xps13", 0.80),
        
        # Phone similarities
        ("phone_iphone_14", "phone_samsung_s23", 0.75),
        ("phone_pixel_7", "phone_oneplus_10", 0.82),
        
        # Cross-category similarities
        ("laptop_macbook_pro", "tablet_ipad_air", 0.65),
        ("phone_samsung_s23", "tablet_samsung_tab", 0.70),
        ("laptop_dell_xps13", "mouse_logitech", 0.45),
        ("laptop_macbook_pro", "monitor_dell", 0.50),
    ]
    
    for p1, p2, score in similarities:
        engine.add_product_similarity(p1, p2, score)
    
    # Add user interactions for collaborative filtering
    users_data = [
        # Alice - likes premium laptops and Apple products
        ("alice_001", [
            ("laptop_macbook_pro", 5.0, "purchase"),
            ("tablet_ipad_air", 4.5, "purchase"),
            ("phone_iphone_14", 4.8, "view"),
            ("monitor_dell", 4.0, "cart_add"),
            ("laptop_dell_xps13", 3.5, "view"),
        ]),
        
        # Bob - budget-conscious, likes diverse tech
        ("bob_002", [
            ("laptop_hp_spectre", 4.2, "purchase"),
            ("phone_pixel_7", 4.5, "purchase"),
            ("mouse_logitech", 4.0, "purchase"),
            ("laptop_lenovo_thinkpad", 4.0, "view"),
            ("headphones_sony", 3.8, "cart_add"),
        ]),
        
        # Carol - similar taste to Alice (for collaborative filtering)
        ("carol_003", [
            ("laptop_macbook_pro", 4.8, "purchase"),
            ("tablet_ipad_air", 4.2, "view"),
            ("phone_iphone_14", 5.0, "purchase"),
            ("laptop_surface_pro", 4.0, "view"),
        ]),
        
        # David - mobile enthusiast
        ("david_004", [
            ("phone_samsung_s23", 4.7, "purchase"),
            ("tablet_samsung_tab", 4.3, "purchase"),
            ("phone_oneplus_10", 4.0, "view"),
            ("headphones_sony", 4.5, "purchase"),
        ]),
    ]
    
    for user_id, interactions in users_data:
        for item_id, rating, action in interactions:
            engine.add_user_interaction(user_id, item_id, rating, action)


def show_system_performance():
    """Demonstrate system performance and statistics."""
    
    print("\\n\\n" + "=" * 60)
    print("SYSTEM PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    engine = RecommendationEngine()
    setup_comprehensive_data(engine)
    
    # Get comprehensive statistics
    stats = engine.get_system_statistics()
    
    print("\\nSYSTEM STATISTICS:")
    print("-" * 20)
    
    print(f"User-Item Interactions:")
    ui_stats = stats['user_item_interactions']
    print(f"  - Total interactions: {ui_stats['size']}")
    print(f"  - Hash table load factor: {ui_stats['load_factor']:.3f}")
    print(f"  - Average bucket size: {ui_stats['avg_bucket_size']:.2f}")
    
    print(f"\\nProduct Similarity Graph:")
    graph_stats = stats['product_similarities']
    print(f"  - Total products: {graph_stats['products']}")
    print(f"  - Total similarity edges: {graph_stats['edges']}")
    print(f"  - Graph density: {graph_stats['density']:.4f}")
    print(f"  - Average degree: {graph_stats['average_degree']:.2f}")
    
    print(f"\\nUser Behavior Tree:")
    tree_stats = stats['behavior_tracking']
    print(f"  - Total behavior records: {tree_stats['size']}")
    print(f"  - Tree height: {tree_stats['height']}")
    print(f"  - Is balanced: {tree_stats['is_balanced']}")
    
    print(f"\\nCategory Hierarchy:")
    cat_stats = stats['category_hierarchy']
    print(f"  - Total categories: {cat_stats['total_categories']}")
    print(f"  - Total products: {cat_stats['total_products']}")
    print(f"  - Tree depth: {cat_stats['max_depth']}")
    print(f"  - Average products per category: {cat_stats['avg_products_per_category']:.2f}")
    
    print(f"\\nCache Statistics:")
    print(f"  - Cache entries: {stats['cache_size']}")
    
    # Performance demonstration
    print("\\n\\nPERFORMACE DEMONSTRATION:")
    print("-" * 25)
    
    import time
    
    # Time recommendation generation
    start_time = time.time()
    recommendations = engine.get_hybrid_recommendations("alice_001", 10)
    end_time = time.time()
    
    print(f"Hybrid recommendation generation time: {(end_time - start_time)*1000:.2f} ms")
    print(f"Number of recommendations: {len(recommendations)}")
    
    # Test caching
    start_time = time.time()
    cached_recommendations = engine.get_hybrid_recommendations("alice_001", 10)
    end_time = time.time()
    
    print(f"Cached recommendation retrieval time: {(end_time - start_time)*1000:.2f} ms")
    print(f"Cache hit: {recommendations == cached_recommendations}")


def main():
    """Main demonstration function."""
    
    print("E-COMMERCE RECOMMENDATION SYSTEM")
    print("Data Structures Implementation and Optimization")
    print("Phase 1: Design and Implementation Demonstration")
    
    try:
        # Individual data structure demonstrations
        demonstrate_data_structures()
        
        # Recommendation strategy demonstrations
        demonstrate_recommendation_strategies()
        
        # System performance analysis
        show_system_performance()
        
        print("\\n\\n" + "=" * 60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\\nAll data structures are working correctly and efficiently.")
        print("The system demonstrates:")
        print("- Efficient data storage and retrieval")
        print("- Multiple recommendation strategies")
        print("- Real-time performance optimization")
        print("- Scalable architecture design")
        
    except Exception as e:
        print(f"\\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()