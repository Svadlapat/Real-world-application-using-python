"""
User Behavior Tree Implementation
Binary Search Tree for efficient user activity tracking and temporal queries

This module implements a BST to store user interactions ordered by timestamp,
enabling efficient range queries and temporal analysis.
"""

from datetime import datetime, timedelta


class BehaviorNode:
    """
    Node class for the User Behavior Tree.
    
    Each node represents a user interaction with timestamp-based ordering.
    """
    
    def __init__(self, user_id, item_id, timestamp, action_type, metadata=None):
        """
        Initialize a behavior node.
        
        Args:
            user_id (str): User identifier
            item_id (str): Item identifier  
            timestamp (datetime): When the interaction occurred
            action_type (str): Type of action (view, purchase, cart_add, etc.)
            metadata (dict): Additional interaction data
        """
        self.user_id = user_id
        self.item_id = item_id
        self.timestamp = timestamp
        self.action_type = action_type
        self.metadata = metadata or {}
        self.left = None
        self.right = None
        
    def __str__(self):
        """String representation of the node."""
        return f"{self.user_id}:{self.item_id}:{self.action_type}@{self.timestamp}"


class UserBehaviorTree:
    """
    Binary Search Tree for storing and querying user behavior data.
    
    Organizes interactions by timestamp for efficient temporal queries.
    Supports range searches, recent activity lookups, and behavior analysis.
    """
    
    def __init__(self):
        """Initialize empty behavior tree."""
        self.root = None
        self.size = 0
    
    def insert(self, user_id, item_id, timestamp, action_type, metadata=None):
        """
        Insert a new user behavior record.
        
        Args:
            user_id (str): User identifier
            item_id (str): Item identifier
            timestamp (datetime): Interaction timestamp
            action_type (str): Action type
            metadata (dict): Additional data
            
        Time Complexity: O(log n) average, O(n) worst case
        """
        new_node = BehaviorNode(user_id, item_id, timestamp, 
                               action_type, metadata)
        
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)
        
        self.size += 1
    
    def _insert_recursive(self, current, new_node):
        """
        Recursive helper for insertion.
        
        Orders nodes by timestamp (earlier timestamps go left).
        """
        if new_node.timestamp <= current.timestamp:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursive(current.right, new_node)
    
    def search_by_timestamp(self, target_timestamp):
        """
        Search for interactions at a specific timestamp.
        
        Args:
            target_timestamp (datetime): Timestamp to search for
            
        Returns:
            list: List of BehaviorNode objects at that timestamp
            
        Time Complexity: O(log n + k) where k is number of matches
        """
        results = []
        self._search_timestamp_recursive(self.root, target_timestamp, results)
        return results
    
    def _search_timestamp_recursive(self, node, target_timestamp, results):
        """Recursive helper for timestamp search."""
        if node is None:
            return
        
        if node.timestamp == target_timestamp:
            results.append(node)
            # Check both subtrees as there might be multiple entries
            # at the same timestamp
            self._search_timestamp_recursive(node.left, target_timestamp, results)
            self._search_timestamp_recursive(node.right, target_timestamp, results)
        elif target_timestamp < node.timestamp:
            self._search_timestamp_recursive(node.left, target_timestamp, results)
        else:
            self._search_timestamp_recursive(node.right, target_timestamp, results)
    
    def get_interactions_in_range(self, start_time, end_time):
        """
        Get all interactions within a time range.
        
        Args:
            start_time (datetime): Range start
            end_time (datetime): Range end
            
        Returns:
            list: List of BehaviorNode objects in the time range
            
        Time Complexity: O(log n + k) where k is number of results
        """
        results = []
        self._range_search_recursive(self.root, start_time, end_time, results)
        return results
    
    def _range_search_recursive(self, node, start_time, end_time, results):
        """Recursive helper for range search."""
        if node is None:
            return
        
        # If current node is in range, add it
        if start_time <= node.timestamp <= end_time:
            results.append(node)
        
        # Recursively search left subtree if it might contain valid nodes
        if node.timestamp > start_time:
            self._range_search_recursive(node.left, start_time, end_time, results)
        
        # Recursively search right subtree if it might contain valid nodes
        if node.timestamp < end_time:
            self._range_search_recursive(node.right, start_time, end_time, results)
    
    def get_recent_activity(self, user_id=None, hours=24, action_types=None):
        """
        Get recent user activity within specified time window.
        
        Args:
            user_id (str): Specific user ID (None for all users)
            hours (int): Number of hours to look back
            action_types (list): Filter by specific action types
            
        Returns:
            list: Recent behavior nodes matching criteria
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        recent_interactions = self.get_interactions_in_range(start_time, end_time)
        
        # Filter by user_id if specified
        if user_id:
            recent_interactions = [node for node in recent_interactions 
                                 if node.user_id == user_id]
        
        # Filter by action types if specified
        if action_types:
            recent_interactions = [node for node in recent_interactions 
                                 if node.action_type in action_types]
        
        return recent_interactions
    
    def get_user_behavior_pattern(self, user_id, days=30):
        """
        Analyze user behavior patterns over a time period.
        
        Args:
            user_id (str): User to analyze
            days (int): Number of days to analyze
            
        Returns:
            dict: Behavior analysis including action counts, frequency, etc.
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        user_interactions = []
        all_interactions = self.get_interactions_in_range(start_time, end_time)
        
        for node in all_interactions:
            if node.user_id == user_id:
                user_interactions.append(node)
        
        if not user_interactions:
            return {"total_interactions": 0, "action_counts": {}, 
                   "most_active_day": None, "favorite_items": []}
        
        # Analyze action types
        action_counts = {}
        item_interactions = {}
        daily_activity = {}
        
        for interaction in user_interactions:
            # Count action types
            action_counts[interaction.action_type] = \
                action_counts.get(interaction.action_type, 0) + 1
            
            # Count item interactions
            item_interactions[interaction.item_id] = \
                item_interactions.get(interaction.item_id, 0) + 1
            
            # Count daily activity
            day_key = interaction.timestamp.date()
            daily_activity[day_key] = daily_activity.get(day_key, 0) + 1
        
        # Find most active day
        most_active_day = max(daily_activity.items(), 
                            key=lambda x: x[1])[0] if daily_activity else None
        
        # Find favorite items (top 5)
        favorite_items = sorted(item_interactions.items(), 
                              key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_interactions": len(user_interactions),
            "action_counts": action_counts,
            "most_active_day": most_active_day,
            "favorite_items": favorite_items,
            "daily_activity": daily_activity,
            "time_range": f"{start_time.date()} to {end_time.date()}"
        }
    
    def inorder_traversal(self):
        """
        Get all interactions in chronological order.
        
        Returns:
            list: All behavior nodes sorted by timestamp
            
        Time Complexity: O(n)
        """
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive helper for inorder traversal."""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node)
            self._inorder_recursive(node.right, result)
    
    def get_statistics(self):
        """
        Get tree statistics and performance metrics.
        
        Returns:
            dict: Tree statistics including size, height, balance info
        """
        if self.root is None:
            return {"size": 0, "height": 0, "is_balanced": True}
        
        height = self._calculate_height(self.root)
        is_balanced = self._is_balanced(self.root)
        
        return {
            "size": self.size,
            "height": height,
            "is_balanced": is_balanced,
            "balance_factor": self._get_balance_factor(self.root)
        }
    
    def _calculate_height(self, node):
        """Calculate the height of a subtree."""
        if node is None:
            return 0
        return 1 + max(self._calculate_height(node.left),
                      self._calculate_height(node.right))
    
    def _is_balanced(self, node):
        """Check if the tree is balanced."""
        if node is None:
            return True
        
        left_height = self._calculate_height(node.left)
        right_height = self._calculate_height(node.right)
        
        return (abs(left_height - right_height) <= 1 and
                self._is_balanced(node.left) and
                self._is_balanced(node.right))
    
    def _get_balance_factor(self, node):
        """Get the balance factor of a node."""
        if node is None:
            return 0
        return (self._calculate_height(node.left) - 
                self._calculate_height(node.right))


# Example usage and testing
if __name__ == "__main__":
    # Create behavior tree
    behavior_tree = UserBehaviorTree()
    
    # Sample behavior data
    base_time = datetime.now() - timedelta(days=5)
    
    sample_behaviors = [
        ("user_001", "item_101", base_time + timedelta(hours=1), "view"),
        ("user_001", "item_101", base_time + timedelta(hours=2), "cart_add"),
        ("user_001", "item_102", base_time + timedelta(hours=3), "view"),
        ("user_002", "item_101", base_time + timedelta(hours=4), "purchase"),
        ("user_001", "item_101", base_time + timedelta(hours=5), "purchase"),
        ("user_003", "item_103", base_time + timedelta(hours=6), "view"),
        ("user_002", "item_102", base_time + timedelta(days=1), "view"),
        ("user_001", "item_104", base_time + timedelta(days=2), "wishlist_add"),
    ]
    
    # Insert sample data
    for user_id, item_id, timestamp, action_type in sample_behaviors:
        behavior_tree.insert(user_id, item_id, timestamp, action_type)
    
    print("User Behavior Tree Demo")
    print("=" * 40)
    
    # Recent activity
    recent = behavior_tree.get_recent_activity(hours=168)  # Last week
    print(f"Recent activity (last week): {len(recent)} interactions")
    
    # User behavior pattern
    pattern = behavior_tree.get_user_behavior_pattern("user_001", days=7)
    print(f"User_001 behavior pattern: {pattern}")
    
    # Range query
    range_start = base_time
    range_end = base_time + timedelta(hours=6)
    range_results = behavior_tree.get_interactions_in_range(range_start, range_end)
    print(f"Interactions in first 6 hours: {len(range_results)}")
    
    # Tree statistics
    stats = behavior_tree.get_statistics()
    print(f"Tree statistics: {stats}")