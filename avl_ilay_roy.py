#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

from inspect import stack


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type key: int or None
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.right = None
		self.left = None
		self.parent = None
		self.height = -1
		self.size = 0
		# In case of instantiating virtual AVL node: key, value = None
		# if not virtual node, always asign node left & right son (which are virtual nodes)
		if key != None and value != None:
			self.left = AVLNode(None, None)
			self.right = AVLNode(None, None)
			self.left.parent = self
			self.right.parent = self
			self.height = 0
			self.size = 1
		# field of balance factor of node
		self.BF = 0
		
	def __eq__(self, other):
		if not isinstance(other, AVLNode):
			return False
		return self.key == other.key and self.value == other.value

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent


	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node
		#node.set_parent(self)


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node
		#node.set_parent(self)



	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node


	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key


	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value


	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None
	
	"""sets the size of node

	@type s: int
	@param s: the size
	"""

	def set_size(self, s):
		self.size = s

	# get size of node, based on number of nodes in subtree with self as root + 1
	def get_size(self):
		return self.size

	# returns the node balance factor
	def get_BF(self):
		return self.BF
	
	# helper function for getting updated height from children
	def get_height_from_children(self):
		return 1 + max(self.left.height, self.right.height)


	"""returns whether self is a leaf"""
	def is_leaf(self):
		right = self.get_right()
		left = self.get_left()
		return not (left.is_real_node() or right.is_real_node())

	"""returns whether self has single child"""
	def has_single_child(self):
		right = self.get_right()
		left = self.get_left()
		return (left.is_real_node() and not right.is_real_node()) or (right.is_real_node() and not left.is_real_node())

	"""update the size of node by adding 1 to his children size sum
	"""
	def update_size_from_children(self):
		self.set_size(1 + self.get_left().get_size() + self.get_right().get_size())

	def update_BF(self):
		self.BF = self.get_left().get_height() - self.get_right().get_height()

	"""update the height of node by adding 1 to his children max height
	"""
	def update_height_from_children(self):
		self.set_height(1 + max(self.get_right().get_height(), self.get_left().get_height()))

	def update(self):
		self.update_height_from_children()
		#self.update_size_from_children()
		self.update_BF()


"""
A class implementing the ADT Dictionary, using an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	# assigns as default value of root field a virtual AVL node when no root param is given in ctor
	def __init__(self, root=AVLNode(None, None)):
		self.root = root
        # add your fields here
		if root.get_left() == None and not root.is_real_node():
			# set left child of root as virtual node
			root.set_left(AVLNode(None, None))
		if root.get_right() == None and not root.is_real_node():
			# set right child of root as virtual node
			root.set_right(AVLNode(None, None))



	"""searches for a AVLNode in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	"""
	def search(self, key):
		curr = self.get_root()
		while curr.is_real_node() and curr.get_key() != key:
			if curr.get_key() > key:
				curr = curr.get_left()
			else:
				curr = curr.get_right()
		if curr.is_real_node():
			return curr
		else:
			return None

	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		# if the tree is empty just insert the node
		if self.root.get_key() == None:
			self.root = AVLNode(key, val)
			return 0
		
		# create new AVLnode
		new_node = AVLNode(key, val)
		# insert the node as binary search tree insertion
		node_inserted = self.BST_insert(new_node)

		# start rebalancing process with parent of inserted node
		p = node_inserted.get_parent()

		# fix the tree if needed in order to preserve AVL qualities
		balance_actions = self.insertion_rebalance_tree(p)
		return balance_actions
	


	# complexity: O(log n) complexity (where n is the size of the tree)
	def BST_insert(self, node):

		curr = self.get_root()

		# go down the tree until the desired
		# virtual node
		while curr.is_real_node():
			# go right if new key is greater than
			# current node key, Otherwise left
			# p.set_size(p.get_size() + 1)
			if curr.get_key() < node.get_key():
				curr = curr.get_right()
			else:
				curr = curr.get_left()

		# insert the new node between the virtual node
		# and his parent
		parent = curr.parent
		if parent.get_key() > node.get_key():
			parent.set_left(node)
		else:
			parent.set_right(node)

		node.set_parent(parent)

		parent = node.get_parent()
		# update the size of the ancestors, up from the inserted node (as a leaf) until the root
		self.increment_size_to_root(parent)

		return node

	""" balance the tree after insertion """
	def insertion_rebalance_tree(self, p):
		balance_actions = 0
		while p != None:
			prev_height = p.get_height()
			p.update()
			
			# Stage 3.2: If balance factor is within range and height hasn't changed, terminate
			if abs(p.get_BF()) < 2 and prev_height == p.get_height():
				break
			# Stage 3.3: If balance factor is within range but height changed, move to parent's parent
			elif abs(p.get_BF()) < 2 and prev_height != p.get_height():
				balance_actions += 1
				p = p.get_parent()
			else:
			# Stage 3.4: Perform rotation and terminate
				balance_actions += self.tree_rotation(p)
				break

		return balance_actions

	"""rotate the tree in order to re-balance the tree
	returns the number of rotations required"""

	def tree_rotation(self, node):
		if node.get_BF() == -2:
			if node.get_right().get_BF() == -1 or node.get_right().get_BF() == 0:
				self.left_rotation(node)
				return 1
			else:
				# This is the case of node's right son has balance factor = 1
				self.right_rotation(node.get_right())
				self.left_rotation(node)
				return 2
		elif node.get_BF() == 2:
			if node.get_left().get_BF() == 1 or node.get_left().get_BF() == 0:
				self.right_rotation(node)
				return 1
			else:
				# This is the case of node's left son has balance factor = -1
				self.left_rotation(node.get_left())
				self.right_rotation(node)
				return 2
		return 0

	"""perform left rotation"""

	def left_rotation(self, node):
		B_node = node
		A_node = node.get_right()

		# change pointers to complete the rotation
		B_node.set_right(A_node.get_left())
		B_node.get_right().set_parent(B_node)
		A_node.set_left(B_node)
		A_node.set_parent(B_node.get_parent())
		if A_node.get_parent() != None:
			if A_node.get_parent().get_left().get_key() == B_node.get_key():
				A_node.get_parent().set_left(A_node)
			else:
				A_node.get_parent().set_right(A_node)
		else:
			self.root = A_node
		B_node.set_parent(A_node)

		B_node.update()
		A_node.update()

	"""perform right rotation"""

	def right_rotation(self, node):
		B_node = node
		A_node = node.get_left()

		# change pointers to complete the rotation
		B_node.set_left(A_node.get_right())
		B_node.get_left().set_parent(B_node)
		A_node.set_right(B_node)
		A_node.set_parent(B_node.get_parent())

		if A_node.get_parent() != None:
			if A_node.get_parent().get_left().get_key() == B_node.get_key():
				A_node.get_parent().set_left(A_node)
			else:
				A_node.get_parent().set_right(A_node)
		else:
			self.root = A_node

		B_node.set_parent(A_node)

		B_node.update()
		A_node.update()


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		# get parent of physically deleted  node from the tree, and fix all the pointers
		p = self.BST_delete(node)

		# get parent of deleted node to start rebalancing process
		# p = deleted_node.get_parent()

		# fix the tree if needed in order to preserve AVL qualities
		# returns the number of rotations and/or height changes needed
		balance_actions = self.deletion_rebalance_tree(p)
		return balance_actions
	
	"""delete the node from the tree as binary serach tree
	deletation, by changing the necessary pointers"""
	### complexity: O(log n)
	def BST_delete(self, node):
		parent = node.get_parent()
		if parent is None:
			# the node is the tree root
			return self.BST_root_delete()
		if node.is_leaf():
			# the node is a leaf, so we just change the parent pointer
			if parent.get_left().get_key() == node.get_key():
				parent.set_left(AVLNode(None, None))
			else:
				parent.set_right(AVLNode(None, None))
			
		elif node.has_single_child():
			# the node has single child, so we will bypass him by correcting
			# the parent pointer and the child pointer
			if parent.get_left().get_key() == node.get_key():
				if node.get_right().is_real_node():
					parent.set_left(node.get_right())
					node.get_right().set_parent(parent)
				else:
					parent.set_left(node.get_left())
					node.get_left().set_parent(parent)
			else:
				if node.get_right().is_real_node():
					parent.set_right(node.get_right())
					node.get_right().set_parent(parent)
				else:
					parent.set_right(node.get_left())
					node.get_left().set_parent(parent)
			
		else:
			# the node has 2 children, so we find the node successor
			# then we remove the successor and replace with the node
			# by correcting all the pointers
			successor = self.successor(node)

			parent = successor.get_parent()

			if successor.is_leaf():
			# the node is a leaf, so we just change the parent pointer
				if parent.get_left().get_key() == successor.get_key():
					parent.set_left(AVLNode(None, None))
				else:
					parent.set_right(AVLNode(None, None))
			else: # one child ONLY
				if parent.get_left().get_key() == successor.get_key():
					if successor.get_right().is_real_node:
						parent.set_left(successor.get_right())
						successor.get_right().set_parent(parent)
					else:
						parent.set_left(successor.get_left())
						successor.get_left().set_parent(parent)
				else:
					if successor.get_right().is_real_node():
						parent.set_right(successor.get_right())
						successor.get_right().set_parent(parent)
					else:
						parent.set_right(successor.get_left())
						successor.get_left().set_parent(parent)

			# Switch between original node to delete with successor node	
			parentOriginal = node.get_parent()
			if parentOriginal.get_left().get_key() == node.get_key():
				parentOriginal.set_left(successor)
			else:
				parentOriginal.set_right(successor)

			successor.set_parent(parentOriginal)
			successor.set_left(node.get_left())
			successor.set_right(node.get_right())
			node.get_left().set_parent(successor)
			node.get_right().set_parent(successor)

			# Use case when parent of physically deleted node (successor) is the node to delete, than parent = parent of original node
			if parent.get_key() == node.get_key():
				parent = parentOriginal

			# update the fields of the replacement node
			# successor.update()

		# update the size of ancestors
		self.decrement_size_to_root(parent)

		return parent
			

			# self.BST_delete(replacement_node)
			# parent = node.get_parent()

			# if parent.get_left().get_key() == node.get_key():
			# 	parent.set_left(replacement_node)
			# else:
			# 	parent.set_right(replacement_node)

			# replacement_node.set_parent(parent)
			# replacement_node.set_left(node.get_left())
			# replacement_node.set_right(node.get_right())
			# node.get_left().set_parent(replacement_node)
			# node.get_right().set_parent(replacement_node)

			# update the fields of the replacement node
			# replacement_node.update_size_from_children()
			# replacement_node.update_height_from_children()
			# replacement_node.update_BF()
			# p = replacement_node.get_parent()
			# update the fields of ancestors
			# while (p != None):
			# 	p.update_size_from_children()
			# 	p.update_height_from_children()
			# 	p.update_BF()
			# 	p = p.get_parent()
		
		# # update the fields of the ancestors
		# while (parent != None):
		# 	parent.update_size_from_children()
		# 	parent.update_height_from_children()
		# 	parent.update_BF()
		# 	parent = parent.get_parent()

		# return node

	def BST_root_delete(self):
		root = self.get_root()
		if root.is_leaf():
			# the root is a leaf so we return empty tree
			self.set_root(AVLNode(None, None))
			return AVLNode(None, None)
		elif root.has_single_child():
			# the root has single child, so we remove the root
			# and now the child is the tree root
			if root.get_left().is_real_node():
				self.set_root(root.get_left())
				root.get_left().set_parent(root.get_parent())
				return root.get_left()
			else:
				self.set_root(root.get_right())
				root.get_right().set_parent(root.get_parent())
				return root.get_right()
		else:
			# the root has 2 children, so we find his successor
			# and replace it with the root
			successor = self.successor(root)
			self.BST_delete(successor)
			self.set_root(successor)
			successor.set_parent(root.get_parent())
			successor.set_left(root.get_left())
			successor.set_right(root.get_right())
			root.get_left().set_parent(successor)
			root.get_right().set_parent(successor)
			return successor

	""" rabalance the tree after deletion """
	def deletion_rebalance_tree(self, p):
		balance_actions = 0
		while p != None:
			prev_height = p.get_height()
			p.update()

			# Stage 3.2: If balance factor is within range and height hasn't changed, terminate
			if abs(p.get_BF()) < 2 and prev_height == p.get_height():
				break
			# Stage 3.3: If balance factor is within range but height changed, move to parent's parent
			elif abs(p.get_BF()) < 2 and prev_height != p.get_height():
				balance_actions += 1
				p = p.get_parent()
			else:
			# Stage 3.4: Perform rotation, move to parent's parent
				balance_actions += self.tree_rotation(p)
				p = p.get_parent().get_parent()
		return balance_actions

	"""returns the successor node in self of node """
	def successor(self, node):
		if node.get_right().is_real_node():
			curr = node.get_right()
			while (curr.get_left().is_real_node()):
				curr = curr.get_left()
			return curr
		else:
			parent = node.get_parent()
			curr = node
			if parent is None:
				return curr.get_left()
			while (parent.get_left().get_key() != curr.get_key()):
				curr = parent
				parent = parent.get_parent()
				if parent is None:
					return curr.get_left()
			return parent


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		list_in_order = []
		s = []
		curr = self.get_root()
		while len(s) > 0 or curr.is_real_node():
			while curr.is_real_node():
				s.append(curr)
				curr = curr.get_left()
			curr = s.pop()
			list_in_order.append((curr.get_key(), curr.get_value()))
			curr = curr.get_right()
		return list_in_order


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.root.get_size()	

	
	"""splits the dictionary at the i'th index

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		# store the minimum of the larger keys
		larger_min = self.successor(node)
		if larger_min == None:
			self.delete(node)
			return [self, AVLTree(AVLNode(None, None))]
		# Create the split trees
		node.get_left().set_parent(None)
		t1 = AVLTree(node.get_left())   # The smaller keys
		node.get_right().set_parent(None)
		t2 = AVLTree(node.get_right())  # The larger keys
		# Go up the tree until reaching the root
		while node is not None and node.get_parent() is not None:
			parent = node.get_parent()
			# If the key of the parent is smaller than the key of the current
			# node, then join t1 with the left subtree of the node's parent,
			# with the key and value of the parent in between
			if parent.get_key() < node.get_key():
				# Deal with the case that t1 is empty
				if t1.get_root().get_key() == None:
					if parent.get_left().is_real_node():
						parent.get_left().set_parent(None)
						t1 = AVLTree(parent.get_left())
						t1.insert(parent.get_key(), parent.get_value())
				# Otherwise just join the trees
				else:
					if parent.get_left().is_real_node():
						parent.get_left().set_parent(None)
						tree_to_join = AVLTree(parent.get_left())
						t1.join(tree_to_join, parent.get_key(), parent.get_value())
			# If the key of the parent is greater than the key of the current
			# node, then join t2 with the right subtree of the node's parent,
			# with the key and value of the parent in between
			else:
				# Deal with the case that t2 is empty
				if t2.get_root().get_key() == None:
					if parent.get_right().is_real_node():
						parent.get_right().set_parent(None)
						t2 = AVLTree(parent.get_right())
						t2.insert(parent.get_key(), parent.get_value())
				# Otherwise just join the trees
				else:
					if parent.get_right().is_real_node():
						parent.get_right().set_parent(None)
						tree_to_join = AVLTree(parent.get_right())
						t2.join(tree_to_join, parent.get_key(), parent.get_value())
			node = node.get_parent()

		return [t1, t2]


	
	"""joins self with key and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree2
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def join(self, tree2, key, val):
		# create the separating node
		separator = AVLNode(key, val)

		# verify the root fields have correct values
		# self.get_root().update_height_from_children()
		# self.get_root().update_size_from_children()
		# self.get_root().update_BF()
		# tree2.get_root().update_height_from_children()
		# tree2.get_root().update_size_from_children()
		# tree2.get_root().update_BF()
		
		# compute height difference to find which tree is taller
		height_difference = self.get_root().get_height() - tree2.get_root().get_height()

		# attach two AVL trees with a separating node as the root
		if abs(height_difference) <= 1:
			self.connect_roots(tree2, separator)

		# attach two AVL trees with a separating node in the middle
		else:
			self.attachTrees(tree2, separator, height_difference)

		# fix the tree if needed in order to preserve AVL qualities
		self.deletion_rebalance_tree(separator)
		return abs(height_difference)


	"""join self with seperator node and another AVL tree"""
	def attachTrees(self, tree, separator, height_difference):
		if height_difference > 0:
			# self is taller than tree
			taller = self
			shorter = tree
		else:
			# the tree is taller than self, we do the same operations as before
			taller = tree
			shorter = self

		# connect the separator node to the node we found,
		# by changing the correct pointers
		if taller.get_root().get_key() > separator.get_key():
			# find the node in left sub-tree of self which his height
			# is equal to tree height
			node_to_join = taller.node_at_height(shorter.get_root().get_height(), "left")
			# all the taller nodes are greater than the separator node
			taller.left_connection(shorter, separator, node_to_join)
		else:
			# find the node in right sub-tree of self which his height
			# is equal to tree height
			node_to_join = taller.node_at_height(shorter.get_root().get_height(), "right")
			# all the taller nodes are smaller than the separator node
			taller.right_connection(shorter, separator, node_to_join)

		shorter.get_root().set_parent(separator)
		shorter.set_root(taller.get_root())

	"""connect the separator to trees, so that his left child is 
		the node in the left sub-tree of the taller tree, and his right
		child is the root of the shorter tree"""
	def left_connection(self, shorter, separator, node_to_join):
		separator.set_right(node_to_join)
		separator.set_parent(node_to_join.get_parent())
		node_to_join.get_parent().set_left(separator)
		node_to_join.set_parent(separator)
		separator.set_left(shorter.get_root())

		#update separator fields
		separator.update_height_from_children()
		separator.update_size_from_children()
		separator.update_BF()
		

	"""connect the separator to trees, so that his right child is 
		the node in the left sub-tree of the taller tree, and his left
		child is the root of the shorter tree"""
	def right_connection(self, shorter, separator, node_to_join):
		separator.set_left(node_to_join)
		separator.set_parent(node_to_join.get_parent())
		node_to_join.get_parent().set_right(separator)
		node_to_join.set_parent(separator)
		separator.set_right(shorter.get_root())


		#update separator fields
		separator.update_height_from_children()
		separator.update_size_from_children()
		separator.update_BF()

	"""connect self and AVL tree with a separating node as their root"""
	def connect_roots(self, tree, separator):
		# the trees height is equal so we just need to connect
		# the separating node to their roots
		if separator.get_key() > self.get_root().get_key():
			separator.set_left(self.get_root())
			separator.set_right(tree.get_root())
		else:
			separator.set_left(tree.get_root())
			separator.set_right(self.get_root())
		# set parent of tree avl-tree root node as seperator node
		tree.get_root().set_parent(separator)
		tree.set_root(separator)
		# set parent of self avl-tree root node as seperator node
		self.get_root().set_parent(separator)
		self.set_root(separator)

	"""find the first node in self which his height is equal or less than h
		in the @side sub-tree"""
	def node_at_height(self, h, side):
		if side == "left":
			curr = self.get_root()
			while curr.get_key() is not None and curr.get_height() > h:
				curr = curr.get_left()
			return curr
		else:
			curr = self.get_root()
			while curr.get_key() is not None and curr.get_height() > h:
				curr = curr.get_right()
			return curr


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

	def get_root(self):
		return self.root

	def set_root(self, node):
		self.root = node

	
	def increment_size_to_root(self, node_to_start):
		while node_to_start != None:
			node_to_start.set_size(node_to_start.get_size() + 1)
			node_to_start = node_to_start.get_parent()

	def decrement_size_to_root(self, node_to_start):
		while node_to_start != None:
			node_to_start.set_size(node_to_start.get_size() - 1)
			node_to_start = node_to_start.get_parent()