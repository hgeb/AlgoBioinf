# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 16:31:01 2021

@author: hanne
"""

######################################
### BINARY TREE
######################################    
        
class BinaryTree:
    """
    Defines a binary tree containing internal and leaf nodes.
    """
    def __init__(self,root = None):
        self.root = root
        self.leaves = []
    
    def __repr__(self):
        return f'{self.root}'
    
    class Node:
        def __init__(self,parent = None):
            self.parent = parent
            self.tag = False
            self.score = {}
            
        def setTag(self, tag):
            self.tag = tag
    
    class LeafNode(Node):
        """
        Leaf node of binary tree.
        """
        def __init__(self,num,parent = None , sequence = ""):
            super().__init__(parent)
            self.num = num
            self.sequence = sequence
            
        def __repr__(self):
            return f'{self.num}'
        
        def setSequence(self, sequence):
            self.sequence = sequence
        
    
    class InternalNode(Node):
        """
        Internal node of binary tree.
        """
        def __init__(self, left, right, parent =None):
            super().__init__(parent)
            self.left = left
            self.right = right
            
        def __repr__(self):
            return f'({self.left},{self.right})'
    
    def setRoot(self, root):
        """
        Sets root of binary Tree.

        Parameters
        ----------
        root : Node
            Root node of binary tree.

        Returns
        -------
        None.

        """
        self.root = root
        
    def addLeaf(self, leaf):
        """
        Adds leaf to leaves to keep track of LeafNodes in binary tree.

        Parameters
        ----------
        leaf : BinaryTree.LeafNode
            Leaf of binary tree.

        Returns
        -------
        None.

        """
        
        self.leaves.append(leaf)
        
    def getLeaves(self):
        """
        Gets leves of binary tree

        Returns
        -------
        List
            Leafes of binary tree.

        """
        return self.leaves
    
    
    
        
    def hasRoot(self):
        if self.root:
            return True
        else:
            return False
    