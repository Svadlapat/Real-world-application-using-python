"""
Hash Table Implementation for User-Item Interaction Matrix
Optimized for e-commerce recommendation system

This module implements a custom hash table to store and efficiently retrieve
user-item interaction data such as ratings, purchases, and browsing history.
"""

class UserItemHashTable:
    """
    Custom hash table implementation for storing user-item interactions.
    
    Uses separate chaining for collision resolution and dynamic resizing
    to maintain optimal performance as the dataset grows.
    """
    
    def __init__(self, initial_capacity=1000):
        """
        Initialize the hash table with specified capacity.
        
        Args:
            initial_capacity (int): Initial size of the hash table
        """
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash_function(self, user_id, item_id):
        """
        Custom hash function for user-item pairs.
        
        Combines user_id and item_id to create a unique hash value.
        Uses polynomial rolling hash for better distribution.
        
        Args:
            user_id (str/int): Unique user identifier
            item_id (str/int): Unique item identifier
            
        Returns:
            int: Hash value for the user-item pair
        """
        # Convert to strings if they aren't already
        user_str = str(user_id)
        item_str = str(item_id)
        
        # Combine user and item IDs
        combined = f"{user_str}#{item_str}"
        
        # Polynomial rolling hash
        hash_value = 0
        base = 31
        for char in combined:
            hash_value = (hash_value * base + ord(char)) % self.capacity
        
        return hash_value
    
    def _resize(self):
        """
        Resize the hash table when load factor exceeds threshold.
        
        Doubles the capacity and rehashes all existing entries.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        # Rehash all existing entries
        for bucket in old_buckets:
            for user_id, item_id, interaction_data in bucket:
                self.insert(user_id, item_id, interaction_data)
    
    def insert(self, user_id, item_id, interaction_data):
        """
        Insert or update user-item interaction data.
        
        Args:
            user_id (str/int): User identifier
            item_id (str/int): Item identifier
            interaction_data (dict): Interaction details (rating, timestamp, etc.)
        
        Time Complexity: O(1) average, O(n) worst case
        """
        # Check if resize is needed
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        hash_index = self._hash_function(user_id, item_id)
        bucket = self.buckets[hash_index]
        
        # Check if entry already exists and update it
        for i, (existing_user, existing_item, existing_data) in enumerate(bucket):
            if existing_user == user_id and existing_item == item_id:
                bucket[i] = (user_id, item_id, interaction_data)
                return
        
        # Add new entry
        bucket.append((user_id, item_id, interaction_data))
        self.size += 1
    
    def get(self, user_id, item_id):
        """
        Retrieve interaction data for a user-item pair.
        
        Args:
            user_id (str/int): User identifier
            item_id (str/int): Item identifier
            
        Returns:
            dict: Interaction data if found, None otherwise
            
        Time Complexity: O(1) average, O(n) worst case
        """
        hash_index = self._hash_function(user_id, item_id)
        bucket = self.buckets[hash_index]
        
        for existing_user, existing_item, interaction_data in bucket:
            if existing_user == user_id and existing_item == item_id:
                return interaction_data
        
        return None
    
    def get_user_interactions(self, user_id):
        """
        Get all interactions for a specific user.
        
        Args:
            user_id (str/int): User identifier
            
        Returns:
            list: List of (item_id, interaction_data) tuples
            
        Time Complexity: O(n) where n is total number of interactions
        """
        user_interactions = []
        
        for bucket in self.buckets:
            for existing_user, item_id, interaction_data in bucket:
                if existing_user == user_id:
                    user_interactions.append((item_id, interaction_data))
        
        return user_interactions
    
    def get_item_interactions(self, item_id):
        """
        Get all interactions for a specific item.
        
        Args:
            item_id (str/int): Item identifier
            
        Returns:
            list: List of (user_id, interaction_data) tuples
            
        Time Complexity: O(n) where n is total number of interactions
        """
        item_interactions = []
        
        for bucket in self.buckets:
            for user_id, existing_item, interaction_data in bucket:
                if existing_item == item_id:
                    item_interactions.append((user_id, interaction_data))
        
        return item_interactions
    
    def delete(self, user_id, item_id):
        """
        Delete a user-item interaction.
        
        Args:
            user_id (str/int): User identifier
            item_id (str/int): Item identifier
            
        Returns:
            bool: True if deleted, False if not found
            
        Time Complexity: O(1) average, O(n) worst case
        """
        hash_index = self._hash_function(user_id, item_id)
        bucket = self.buckets[hash_index]
        
        for i, (existing_user, existing_item, interaction_data) in enumerate(bucket):
            if existing_user == user_id and existing_item == item_id:
                del bucket[i]
                self.size -= 1
                return True
        
        return False
    
    def get_statistics(self):
        """
        Get hash table performance statistics.
        
        Returns:
            dict: Statistics including size, capacity, load factor, etc.
        """
        bucket_sizes = [len(bucket) for bucket in self.buckets]
        
        return {
            'size': self.size,
            'capacity': self.capacity,
            'load_factor': self.size / self.capacity,
            'max_bucket_size': max(bucket_sizes) if bucket_sizes else 0,
            'avg_bucket_size': sum(bucket_sizes) / len(bucket_sizes) if bucket_sizes else 0,
            'empty_buckets': bucket_sizes.count(0)
        }

# Example usage and testing
if __name__ == "__main__":
    # Create hash table instance
    interaction_table = UserItemHashTable(100)
    
    # Sample interaction data
    sample_interactions = [
        ("user_001", "item_101", {"rating": 4.5, "timestamp": "2023-01-15", "action": "purchase"}),
        ("user_001", "item_102", {"rating": 3.0, "timestamp": "2023-01-16", "action": "view"}),
        ("user_002", "item_101", {"rating": 5.0, "timestamp": "2023-01-17", "action": "purchase"}),
        ("user_002", "item_103", {"rating": 2.5, "timestamp": "2023-01-18", "action": "return"}),
    ]
    
    # Insert sample data
    for user_id, item_id, data in sample_interactions:
        interaction_table.insert(user_id, item_id, data)
    
    # Demonstrate retrieval operations
    print("Hash Table Implementation Demo")
    print("=" * 40)
    
    # Get specific interaction
    result = interaction_table.get("user_001", "item_101")
    print(f"user_001 interaction with item_101: {result}")
    
    # Get all interactions for a user
    user_interactions = interaction_table.get_user_interactions("user_001")
    print(f"All interactions for user_001: {user_interactions}")
    
    # Get statistics
    stats = interaction_table.get_statistics()
    print(f"Hash table statistics: {stats}")