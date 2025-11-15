"""
Interactive Command Line Interface for E-Commerce Recommendation System
Phase 2: Proof of Concept Interactive Demonstration

This module provides an interactive CLI for demonstrating and testing
the recommendation system functionality.
"""

import sys
import os
import json
from datetime import datetime, timedelta
import time

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommendation_engine import RecommendationEngine


class RecommendationSystemCLI:
    """Interactive CLI for the E-Commerce Recommendation System."""
    
    def __init__(self):
        """Initialize the CLI with a recommendation engine."""
        self.engine = RecommendationEngine()
        self.demo_data_loaded = False
        
    def display_banner(self):
        """Display the application banner."""
        print("=" * 80)
        print("E-COMMERCE RECOMMENDATION SYSTEM")
        print("Phase 2: Proof of Concept Interactive Demo")
        print("=" * 80)
        print("Welcome to the interactive demonstration of our data structures!")
        print("This system demonstrates hash tables, graphs, trees, and their integration.")
        print("=" * 80)
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1. 🏗️  Load Demo Data")
        print("2. 👤 User Interaction Management")
        print("3. 🔗 Product Similarity Management")
        print("4. 📊 Behavior Analysis")
        print("5. 🏷️  Category Management")
        print("6. 🎯 Generate Recommendations")
        print("7. 📈 System Statistics")
        print("8. 🧪 Run Test Suite")
        print("9. 💾 Data Import/Export")
        print("0. 🚪 Exit")
        print("-" * 40)
    
    def load_demo_data(self):
        """Load comprehensive demo data for testing."""
        print("\n🏗️ LOADING DEMO DATA...")
        print("-" * 40)
        
        try:
            # Create category hierarchy
            print("Creating category hierarchy...")
            categories = [
                ("electronics", "Electronics", None),
                ("computers", "Computers", "electronics"),
                ("phones", "Mobile Phones", "electronics"),
                ("tablets", "Tablets", "electronics"),
                ("laptops", "Laptops", "computers"),
                ("gaming", "Gaming", "computers"),
                ("accessories", "Accessories", "electronics"),
            ]
            
            for cat_id, cat_name, parent_id in categories:
                if parent_id:
                    self.engine.category_tree.add_category(cat_id, cat_name, parent_id)
                else:
                    self.engine.category_tree.add_category(cat_id, cat_name)
            
            # Add products to categories
            print("Adding products to categories...")
            products_data = [
                ("laptop_dell_xps13", "laptops"),
                ("laptop_macbook_pro", "laptops"),
                ("laptop_hp_spectre", "laptops"),
                ("laptop_gaming_asus", "gaming"),
                ("phone_iphone_14", "phones"),
                ("phone_samsung_s23", "phones"),
                ("phone_pixel_7", "phones"),
                ("tablet_ipad_air", "tablets"),
                ("tablet_surface_pro", "tablets"),
                ("mouse_logitech", "accessories"),
                ("keyboard_mechanical", "accessories"),
                ("headphones_sony", "accessories"),
            ]
            
            for product_id, category_id in products_data:
                self.engine.add_product_to_category(product_id, category_id)
            
            # Add product similarities
            print("Building product similarity network...")
            similarities = [
                ("laptop_dell_xps13", "laptop_hp_spectre", 0.85),
                ("laptop_macbook_pro", "tablet_ipad_air", 0.65),
                ("phone_iphone_14", "tablet_ipad_air", 0.70),
                ("phone_samsung_s23", "tablet_surface_pro", 0.68),
                ("laptop_dell_xps13", "mouse_logitech", 0.45),
                ("laptop_macbook_pro", "headphones_sony", 0.50),
                ("phone_iphone_14", "phone_samsung_s23", 0.75),
                ("laptop_gaming_asus", "mouse_logitech", 0.80),
                ("laptop_gaming_asus", "keyboard_mechanical", 0.85),
            ]
            
            for p1, p2, score in similarities:
                self.engine.add_product_similarity(p1, p2, score)
            
            # Add user interactions
            print("Creating user interaction history...")
            users_data = [
                # Tech enthusiast Alice
                ("alice_tech", [
                    ("laptop_macbook_pro", 5.0, "purchase"),
                    ("tablet_ipad_air", 4.5, "purchase"),
                    ("phone_iphone_14", 4.8, "view"),
                    ("headphones_sony", 4.2, "cart_add"),
                    ("laptop_dell_xps13", 3.5, "view"),
                ]),
                
                # Budget-conscious Bob
                ("bob_budget", [
                    ("laptop_hp_spectre", 4.2, "purchase"),
                    ("phone_pixel_7", 4.5, "purchase"),
                    ("mouse_logitech", 4.0, "purchase"),
                    ("keyboard_mechanical", 3.8, "view"),
                    ("headphones_sony", 3.5, "cart_add"),
                ]),
                
                # Gaming enthusiast Charlie
                ("charlie_gamer", [
                    ("laptop_gaming_asus", 5.0, "purchase"),
                    ("mouse_logitech", 4.8, "purchase"),
                    ("keyboard_mechanical", 4.7, "purchase"),
                    ("headphones_sony", 4.5, "purchase"),
                    ("tablet_surface_pro", 3.0, "view"),
                ]),
                
                # Mobile-focused Diana
                ("diana_mobile", [
                    ("phone_samsung_s23", 4.7, "purchase"),
                    ("tablet_surface_pro", 4.3, "purchase"),
                    ("phone_pixel_7", 4.0, "view"),
                    ("tablet_ipad_air", 3.8, "view"),
                ]),
                
                # Similar to Alice (for collaborative filtering)
                ("eve_similar", [
                    ("laptop_macbook_pro", 4.8, "purchase"),
                    ("tablet_ipad_air", 4.2, "view"),
                    ("phone_iphone_14", 5.0, "purchase"),
                    ("headphones_sony", 4.0, "cart_add"),
                ]),
            ]
            
            for user_id, interactions in users_data:
                for item_id, rating, action in interactions:
                    self.engine.add_user_interaction(user_id, item_id, rating, action)
            
            self.demo_data_loaded = True
            print("\n✅ Demo data loaded successfully!")
            print(f"   📊 Categories: {self.engine.category_tree.total_categories}")
            print(f"   📦 Products: {self.engine.category_tree.total_products}")
            print(f"   👥 Users: 5")
            print(f"   🤝 Interactions: {self.engine.user_item_table.size}")
            print(f"   🔗 Similarities: {self.engine.similarity_graph.edge_count}")
            
        except Exception as e:
            print(f"❌ Error loading demo data: {e}")
    
    def user_interaction_menu(self):
        """Handle user interaction management."""
        while True:
            print("\n👤 USER INTERACTION MANAGEMENT")
            print("-" * 40)
            print("1. Add User Interaction")
            print("2. View User Profile")
            print("3. Search User Interactions")
            print("4. Update Interaction")
            print("5. Delete Interaction") 
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self._add_user_interaction()
            elif choice == "2":
                self._view_user_profile()
            elif choice == "3":
                self._search_user_interactions()
            elif choice == "4":
                self._update_interaction()
            elif choice == "5":
                self._delete_interaction()
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _add_user_interaction(self):
        """Add a new user interaction."""
        print("\n➕ ADD USER INTERACTION")
        print("-" * 30)
        
        try:
            user_id = input("User ID: ").strip()
            item_id = input("Item ID: ").strip()
            rating = float(input("Rating (1.0-5.0): ").strip())
            action = input("Action (purchase/view/cart_add/wishlist_add): ").strip()
            
            if not all([user_id, item_id]) or not 1.0 <= rating <= 5.0:
                print("❌ Invalid input! Please check your values.")
                return
            
            self.engine.add_user_interaction(user_id, item_id, rating, action)
            print(f"✅ Added interaction: {user_id} → {item_id} ({rating}⭐, {action})")
            
        except ValueError:
            print("❌ Invalid rating! Please enter a number between 1.0 and 5.0.")
        except Exception as e:
            print(f"❌ Error adding interaction: {e}")
    
    def _view_user_profile(self):
        """View a user's complete profile and interaction history."""
        print("\n👁️ VIEW USER PROFILE")
        print("-" * 25)
        
        user_id = input("Enter User ID: ").strip()
        if not user_id:
            print("❌ Invalid user ID!")
            return
        
        # Get user interactions
        interactions = self.engine.user_item_table.get_user_interactions(user_id)
        
        if not interactions:
            print(f"❌ No interactions found for user '{user_id}'")
            return
        
        print(f"\n📊 PROFILE FOR USER: {user_id}")
        print("-" * 50)
        print(f"Total Interactions: {len(interactions)}")
        
        # Display interactions
        print("\n🛍️ INTERACTION HISTORY:")
        for item_id, data in interactions:
            print(f"  • {item_id}: {data['rating']}⭐ ({data['action']}) - {data['timestamp'][:10]}")
        
        # Get behavior analysis
        try:
            pattern = self.engine.behavior_tree.get_user_behavior_pattern(user_id, days=30)
            print(f"\n📈 BEHAVIOR ANALYSIS (Last 30 days):")
            print(f"  • Total interactions: {pattern['total_interactions']}")
            print(f"  • Action breakdown: {pattern['action_counts']}")
            
            if pattern['favorite_items']:
                print(f"  • Favorite items:")
                for item_id, count in pattern['favorite_items'][:3]:
                    print(f"    - {item_id}: {count} interactions")
        except Exception as e:
            print(f"  ⚠️ Could not analyze behavior patterns: {e}")
    
    def _search_user_interactions(self):
        """Search for specific user interactions."""
        print("\n🔍 SEARCH USER INTERACTIONS")
        print("-" * 35)
        
        user_id = input("User ID: ").strip()
        item_id = input("Item ID (optional): ").strip()
        
        if not user_id:
            print("❌ User ID is required!")
            return
        
        if item_id:
            # Search for specific interaction
            result = self.engine.user_item_table.get(user_id, item_id)
            if result:
                print(f"\n✅ Found interaction:")
                print(f"  User: {user_id}")
                print(f"  Item: {item_id}")
                print(f"  Rating: {result['rating']}⭐")
                print(f"  Action: {result['action']}")
                print(f"  Timestamp: {result['timestamp']}")
            else:
                print(f"❌ No interaction found between {user_id} and {item_id}")
        else:
            # Search for all user interactions
            interactions = self.engine.user_item_table.get_user_interactions(user_id)
            if interactions:
                print(f"\n✅ Found {len(interactions)} interactions for {user_id}:")
                for item_id, data in interactions[:10]:  # Show first 10
                    print(f"  • {item_id}: {data['rating']}⭐ ({data['action']})")
                if len(interactions) > 10:
                    print(f"  ... and {len(interactions) - 10} more")
            else:
                print(f"❌ No interactions found for user {user_id}")
    
    def _update_interaction(self):
        """Update an existing interaction."""
        print("\n✏️ UPDATE INTERACTION")
        print("-" * 25)
        
        try:
            user_id = input("User ID: ").strip()
            item_id = input("Item ID: ").strip()
            
            # Check if interaction exists
            existing = self.engine.user_item_table.get(user_id, item_id)
            if not existing:
                print(f"❌ No interaction found between {user_id} and {item_id}")
                return
            
            print(f"\nCurrent interaction:")
            print(f"  Rating: {existing['rating']}⭐")
            print(f"  Action: {existing['action']}")
            
            new_rating = float(input("New Rating (1.0-5.0): ").strip())
            new_action = input("New Action: ").strip()
            
            if not 1.0 <= new_rating <= 5.0:
                print("❌ Invalid rating!")
                return
            
            self.engine.add_user_interaction(user_id, item_id, new_rating, new_action)
            print(f"✅ Updated interaction: {user_id} → {item_id} ({new_rating}⭐, {new_action})")
            
        except ValueError:
            print("❌ Invalid rating! Please enter a number.")
        except Exception as e:
            print(f"❌ Error updating interaction: {e}")
    
    def _delete_interaction(self):
        """Delete a user interaction."""
        print("\n🗑️ DELETE INTERACTION")
        print("-" * 25)
        
        user_id = input("User ID: ").strip()
        item_id = input("Item ID: ").strip()
        
        if not user_id or not item_id:
            print("❌ Both User ID and Item ID are required!")
            return
        
        # Check if interaction exists
        existing = self.engine.user_item_table.get(user_id, item_id)
        if not existing:
            print(f"❌ No interaction found between {user_id} and {item_id}")
            return
        
        confirm = input(f"Delete interaction {user_id} → {item_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            success = self.engine.user_item_table.delete(user_id, item_id)
            if success:
                print("✅ Interaction deleted successfully!")
            else:
                print("❌ Failed to delete interaction!")
        else:
            print("❌ Deletion cancelled.")
    
    def product_similarity_menu(self):
        """Handle product similarity management."""
        while True:
            print("\n🔗 PRODUCT SIMILARITY MANAGEMENT")
            print("-" * 45)
            print("1. Add Product Similarity")
            print("2. Find Similar Products")
            print("3. Find Recommendation Path")
            print("4. Analyze Product Clusters")
            print("5. View Similarity Network Stats")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self._add_product_similarity()
            elif choice == "2":
                self._find_similar_products()
            elif choice == "3":
                self._find_recommendation_path()
            elif choice == "4":
                self._analyze_product_clusters()
            elif choice == "5":
                self._view_similarity_stats()
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _add_product_similarity(self):
        """Add a product similarity relationship."""
        print("\n➕ ADD PRODUCT SIMILARITY")
        print("-" * 35)
        
        try:
            product1 = input("Product 1 ID: ").strip()
            product2 = input("Product 2 ID: ").strip()
            similarity = float(input("Similarity Score (0.0-1.0): ").strip())
            
            if not all([product1, product2]) or not 0.0 <= similarity <= 1.0:
                print("❌ Invalid input! Check product IDs and similarity score.")
                return
            
            self.engine.add_product_similarity(product1, product2, similarity)
            print(f"✅ Added similarity: {product1} ↔ {product2} ({similarity:.3f})")
            
        except ValueError:
            print("❌ Invalid similarity score! Please enter a number between 0.0 and 1.0.")
        except Exception as e:
            print(f"❌ Error adding similarity: {e}")
    
    def _find_similar_products(self):
        """Find products similar to a given product."""
        print("\n🔍 FIND SIMILAR PRODUCTS")
        print("-" * 30)
        
        product_id = input("Product ID: ").strip()
        if not product_id:
            print("❌ Product ID is required!")
            return
        
        try:
            min_similarity = float(input("Minimum Similarity (0.0-1.0, default 0.0): ").strip() or "0.0")
            max_results = int(input("Maximum Results (default 10): ").strip() or "10")
        except ValueError:
            print("❌ Invalid input! Using defaults.")
            min_similarity = 0.0
            max_results = 10
        
        # Get similar products
        similar_products = self.engine.similarity_graph.get_similar_products(
            product_id, min_similarity, max_results)
        
        if similar_products:
            print(f"\n✅ Found {len(similar_products)} similar products to '{product_id}':")
            for similar_product, score in similar_products:
                print(f"  • {similar_product}: {score:.3f} similarity")
        else:
            print(f"❌ No similar products found for '{product_id}'")
        
        # Try advanced similarity search
        print(f"\n🧠 Advanced similarity analysis (including transitive relationships):")
        advanced_similar = self.engine.similarity_graph.get_top_k_similar_products_advanced(
            product_id, k=max_results, use_transitive=True)
        
        if advanced_similar:
            print(f"Advanced results:")
            for product, score in advanced_similar:
                print(f"  • {product}: {score:.3f} combined similarity")
        else:
            print("No advanced similarities found.")
    
    def _find_recommendation_path(self):
        """Find a recommendation path between two products."""
        print("\n🛤️ FIND RECOMMENDATION PATH")
        print("-" * 35)
        
        start_product = input("Start Product ID: ").strip()
        target_product = input("Target Product ID: ").strip()
        
        if not start_product or not target_product:
            print("❌ Both product IDs are required!")
            return
        
        try:
            max_depth = int(input("Maximum Path Length (default 3): ").strip() or "3")
        except ValueError:
            max_depth = 3
        
        path = self.engine.similarity_graph.find_recommendation_path(
            start_product, target_product, max_depth)
        
        if path:
            print(f"\n✅ Found recommendation path:")
            print("   " + " → ".join(path))
            print(f"   Path length: {len(path)} products")
        else:
            print(f"❌ No recommendation path found between '{start_product}' and '{target_product}'")
    
    def _analyze_product_clusters(self):
        """Analyze product clusters in the similarity network."""
        print("\n🔍 PRODUCT CLUSTER ANALYSIS")
        print("-" * 40)
        
        try:
            min_similarity = float(input("Minimum Similarity for Clustering (default 0.7): ").strip() or "0.7")
        except ValueError:
            min_similarity = 0.7
        
        clusters = self.engine.similarity_graph.get_product_clusters(min_similarity)
        
        if clusters:
            print(f"\n✅ Found {len(clusters)} product clusters:")
            for i, cluster in enumerate(clusters, 1):
                print(f"\n  Cluster {i} ({len(cluster)} products):")
                for product in cluster:
                    print(f"    • {product}")
        else:
            print(f"❌ No clusters found with minimum similarity {min_similarity}")
    
    def _view_similarity_stats(self):
        """View similarity network statistics."""
        print("\n📊 SIMILARITY NETWORK STATISTICS")
        print("-" * 45)
        
        stats = self.engine.similarity_graph.get_graph_statistics()
        
        print(f"Total Products: {stats['products']}")
        print(f"Total Similarity Edges: {stats['edges']}")
        print(f"Network Density: {stats['density']:.4f}")
        print(f"Average Degree: {stats['average_degree']:.2f}")
        print(f"Maximum Degree: {stats['max_degree']}")
        
        if stats['degree_distribution']:
            print(f"\nDegree Distribution:")
            degree_counts = {}
            for degree in stats['degree_distribution']:
                degree_counts[degree] = degree_counts.get(degree, 0) + 1
            
            for degree in sorted(degree_counts.keys()):
                count = degree_counts[degree]
                print(f"  Degree {degree}: {count} products")
    
    def generate_recommendations_menu(self):
        """Handle recommendation generation."""
        while True:
            print("\n🎯 RECOMMENDATION GENERATION")
            print("-" * 40)
            print("1. Collaborative Filtering")
            print("2. Content-Based Filtering")
            print("3. Category-Based Recommendations")
            print("4. Behavior-Based Recommendations")
            print("5. Hybrid Recommendations (All Strategies)")
            print("6. Compare All Strategies")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self._generate_collaborative_recommendations()
            elif choice == "2":
                self._generate_content_recommendations()
            elif choice == "3":
                self._generate_category_recommendations()
            elif choice == "4":
                self._generate_behavior_recommendations()
            elif choice == "5":
                self._generate_hybrid_recommendations()
            elif choice == "6":
                self._compare_all_strategies()
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _generate_collaborative_recommendations(self):
        """Generate collaborative filtering recommendations."""
        print("\n🤝 COLLABORATIVE FILTERING RECOMMENDATIONS")
        print("-" * 50)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 5): ").strip() or "5")
        except ValueError:
            num_recs = 5
        
        start_time = time.time()
        recommendations = self.engine.get_collaborative_recommendations(user_id, num_recs)
        end_time = time.time()
        
        if recommendations:
            print(f"\n✅ Collaborative filtering recommendations for '{user_id}':")
            for item_id, predicted_rating in recommendations:
                print(f"  • {item_id}: {predicted_rating:.3f} predicted rating")
        else:
            print(f"❌ No collaborative recommendations found for '{user_id}'")
            print("   (This might happen if the user has no similar users)")
        
        print(f"\n⏱️ Generation time: {(end_time - start_time)*1000:.2f} ms")
    
    def _generate_content_recommendations(self):
        """Generate content-based filtering recommendations."""
        print("\n📄 CONTENT-BASED FILTERING RECOMMENDATIONS")
        print("-" * 50)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 5): ").strip() or "5")
        except ValueError:
            num_recs = 5
        
        start_time = time.time()
        recommendations = self.engine.get_content_based_recommendations(user_id, num_recs)
        end_time = time.time()
        
        if recommendations:
            print(f"\n✅ Content-based recommendations for '{user_id}':")
            for item_id, similarity_score in recommendations:
                print(f"  • {item_id}: {similarity_score:.3f} similarity score")
        else:
            print(f"❌ No content-based recommendations found for '{user_id}'")
            print("   (This might happen if the user has no highly-rated items with similarities)")
        
        print(f"\n⏱️ Generation time: {(end_time - start_time)*1000:.2f} ms")
    
    def _generate_category_recommendations(self):
        """Generate category-based recommendations."""
        print("\n🏷️ CATEGORY-BASED RECOMMENDATIONS")
        print("-" * 40)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 5): ").strip() or "5")
        except ValueError:
            num_recs = 5
        
        start_time = time.time()
        recommendations = self.engine.get_category_based_recommendations(user_id, num_recs)
        end_time = time.time()
        
        if recommendations:
            print(f"\n✅ Category-based recommendations for '{user_id}':")
            for item_id in recommendations:
                print(f"  • {item_id}")
        else:
            print(f"❌ No category-based recommendations found for '{user_id}'")
        
        print(f"\n⏱️ Generation time: {(end_time - start_time)*1000:.2f} ms")
    
    def _generate_behavior_recommendations(self):
        """Generate behavior-based recommendations."""
        print("\n📊 BEHAVIOR-BASED RECOMMENDATIONS")
        print("-" * 40)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 5): ").strip() or "5")
        except ValueError:
            num_recs = 5
        
        start_time = time.time()
        recommendations = self.engine.get_behavior_based_recommendations(user_id, num_recs)
        end_time = time.time()
        
        if recommendations:
            print(f"\n✅ Behavior-based recommendations for '{user_id}':")
            for item_id in recommendations:
                print(f"  • {item_id}")
        else:
            print(f"❌ No behavior-based recommendations found for '{user_id}'")
            print("   (This might happen if the user has no recent activity)")
        
        print(f"\n⏱️ Generation time: {(end_time - start_time)*1000:.2f} ms")
    
    def _generate_hybrid_recommendations(self):
        """Generate hybrid recommendations."""
        print("\n🎯 HYBRID RECOMMENDATIONS (ALL STRATEGIES)")
        print("-" * 50)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 10): ").strip() or "10")
        except ValueError:
            num_recs = 10
        
        start_time = time.time()
        recommendations = self.engine.get_hybrid_recommendations(user_id, num_recs)
        end_time = time.time()
        
        if recommendations:
            print(f"\n✅ Hybrid recommendations for '{user_id}':")
            print("   (Combined using weighted scoring from all strategies)")
            print()
            
            for i, (item_id, combined_score, strategy_breakdown) in enumerate(recommendations, 1):
                print(f"  {i}. {item_id}: {combined_score:.3f} combined score")
                
                # Show strategy breakdown
                strategies = []
                for strategy, score in strategy_breakdown.items():
                    strategies.append(f"{strategy}={score:.2f}")
                print(f"     Strategies: {', '.join(strategies)}")
                print()
        else:
            print(f"❌ No hybrid recommendations found for '{user_id}'")
        
        print(f"⏱️ Generation time: {(end_time - start_time)*1000:.2f} ms")
    
    def _compare_all_strategies(self):
        """Compare all recommendation strategies side by side."""
        print("\n📊 STRATEGY COMPARISON")
        print("-" * 30)
        
        user_id = input("User ID: ").strip()
        if not user_id:
            print("❌ User ID is required!")
            return
        
        try:
            num_recs = int(input("Number of recommendations per strategy (default 5): ").strip() or "5")
        except ValueError:
            num_recs = 5
        
        print(f"\n🔍 Comparing recommendation strategies for '{user_id}':")
        print("=" * 80)
        
        strategies = [
            ("Collaborative Filtering", self.engine.get_collaborative_recommendations),
            ("Content-Based Filtering", self.engine.get_content_based_recommendations),
            ("Category-Based", self.engine.get_category_based_recommendations),
            ("Behavior-Based", self.engine.get_behavior_based_recommendations),
        ]
        
        results = {}
        
        for strategy_name, strategy_func in strategies:
            start_time = time.time()
            try:
                recs = strategy_func(user_id, num_recs)
                end_time = time.time()
                results[strategy_name] = {
                    'recommendations': recs,
                    'time': (end_time - start_time) * 1000,
                    'count': len(recs) if recs else 0
                }
            except Exception as e:
                results[strategy_name] = {
                    'recommendations': [],
                    'time': 0,
                    'count': 0,
                    'error': str(e)
                }
        
        # Display results
        for strategy_name, result in results.items():
            print(f"\n🎯 {strategy_name}:")
            print(f"   Count: {result['count']} recommendations")
            print(f"   Time: {result['time']:.2f} ms")
            
            if 'error' in result:
                print(f"   ❌ Error: {result['error']}")
            elif result['recommendations']:
                print("   Results:")
                for item in result['recommendations'][:3]:  # Show top 3
                    if isinstance(item, tuple):
                        if len(item) == 2:
                            print(f"     • {item[0]}: {item[1]:.3f}")
                        else:
                            print(f"     • {item[0]}")
                    else:
                        print(f"     • {item}")
                if len(result['recommendations']) > 3:
                    print(f"     ... and {len(result['recommendations']) - 3} more")
            else:
                print("   ❌ No recommendations found")
        
        # Generate hybrid for comparison
        print(f"\n🎯 Hybrid (Combined):")
        start_time = time.time()
        hybrid_recs = self.engine.get_hybrid_recommendations(user_id, num_recs)
        end_time = time.time()
        
        print(f"   Count: {len(hybrid_recs)} recommendations")
        print(f"   Time: {(end_time - start_time)*1000:.2f} ms")
        if hybrid_recs:
            print("   Top 3 Results:")
            for i, (item_id, score, _) in enumerate(hybrid_recs[:3], 1):
                print(f"     {i}. {item_id}: {score:.3f}")
    
    def system_statistics_menu(self):
        """Display comprehensive system statistics."""
        print("\n📈 SYSTEM STATISTICS")
        print("-" * 30)
        
        if not self.demo_data_loaded:
            print("⚠️ Demo data not loaded. Statistics may be limited.")
            print("Consider loading demo data first (Option 1 from main menu).")
        
        stats = self.engine.get_system_statistics()
        
        print(f"\n🏗️ DATA STRUCTURE STATISTICS:")
        print("-" * 40)
        
        # Hash Table Statistics
        ui_stats = stats['user_item_interactions']
        print(f"📊 User-Item Hash Table:")
        print(f"   • Total interactions: {ui_stats['size']}")
        print(f"   • Table capacity: {ui_stats['capacity']}")
        print(f"   • Load factor: {ui_stats['load_factor']:.3f}")
        print(f"   • Average bucket size: {ui_stats['avg_bucket_size']:.2f}")
        print(f"   • Max bucket size: {ui_stats['max_bucket_size']}")
        print(f"   • Empty buckets: {ui_stats['empty_buckets']}")
        
        # Graph Statistics
        graph_stats = stats['product_similarities']
        print(f"\n🔗 Product Similarity Graph:")
        print(f"   • Total products: {graph_stats['products']}")
        print(f"   • Total edges: {graph_stats['edges']}")
        print(f"   • Graph density: {graph_stats['density']:.4f}")
        print(f"   • Average degree: {graph_stats['average_degree']:.2f}")
        print(f"   • Maximum degree: {graph_stats['max_degree']}")
        
        # Tree Statistics
        tree_stats = stats['behavior_tracking']
        print(f"\n🌳 User Behavior Tree:")
        print(f"   • Total records: {tree_stats['size']}")
        print(f"   • Tree height: {tree_stats['height']}")
        print(f"   • Is balanced: {'✅ Yes' if tree_stats['is_balanced'] else '❌ No'}")
        print(f"   • Balance factor: {tree_stats['balance_factor']}")
        
        # Category Tree Statistics
        cat_stats = stats['category_hierarchy']
        print(f"\n🏷️ Category Hierarchy:")
        print(f"   • Total categories: {cat_stats['total_categories']}")
        print(f"   • Total products: {cat_stats['total_products']}")
        print(f"   • Tree depth: {cat_stats['max_depth']}")
        print(f"   • Leaf categories: {cat_stats['leaf_categories']}")
        print(f"   • Avg products per category: {cat_stats['avg_products_per_category']:.2f}")
        
        # Performance Statistics
        print(f"\n⚡ PERFORMANCE STATISTICS:")
        print("-" * 30)
        print(f"   • Cache entries: {stats['cache_size']}")
        
        # Run quick performance test
        if self.demo_data_loaded:
            print("\n🏃 QUICK PERFORMANCE TEST:")
            test_user = "alice_tech"
            
            start_time = time.time()
            hybrid_recs = self.engine.get_hybrid_recommendations(test_user, 10)
            first_call = (time.time() - start_time) * 1000
            
            start_time = time.time()
            cached_recs = self.engine.get_hybrid_recommendations(test_user, 10)
            second_call = (time.time() - start_time) * 1000
            
            print(f"   • First hybrid recommendation call: {first_call:.2f} ms")
            print(f"   • Cached recommendation call: {second_call:.2f} ms")
            print(f"   • Cache speedup: {first_call/second_call:.1f}x" if second_call > 0 else "")
            print(f"   • Recommendations generated: {len(hybrid_recs)}")
    
    def run_test_suite(self):
        """Run the comprehensive test suite."""
        print("\n🧪 RUNNING TEST SUITE")
        print("-" * 30)
        print("This will run comprehensive tests on all data structures...")
        print("Test results will show the robustness of the implementation.")
        
        confirm = input("\nProceed with test suite? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Test suite cancelled.")
            return
        
        try:
            # Import and run the test suite
            from test_comprehensive import run_comprehensive_tests
            
            print("\n" + "="*80)
            print("STARTING COMPREHENSIVE TEST SUITE")
            print("="*80)
            
            total_tests, failures, errors = run_comprehensive_tests()
            
            print(f"\n{'='*80}")
            print("TEST SUITE COMPLETED")
            print(f"{'='*80}")
            
            if failures == 0 and errors == 0:
                print("🎉 ALL TESTS PASSED! System is working perfectly.")
            else:
                print(f"⚠️ Some tests failed. Review the output above for details.")
            
        except ImportError:
            print("❌ Test suite not found! Make sure test_comprehensive.py is available.")
        except Exception as e:
            print(f"❌ Error running test suite: {e}")
    
    def data_import_export_menu(self):
        """Handle data import/export functionality."""
        while True:
            print("\n💾 DATA IMPORT/EXPORT")
            print("-" * 30)
            print("1. Export Current Data")
            print("2. Import Data from File")
            print("3. Reset All Data")
            print("4. Save System State")
            print("0. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self._export_data()
            elif choice == "2":
                self._import_data()
            elif choice == "3":
                self._reset_data()
            elif choice == "4":
                self._save_system_state()
            elif choice == "0":
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def _export_data(self):
        """Export current system data to JSON."""
        print("\n📤 EXPORT DATA")
        print("-" * 20)
        
        filename = input("Export filename (default: recommendation_data.json): ").strip()
        if not filename:
            filename = "recommendation_data.json"
        
        try:
            # Collect all data
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'interactions': [],
                'similarities': [],
                'categories': {},
                'products': {}
            }
            
            # Export interactions
            for bucket in self.engine.user_item_table.buckets:
                for user_id, item_id, data in bucket:
                    export_data['interactions'].append({
                        'user_id': user_id,
                        'item_id': item_id,
                        'rating': data['rating'],
                        'action': data['action'],
                        'timestamp': data['timestamp']
                    })
            
            # Export similarities
            for product_id, neighbors in self.engine.similarity_graph.graph.items():
                for neighbor_id, similarity in neighbors:
                    # Only export each edge once
                    if product_id < neighbor_id:
                        export_data['similarities'].append({
                            'product1': product_id,
                            'product2': neighbor_id,
                            'similarity': similarity
                        })
            
            # Export categories and products
            for cat_id, cat_node in self.engine.category_tree.category_index.items():
                export_data['categories'][cat_id] = {
                    'name': cat_node.category_name,
                    'parent': cat_node.parent.category_id if cat_node.parent else None,
                    'products': list(cat_node.products)
                }
            
            # Save to file
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✅ Data exported successfully to: {filepath}")
            print(f"   • Interactions: {len(export_data['interactions'])}")
            print(f"   • Similarities: {len(export_data['similarities'])}")
            print(f"   • Categories: {len(export_data['categories'])}")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def _import_data(self):
        """Import data from JSON file."""
        print("\n📥 IMPORT DATA")
        print("-" * 20)
        
        filename = input("Import filename: ").strip()
        if not filename:
            print("❌ Filename is required!")
            return
        
        try:
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            print("⚠️ This will overwrite current data. Continue? (y/N): ", end="")
            confirm = input().strip().lower()
            if confirm != 'y':
                print("❌ Import cancelled.")
                return
            
            # Reset current data
            self.engine = RecommendationEngine()
            
            # Import categories first
            print("Importing categories...")
            for cat_id, cat_data in import_data.get('categories', {}).items():
                if cat_data['parent']:
                    self.engine.category_tree.add_category(
                        cat_id, cat_data['name'], cat_data['parent'])
                else:
                    self.engine.category_tree.add_category(cat_id, cat_data['name'])
                
                # Add products to category
                for product_id in cat_data['products']:
                    self.engine.add_product_to_category(product_id, cat_id)
            
            # Import similarities
            print("Importing similarities...")
            for sim in import_data.get('similarities', []):
                self.engine.add_product_similarity(
                    sim['product1'], sim['product2'], sim['similarity'])
            
            # Import interactions
            print("Importing interactions...")
            for interaction in import_data.get('interactions', []):
                self.engine.add_user_interaction(
                    interaction['user_id'], interaction['item_id'],
                    interaction['rating'], interaction['action'])
            
            print(f"✅ Data imported successfully from: {filepath}")
            print(f"   • Interactions: {len(import_data.get('interactions', []))}")
            print(f"   • Similarities: {len(import_data.get('similarities', []))}")
            print(f"   • Categories: {len(import_data.get('categories', {}))}")
            
            self.demo_data_loaded = True
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except json.JSONDecodeError:
            print("❌ Invalid JSON file!")
        except Exception as e:
            print(f"❌ Error importing data: {e}")
    
    def _reset_data(self):
        """Reset all system data."""
        print("\n🔄 RESET ALL DATA")
        print("-" * 20)
        
        print("⚠️ This will delete ALL current data. This action cannot be undone!")
        confirm = input("Type 'RESET' to confirm: ").strip()
        
        if confirm == 'RESET':
            self.engine = RecommendationEngine()
            self.demo_data_loaded = False
            print("✅ All data has been reset.")
        else:
            print("❌ Reset cancelled.")
    
    def _save_system_state(self):
        """Save current system state with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_state_{timestamp}.json"
        
        print(f"\n💾 Saving system state to: {filename}")
        
        # Use the export functionality with automatic filename
        original_input = input
        input_responses = iter([filename])
        
        def mock_input(prompt):
            try:
                return next(input_responses)
            except StopIteration:
                return ""
        
        # Temporarily replace input function
        import builtins
        builtins.input = mock_input
        
        try:
            self._export_data()
        finally:
            # Restore original input function
            builtins.input = original_input
    
    def run(self):
        """Run the interactive CLI."""
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip()
            
            try:
                if choice == "1":
                    self.load_demo_data()
                elif choice == "2":
                    self.user_interaction_menu()
                elif choice == "3":
                    self.product_similarity_menu()
                elif choice == "4":
                    # Behavior analysis - simple implementation
                    print("\n📊 BEHAVIOR ANALYSIS")
                    print("(Feature available through User Interaction Management)")
                    input("\nPress Enter to continue...")
                elif choice == "5":
                    # Category management - simple implementation
                    print("\n🏷️ CATEGORY MANAGEMENT")
                    print("Categories are managed through the system setup.")
                    print("View category statistics in System Statistics menu.")
                    input("\nPress Enter to continue...")
                elif choice == "6":
                    self.generate_recommendations_menu()
                elif choice == "7":
                    self.system_statistics_menu()
                elif choice == "8":
                    self.run_test_suite()
                elif choice == "9":
                    self.data_import_export_menu()
                elif choice == "0":
                    print("\n👋 Thank you for using the E-Commerce Recommendation System!")
                    print("Phase 2 Proof of Concept demonstration completed.")
                    break
                else:
                    print("❌ Invalid choice! Please select a number from 0-9.")
                
                if choice != "0":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Please try again or contact support if the problem persists.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point for the CLI application."""
    try:
        cli = RecommendationSystemCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your installation and try again.")


if __name__ == "__main__":
    main()