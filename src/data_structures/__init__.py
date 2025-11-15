"""
Data Structures Package for E-Commerce Recommendation System

This package contains optimized data structure implementations for
building efficient recommendation systems.

Modules:
- hash_table: User-item interaction storage with O(1) access
- similarity_graph: Product relationship graph for content-based filtering
- behavior_tree: Temporal behavior tracking with BST implementation
- category_tree: Hierarchical product categorization system
"""

__version__ = "1.0.0"
__author__ = "Data Structures Project Team"

# Import main classes for easy access
from .hash_table import UserItemHashTable
from .similarity_graph import ProductSimilarityGraph
from .behavior_tree import UserBehaviorTree
from .category_tree import CategoryHierarchyTree

__all__ = [
    'UserItemHashTable',
    'ProductSimilarityGraph', 
    'UserBehaviorTree',
    'CategoryHierarchyTree'
]