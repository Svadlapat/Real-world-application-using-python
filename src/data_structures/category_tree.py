"""
Category Hierarchy Tree Implementation
N-ary tree for representing product categories in hierarchical structure

This module implements a tree structure for organizing products by categories,
enabling efficient category-based filtering and hierarchical recommendations.
"""


class CategoryNode:
    """
    Node class for the Category Hierarchy Tree.
    
    Each node represents a product category with potential subcategories.
    """
    
    def __init__(self, category_id, category_name, parent=None):
        """
        Initialize a category node.
        
        Args:
            category_id (str): Unique category identifier
            category_name (str): Human-readable category name
            parent (CategoryNode): Parent category node
        """
        self.category_id = category_id
        self.category_name = category_name
        self.parent = parent
        self.children = []  # List of child CategoryNode objects
        self.products = set()  # Set of product IDs in this category
        self.metadata = {}  # Additional category information
    
    def add_child(self, child_node):
        """Add a child category."""
        child_node.parent = self
        self.children.append(child_node)
    
    def add_product(self, product_id):
        """Add a product to this category."""
        self.products.add(product_id)
    
    def remove_product(self, product_id):
        """Remove a product from this category."""
        self.products.discard(product_id)
    
    def get_depth(self):
        """Get the depth of this node in the tree."""
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth
    
    def get_path_from_root(self):
        """Get the path from root to this node."""
        path = []
        current = self
        while current is not None:
            path.append(current.category_name)
            current = current.parent
        return path[::-1]  # Reverse to get root-to-node path
    
    def __str__(self):
        """String representation of the category."""
        return f"{self.category_name} ({len(self.products)} products)"


class CategoryHierarchyTree:
    """
    N-ary tree implementation for product category hierarchy.
    
    Supports hierarchical organization of products, category-based searches,
    and navigation through the category structure.
    """
    
    def __init__(self, root_name="Root"):
        """
        Initialize the category hierarchy tree.
        
        Args:
            root_name (str): Name for the root category
        """
        self.root = CategoryNode("root", root_name)
        self.category_index = {"root": self.root}  # Fast lookup by category_id
        self.total_categories = 1
        self.total_products = 0
    
    def add_category(self, category_id, category_name, parent_id="root"):
        """
        Add a new category to the hierarchy.
        
        Args:
            category_id (str): Unique identifier for the new category
            category_name (str): Human-readable name
            parent_id (str): ID of the parent category
            
        Returns:
            CategoryNode: The created category node
            
        Time Complexity: O(1) with index lookup
        """
        if category_id in self.category_index:
            raise ValueError(f"Category {category_id} already exists")
        
        if parent_id not in self.category_index:
            raise ValueError(f"Parent category {parent_id} does not exist")
        
        parent_node = self.category_index[parent_id]
        new_category = CategoryNode(category_id, category_name, parent_node)
        
        parent_node.add_child(new_category)
        self.category_index[category_id] = new_category
        self.total_categories += 1
        
        return new_category
    
    def add_product_to_category(self, product_id, category_id):
        """
        Add a product to a specific category.
        
        Args:
            product_id (str): Product identifier
            category_id (str): Category identifier
            
        Time Complexity: O(1)
        """
        if category_id not in self.category_index:
            raise ValueError(f"Category {category_id} does not exist")
        
        category_node = self.category_index[category_id]
        if product_id not in category_node.products:
            category_node.add_product(product_id)
            self.total_products += 1
    
    def get_products_in_category(self, category_id, include_subcategories=True):
        """
        Get all products in a category and optionally its subcategories.
        
        Args:
            category_id (str): Category to search
            include_subcategories (bool): Whether to include child categories
            
        Returns:
            set: Set of product IDs
            
        Time Complexity: O(k) where k is number of subcategories
        """
        if category_id not in self.category_index:
            return set()
        
        category_node = self.category_index[category_id]
        products = set(category_node.products)
        
        if include_subcategories:
            # Recursively get products from all subcategories
            for child in category_node.children:
                child_products = self.get_products_in_category(
                    child.category_id, include_subcategories=True
                )
                products.update(child_products)
        
        return products
    
    def find_category_by_name(self, category_name, case_sensitive=False):
        """
        Find categories by name (supports partial matching).
        
        Args:
            category_name (str): Name to search for
            case_sensitive (bool): Whether search is case sensitive
            
        Returns:
            list: List of matching CategoryNode objects
        """
        matches = []
        search_name = category_name if case_sensitive else category_name.lower()
        
        for category_node in self.category_index.values():
            node_name = (category_node.category_name if case_sensitive 
                        else category_node.category_name.lower())
            
            if search_name in node_name:
                matches.append(category_node)
        
        return matches
    
    def get_category_recommendations(self, product_id, max_recommendations=10):
        """
        Get category-based product recommendations.
        
        Finds other products in the same category and related categories.
        
        Args:
            product_id (str): Product to base recommendations on
            max_recommendations (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended product IDs
        """
        # Find which category the product belongs to
        product_category = None
        for category_node in self.category_index.values():
            if product_id in category_node.products:
                product_category = category_node
                break
        
        if product_category is None:
            return []
        
        recommendations = set()
        
        # Add products from same category
        same_category_products = product_category.products - {product_id}
        recommendations.update(same_category_products)
        
        # Add products from sibling categories
        if product_category.parent:
            for sibling in product_category.parent.children:
                if sibling != product_category:
                    recommendations.update(sibling.products)
        
        # Add products from parent category (if not root)
        if (product_category.parent and 
            product_category.parent != self.root):
            parent_products = product_category.parent.products - {product_id}
            recommendations.update(parent_products)
        
        return list(recommendations)[:max_recommendations]
    
    def get_category_path(self, category_id):
        """
        Get the full path from root to the specified category.
        
        Args:
            category_id (str): Category identifier
            
        Returns:
            list: List of category names from root to target
        """
        if category_id not in self.category_index:
            return []
        
        category_node = self.category_index[category_id]
        return category_node.get_path_from_root()
    
    def get_subcategories(self, category_id, depth=1):
        """
        Get subcategories of a given category up to specified depth.
        
        Args:
            category_id (str): Parent category ID
            depth (int): Maximum depth to traverse (1 = direct children only)
            
        Returns:
            list: List of CategoryNode objects
        """
        if category_id not in self.category_index:
            return []
        
        category_node = self.category_index[category_id]
        subcategories = []
        
        def collect_subcategories(node, current_depth):
            if current_depth > depth:
                return
            
            for child in node.children:
                subcategories.append(child)
                if current_depth < depth:
                    collect_subcategories(child, current_depth + 1)
        
        collect_subcategories(category_node, 1)
        return subcategories
    
    def display_tree(self, category_id="root", max_depth=None):
        """
        Display the category tree structure.
        
        Args:
            category_id (str): Root category for display
            max_depth (int): Maximum depth to display
            
        Returns:
            str: String representation of the tree
        """
        if category_id not in self.category_index:
            return "Category not found"
        
        result = []
        
        def display_recursive(node, depth=0, prefix=""):
            if max_depth is not None and depth > max_depth:
                return
            
            indent = "  " * depth
            result.append(f"{indent}{prefix}{node}")
            
            for i, child in enumerate(node.children):
                is_last = i == len(node.children) - 1
                child_prefix = "└── " if is_last else "├── "
                display_recursive(child, depth + 1, child_prefix)
        
        root_node = self.category_index[category_id]
        display_recursive(root_node)
        
        return "\n".join(result)
    
    def get_tree_statistics(self):
        """
        Get comprehensive statistics about the category tree.
        
        Returns:
            dict: Tree statistics including depth, branching factor, etc.
        """
        max_depth = 0
        leaf_categories = 0
        category_product_counts = []
        
        def analyze_recursive(node, depth=0):
            nonlocal max_depth, leaf_categories
            
            max_depth = max(max_depth, depth)
            category_product_counts.append(len(node.products))
            
            if not node.children:
                leaf_categories += 1
            
            for child in node.children:
                analyze_recursive(child, depth + 1)
        
        analyze_recursive(self.root)
        
        avg_products_per_category = (sum(category_product_counts) / 
                                   len(category_product_counts) 
                                   if category_product_counts else 0)
        
        return {
            "total_categories": self.total_categories,
            "total_products": self.total_products,
            "max_depth": max_depth,
            "leaf_categories": leaf_categories,
            "avg_products_per_category": avg_products_per_category,
            "category_product_distribution": category_product_counts
        }


# Example usage and testing
if __name__ == "__main__":
    # Create category hierarchy
    category_tree = CategoryHierarchyTree("E-commerce Store")
    
    # Build sample category structure
    # Electronics
    electronics = category_tree.add_category("electronics", "Electronics")
    computers = category_tree.add_category("computers", "Computers", "electronics")
    phones = category_tree.add_category("phones", "Mobile Phones", "electronics")
    
    # Computer subcategories
    laptops = category_tree.add_category("laptops", "Laptops", "computers")
    desktops = category_tree.add_category("desktops", "Desktops", "computers")
    
    # Clothing
    clothing = category_tree.add_category("clothing", "Clothing")
    mens_clothing = category_tree.add_category("mens", "Men's Clothing", "clothing")
    womens_clothing = category_tree.add_category("womens", "Women's Clothing", "clothing")
    
    # Add sample products
    products_data = [
        ("laptop_001", "laptops"),
        ("laptop_002", "laptops"),
        ("desktop_001", "desktops"),
        ("phone_001", "phones"),
        ("phone_002", "phones"),
        ("shirt_001", "mens"),
        ("dress_001", "womens"),
    ]
    
    for product_id, category_id in products_data:
        category_tree.add_product_to_category(product_id, category_id)
    
    print("Category Hierarchy Tree Demo")
    print("=" * 40)
    
    # Display tree structure
    print("Category Tree Structure:")
    print(category_tree.display_tree())
    print()
    
    # Get products in category
    electronics_products = category_tree.get_products_in_category("electronics")
    print(f"Products in Electronics category: {electronics_products}")
    
    # Get recommendations
    recommendations = category_tree.get_category_recommendations("laptop_001")
    print(f"Recommendations for laptop_001: {recommendations}")
    
    # Get category path
    path = category_tree.get_category_path("laptops")
    print(f"Path to laptops category: {' > '.join(path)}")
    
    # Tree statistics
    stats = category_tree.get_tree_statistics()
    print(f"Tree statistics: {stats}")