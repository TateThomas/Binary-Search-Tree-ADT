'''Binary Search Tree Module
CS 2420
Author: Tate Thomas

BST Class:

    Description:

    Binary Search Tree with option of self balancing. Each child is a subtree,
    meaning each child is its own BST and can be treated as a separate tree to
    an extent (explained later). Doing this allows for recursion in most of its
    methods. Note that a subtree contains a reference to its parent and is linked,
    so it is not completely separate. Any BST can be printed to the terminal, although,
    to keep most trees within a reasonable width, minimal whitespace is used between
    nodes. The drawback of this is that some nodes on different branches may not line
    up to each other when printed. There currently isn't an option to change the
    behavior of the print function. If the tree is self balancing, this is less
    likely to happen.

    __init__(item = None, balancing = False): New BST objects can be instantiated
        with either 1 item (BST(item)) or no items (BST()). It is also possible to set
        the new tree to be self balancing, denoted by setting the second arg as True.
        If a new BST is needed to be empty and self balancing, setting the first arg
        to None will work (BST(None, True)). It is possible to change the self
        balancing feature in the future (explained later).

    Attributes:

    node = value of the root
    parent = reference to the parent of the node if there is one
    left = reference to the left subtree if there is one
    right = reference to the right subtree if there is one

    Methods:

    size(): Returns the amount of nodes present in a tree as an int.
    is_empty(): Returns True if the root is None, False otherwise.
    height(): Returns the current height of the tree.
    add(item, *args): Adds an item to the tree in the appropriate spot; rebalances
        if the tree is set to self balance. You can provide any amount of items,
        separated by a comma. Adding a BST to a tree will take each value of that
        BST and add it to the current tree. If an item is already in the tree, it
        is ignored. Returns self, allowing other methods to be called on top of
        the add method. It is recommended to only call this method at the root of
        the tree, although, the option isn't closed off (for recursion purposes).
        Beware that if add is called on a child, bigger tree may not be sorted.
    remove(item, *args): Removes an item from the tree; rebalances if the tree
        is set to self balance. You can provide any amount of items, separated
        by a comma. If an item given is of the BST class, the entire subtree will
        be removed, only if found. If an item given is not found within the tree,
        it is ignored. Returns self, allowing other methods to be called
        on top of the remove method.
    find(item): Searches the tree for the given item. Returns the node if found.
        If it is not found, a ValueError is raised.
    inorder(): Returns a list with each item in increasing order.
    preorder(): Returns a list with each item in order from the top down, meaning
        the list starts with the root first, then the left branch and its children,
        and ends with the right branch and its children.
    postorder(): Returns a list with each item in order from the ground up, meaning
        the list progressively builds subtrees from left to right to eventually
        form the full tree.
    set_balancing(balancing = True): Sets the tree to be self balancing if the given
        arg is True (defaults to True if no args are given). It then balances the tree
        automatically. If the given arg is False, balancing is turned off, and the
        tree remains untouched. Subtrees/children cannot change the self balancing
        feature.
    is_balanced(): Returns True if the whole tree is balanced, False otherwise.
    balance(): Balances the tree, only allowing for the left and right branches to
        differ by 0 or 1.
    print_tree(keep_whitespace = False,
               dot = False,
               in_file = False,
               file_name = "bst.txt"): Prints a representation of the tree. Method
        was made with the intent of keeping the width to a minimum. Each node may
        not line up to other nodes on the same level.
        The arg "keep_whitespace" gives the choice to keep the whitespace at the
            end of each line, defaulted to False. Useful for if you want the
            representation to have the same width on each line.
        The arg "dot" gives the choice to represent all of the items in the tree
            as a single dot "(.)", defaulted to False. Useful for if you just want
            to see the structure of the tree.
        The arg "in_file" gives the choice to write the tree representation into
            a file, defaulted to False. Useful for visualizing large trees and
            allows the representation to be used elsewhere.
        The arg "file_name" gives the choice to provide a name for the file where
            the tree representation will go, defaulted to "bst.txt". The name must
            be of type str. Useful for if you are printing multiple representations
            into different files.
        If the print_tree method is called on a subtree, this will be displayed at
        the start by connecting a branch from the subrees root to the parent node,
        with the branch pointed in the direction the subtree is relative to the
        parent node. The parent node will be denoted as (...). This method works
        for trees of any size.
    copy(): Returns a shallow copy of the tree/subtree.
    deepcopy(): Returns a deep copy of the tree/subtree. If the method is used on
        a subtree, the deep copy will be its own tree without a parent.
'''


class BST:
    '''Binary Search Tree Class:

    Attributes:
        self.node
        self.parent
        self.left
        self.right

    Methods:
        size()
        is_empty()
        height()
        add(item, *args)
        remove(item, *args)
        find(item)
        inorder()
        preorder()
        postorder()
        set_balancing(balancing = True)
        is_balanced()
        balance()
        print_tree(keep_whitespace = False,
                   dot = False,
                   in_file = False,
                   file_name = "bst.txt")
        copy()
        deepcopy()
    '''


    def __init__(self, item = None, balancing = False):
        '''BST object can be instantiated with 1 item or no items. Balancing
        can be turned on in the second arg. Children are treated as separate
        subtrees
        '''

        self.node = item

        self.parent = None
        self.left = None
        self.right = None

        if isinstance(balancing, bool):
            self._self_balancing = balancing
        else:
            raise TypeError("balancing can only be type bool")

        self._height = 0


    def size(self):
        '''Returns the amount of nodes in the tree'''

        if self.node is None:
            return 0

        if self.left is None:
            left = 0
        else:
            left = self.left.size()

        if self.right is None:
            right = 0
        else:
            right = self.right.size()

        return 1 + left + right


    def is_empty(self):
        '''Returns True if the root node is None, False otherwise'''

        return self.node is None


    def height(self):
        '''Returns the height of the tree'''

        return self._height


    def _update_height(self):
        '''Updates the height of the nodes tree, along with its parent,
        if there is one
        '''

        # update self
        if (self.left is not None) and (self.right is None):
            self._height = self.left._height + 1

        elif (self.right is not None) and (self.left is None):
            self._height = self.right._height + 1

        elif self.left is None:
            self._height = 0

        else:
            if self.left._height >= self.right._height:
                self._height = self.left._height + 1

            else:
                self._height = self.right._height + 1

        # update parent
        if self.parent is not None:

            if self.parent._height == 0:
                self.parent._height = 1

            elif self.parent._height <= self._height:
                self.parent._height = self._height + 1

            self.parent._update_height()


    def add(self, item, *args):
        '''Adds an item to the tree. Any amount of items can be given at once,
        separated by a comma. If a BST is passed as an arg, each item in that
        BST will be copied over to the current tree. If self balancing is enabled,
        the tree will then rebalance. Returns self
        '''

        if isinstance(item, BST):
            preord = item.preorder()
            for value in preord:
                self.add(value)

        else:

            if self.is_empty():
                self.node = item
                return self

            if item < self.node:
                if self.left is None:
                    self.left = BST(item, self._self_balancing)
                    self.left.parent = self
                    self.left._update_height()
                else:
                    self.left.add(item)

            elif item > self.node:
                if self.right is None:
                    self.right = BST(item, self._self_balancing)
                    self.right.parent = self
                    self.right._update_height()
                else:
                    self.right.add(item)

        if self._self_balancing:
            self.balance()

        if len(args) > 0:
            for arg in args:
                self.add(arg)

        return self


    def remove(self, item, *args):
        '''Removes an item from the tree. Any amount of items can be removed at
        once, separated by a comma. If a BST is given as an arg, the root and
        its children/subtrees will also be removed. If the item is not found
        in the tree, it is ignored. If self balancing is enabled, the tree will
        then rebalance. Returns self
        '''

        if isinstance(item, BST):

            if item.parent.left is item:
                item.parent.left = None
            else:
                item.parent.right = None

            item.parent._update_height()
            if self._self_balancing:
                self.balance()

            del item

        else:

            try:
                node = self.find(item)
                par = node.parent
                side = 0

                if (par is not None) and (par.left is node):
                    side = -1
                elif (par is not None) and (par.right is node):
                    side = 1

                if (node.left is None) and (node.right is None):

                    if side < 0:
                        par.left = None
                    elif side > 0:
                        par.right = None

                    if side != 0:
                        par._update_height()
                        del node
                    else:
                        node.node = None

                elif (node.left is not None) and (node.right is None):

                    if side < 0:
                        par.left = node.left
                        node.left.parent = par
                    elif side > 0:
                        par.right = node.left
                        node.left.parent = par

                    if side != 0:
                        par._update_height()
                        del node
                    else:
                        replacement = node.left
                        node._height = replacement._height
                        node.left = replacement.left
                        node.right = replacement.right
                        node.node = replacement.node
                        del replacement

                elif (node.right is not None) and (node.left is None):

                    if side < 0:
                        par.left = node.right
                        node.right.parent = par
                    elif side > 0:
                        par.right = node.right
                        node.right.parent = par

                    if side != 0:
                        par._update_height()
                        del node
                    else:
                        replacement = node.right
                        node._height = replacement._height
                        node.left = replacement.left
                        node.right = replacement.right
                        node.node = replacement.node
                        del replacement

                else:
                    inorder_list = node.inorder()

                    # find index of successor
                    if node.left._height >= node.right._height:
                        index = inorder_list.index(node.node) - 1
                    else:
                        index = inorder_list.index(node.node) + 1

                    successor = node.find(inorder_list[index])
                    node.remove(successor.node)
                    node.node = successor.node
                    node._update_height()

                    del successor

            except:
                pass

        if self._self_balancing:
            self.balance()

        if len(args) > 0:
            for arg in args:
                self.remove(arg)

        return self


    def find(self, item):
        '''Searches for an item in the tree, returning the BST object that item
        occupies. If it is not found, a ValueError is raised
        '''

        if self.node is None:
            raise ValueError("Tree is empty")

        if item == self.node:
            return self

        if (item < self.node) and (self.left is not None):
            return self.left.find(item)

        if (item > self.node) and (self.right is not None):
            return self.right.find(item)

        raise ValueError("Item not found in tree")


    def inorder(self):
        '''Returns a list of the tree in order of inorder traversal'''

        inorder_list = []

        left_list = []
        if self.left is not None:
            left_list = self.left.inorder()

        right_list = []
        if self.right is not None:
            right_list = self.right.inorder()

        inorder_list.extend(left_list)
        inorder_list.append(self.node)
        inorder_list.extend(right_list)

        return inorder_list


    def preorder(self):
        '''Returns a list of the tree in order of preorder traversal'''

        preorder_list = [self.node]

        left_list = []
        if self.left is not None:
            left_list = self.left.preorder()

        right_list = []
        if self.right is not None:
            right_list = self.right.preorder()

        preorder_list.extend(left_list)
        preorder_list.extend(right_list)

        return preorder_list


    def postorder(self):
        '''Returns a list of the tree in order of postorder traversal'''

        postorder_list = []

        left_list = []
        if self.left is not None:
            left_list = self.left.postorder()

        right_list = []
        if self.right is not None:
            right_list = self.right.postorder()

        postorder_list.extend(left_list)
        postorder_list.extend(right_list)
        postorder_list.append(self.node)

        return postorder_list


    def set_balancing(self, balancing = True):
        '''Sets the self balancing feature to True or False. Only roots of trees
        can change the trees self balancing feature
        '''

        if isinstance(balancing, bool):
            if self.parent is None:
                self._self_balancing = balancing
                if balancing:
                    self.balance()
            else:
                raise AttributeError("Tree is a subtree of another tree; cannot change balancing")
        else:
            raise TypeError("set_balancing only takes type bool")


    def _find_bal_factor(self):
        '''Returns the height of the left side minus the height
        of the right side
        '''

        left_bal = 0
        if self.left is not None:
            left_bal = self.left._height + 1

        right_bal = 0
        if self.right is not None:
            right_bal = self.right._height + 1

        return left_bal - right_bal


    def is_balanced(self):
        '''Returns true if the height of the left side and right side only differ
        by 0 or 1, along with each subtree contained. Returns false otherwise
        '''

        node_factor = self._find_bal_factor()
        if (node_factor > 1) or (node_factor < -1):
            return False

        left_balanced = True
        if self.left is not None:
            left_balanced = self.left.is_balanced()

        right_balanced = True
        if self.right is not None:
            right_balanced = self.right.is_balanced()

        if left_balanced and right_balanced:
            return True
        return False


    def balance(self):
        '''Balances a tree using left and right rotations'''

        # balance left side
        if self.left is not None:
            left_bal = self.left.is_balanced()
            if left_bal is False:
                self.left.balance()

        # balance right side
        if self.right is not None:
            right_bal = self.right.is_balanced()
            if right_bal is False:
                self.right.balance()

        if self.is_balanced() is False:
            node_fact = self._find_bal_factor()

            if node_fact > 0:
                child_fact = self.left._find_bal_factor()
            elif node_fact < 0:
                child_fact = self.right._find_bal_factor()

            if (node_fact > 0) and (child_fact > 0):
                self._rotate_right()

            elif (node_fact > 0) and (child_fact <= 0):
                self.left._rotate_left()
                self._rotate_right()

            elif (node_fact < 0) and (child_fact > 0):
                self.right._rotate_right()
                self._rotate_left()

            elif (node_fact < 0) and (child_fact <= 0):
                self._rotate_left()

        # verify
        if self.is_balanced() is False:
            self.balance()


    def _rotate_left(self):
        '''Rotates a tree left at the top node'''

        # references
        node = BST(self.node, self._self_balancing)
        right = self.right
        child = right.left

        # set up new nodes right child
        node.right = child
        if child is not None:
            child.parent = node

        # set up new nodes left child
        node.left = self.left
        if self.left is not None:
            self.left.parent = node

        # connect new node to tree
        node.parent = self
        self.left = node

        # replace trees node
        self.node = right.node

        # reset trees right child
        self.right = right.right
        right.parent = self

        del right

        node._update_height()


    def _rotate_right(self):
        '''Rotates a tree right at the top node'''

        # references
        node = BST(self.node, self._self_balancing)
        left = self.left
        child = left.right

        # set up new nodes left child
        node.left = child
        if child is not None:
            child.parent = node

        # set up new nodes right child
        node.right = self.right
        if self.right is not None:
            self.right.parent = node

        # connect new node to tree
        node.parent = self
        self.right = node

        # replace trees node
        self.node = left.node

        # reset trees left child
        self.left = left.left
        left.parent = self

        del left

        node._update_height()


    def _tree_to_str_list(self, dot = False):
        '''Converts a tree to an ASCII visual representation. Returns each line
        of that representation in a list
        '''

        if dot:
            node_str = "(.)"
        else:
            if str(self.node)[0] == "(":
                node_str = f"{self.node}"
            else:
                node_str = f"({self.node}"
            if str(self.node)[-1] != ")":
                node_str += ")"

            i = 1
            while i < (len(node_str) - 1):
                if node_str[i] == "(":
                    node_str = node_str[:i] + "{" + node_str[i + 1:]
                elif node_str[i] == ")":
                    node_str = node_str[:i] + "}" + node_str[i + 1:]
                i += 1

        if (self.left is None) and (self.right is None):
            return [node_str]

        str_list = []

        # get left and right lists recursively
        left_list = []
        if self.left is not None:
            left_list = self.left._tree_to_str_list(dot)
        right_list = []
        if self.right is not None:
            right_list = self.right._tree_to_str_list(dot)

        # even out the lists by adding whitespace
        if len(left_list) > 0:
            while len(left_list) < len(right_list):
                left_list.append(len(left_list[0]) * " ")
        if len(right_list) > 0:
            while len(left_list) > len(right_list):
                right_list.append(len(right_list[0]) * " ")

        # delete unneccesary whitespace by merging
        if (len(left_list) > 0) and (len(right_list) > 0):

            # find index of inner parenthesis on both sides
            left_paren = -1
            while left_paren >= (len(left_list[0]) * -1):
                if left_list[0][left_paren].isspace():
                    left_paren -= 1
                else:
                    break
            right_paren = 0
            while right_paren < len(right_list[0]):
                if right_list[0][right_paren].isspace():
                    right_paren += 1
                else:
                    break

            # find max amount of whitespace that can be removed
            max_whitespace = right_paren + ((left_paren * -1) - 1) - (len(node_str) - 2)
            # *max_whitespace_to_be_deleted

            if max_whitespace > 0:

                # make distance even
                if (max_whitespace % 2) == 1:
                    index = 0
                    while index < len(left_list):
                        left_list[index] += " "
                        index += 1
                    max_whitespace += 1

                merge_left = True
                merge_right = True

                # check if its possible to merge on both left and right sides
                while (merge_left or merge_right) and (max_whitespace > 0):
                    line = 0
                    merge = []  # list of tuples of bools telling if you can merge on left or right

                    while line < len(left_list):
                        combined = left_list[line] + right_list[line]

                        # potetial line deleting 2 characters from end of left
                        potent_line_1 = left_list[line][:-2] + right_list[line]
                        if (len(potent_line_1.replace(" ", "")) != len(combined.replace(" ", ""))) or (len(left_list[line][:-2]) == 0):
                            merge_left = False
                        else:
                            merge_left = True

                        # potetial line deleting 2 characters from start of right
                        potent_line_2 = left_list[line] + right_list[line][2:]
                        if len(potent_line_2.replace(" ", "")) != len(combined.replace(" ", "")) or (len(right_list[line][2:]) == 0):
                            merge_right = False
                        else:
                            merge_right = True

                        if (merge_left is False) and (merge_right is False):
                            merge = []
                            break

                        merge.append((merge_left, merge_right))
                        line += 1

                    # remove whitespace
                    if len(merge) > 0:
                        index = 0
                        while index < len(merge):
                            if merge[index][0]:
                                left_list[index] = left_list[index][:-2]
                            elif merge[index][1]:
                                right_list[index] = right_list[index][2:]
                            index += 1
                        max_whitespace -= 2

                if (len(left_list) > 0) and (len(left_list[0]) > 0):

                    if (len(right_list) > 0) and (len(right_list[0]) > 0):

                        index = 0
                        while index < len(left_list):
                            if ((left_list[index][-1] ==  ")") or (left_list[index][-1] ==  "\\")) and ((right_list[index][0] == "(") or (right_list[index][0] == "/")):
                                j = 0
                                while j < len(left_list):
                                    left_list[j] += "  "
                                    j += 1
                            index += 1  

            elif max_whitespace < 0:
                max_whitespace *= -1
                index = 0
                while index < len(left_list):
                    left_list[index] += f"{max_whitespace * ' '}"
                    index += 1

        elif len(left_list) > 0:

            # check if more whitespace is needed for node
            paren = -1
            while paren >= (len(left_list[0]) * -1):
                if left_list[0][paren].isspace():
                    paren -= 1
                else:
                    break

            # add whitespace if needed
            diff = paren + len(node_str)
            if diff > 0:
                index = 0
                while index < len(left_list):
                    left_list[index] += f"{diff * ' '}"
                    index += 1

        else:

            # check if more whitespace is needed for node
            paren = 0
            while paren < len(right_list[0]):
                if right_list[0][paren].isspace():
                    paren += 1
                else:
                    break

            # add whitespace if needed
            diff = paren - len(node_str) + 1
            if diff < 0:
                index = 0
                while index < len(right_list):
                    right_list[index] = f"{(diff * -1) * ' '}" + right_list[index]
                    index += 1

        # merge left and right lists and append
        index = 0
        if (len(left_list) > 0) and (len(right_list) > 0):
            while index < len(left_list):
                str_list.append(left_list[index] + right_list[index])
                index += 1

            whitespace = f"{len(str_list[0]) * ' '}"

            # find parens
            i = 0
            while True:
                if str_list[0][i] == ")":
                    j = i + 2
                    while str_list[0][j] != "(":
                        j += 1
                    break
                i += 1

            # make branches
            while (j - i - 1) >= (len(node_str) - 2):
                branches = whitespace[:i] + "/" + whitespace[i + 1:j] + "\\" + whitespace[j + 1:]
                str_list.insert(0, branches)
                i += 1
                j -= 1
            i -= 1
            j += 1

            # add top node
            root = whitespace[:i] + node_str + whitespace[j + 1:]
            str_list.insert(0, root)

        elif len(left_list) > 0:
            while index < len(left_list):
                str_list.append(left_list[index])
                index += 1

            paren = -1
            while paren >= (len(str_list[0]) * -1):
                if str_list[0][paren].isspace():
                    paren -= 1
                else:
                    break

            whitespace = f"{len(str_list[0]) * ' '}"

            # make branch
            branch = whitespace[:paren] + "/" + whitespace[paren + len(whitespace) + 1:]
            str_list.insert(0, branch)

            # add top node
            root = whitespace[:paren] + node_str + whitespace[paren + len(whitespace) + len(node_str):]
            str_list.insert(0, root)

        else:
            while index < len(right_list):
                str_list.append(right_list[index])
                index += 1

            paren = 0
            while paren < len(str_list[0]):
                if str_list[0][paren].isspace():
                    paren += 1
                else:
                    break

            whitespace = f"{len(str_list[0]) * ' '}"

            # make branch
            branch = whitespace[:paren] + "\\" + whitespace[paren + 1:]
            str_list.insert(0, branch)

            # add top node
            root = whitespace[:paren - len(node_str) + 1] + node_str + whitespace[paren + 1:]
            str_list.insert(0, root)

        return str_list


    def print_tree(self, keep_whitespace = False,
                         dot = False,
                         in_file = False,
                         file_name = "bst.txt"):
        '''Prints a representation of the tree to the terminal. Option to
        keep whitespace at the end of each line. Option to represent values
        in tree as dots. Option to export the representation to a file. Option
        to give that file a specific name
        '''

        if not isinstance(keep_whitespace, bool):
            raise TypeError("keep_whitespace must be type bool")
        if not isinstance(dot, bool):
            raise TypeError("dot must be type bool")
        if not isinstance(in_file, bool):
            raise TypeError("in_file must be type bool")
        if not isinstance(file_name, str):
            raise TypeError("file_name must be type str")

        if self.is_empty():
            if in_file:
                with open(file_name, "w") as file:
                    file.write("()\n")
            else:
                print("()")

        else:
            str_list = self._tree_to_str_list(dot)

            if self.parent is not None:
                paren = 0
                whitespace = f"{len(str_list[0]) * ' '}"

                if self is self.parent.left:

                    # find right most parenthesis
                    while paren < len(str_list[0]):
                        if str_list[0][paren] == ")":
                            break
                        paren += 1

                    # add more whitespace if needed
                    if paren >= (len(str_list[0]) - 4):
                        index = 0
                        while index < len(str_list):
                            str_list[index] += f"{(5 - (len(whitespace) - paren)) * ' '}"
                            index += 1
                        whitespace = f"{len(str_list[0]) * ' '}"

                    branch = whitespace[:paren] + "/" + whitespace[paren + 1:]
                    node = whitespace[:paren] + "(...)" + whitespace[paren + 5:]

                else:

                    # find the left most parenthesis
                    while paren < len(str_list[0]):
                        if str_list[0][paren] == "(":
                            break
                        paren += 1

                    # add more whitespace if needed
                    if paren <= 3:
                        index = 0
                        while index < len(str_list):
                            str_list[index] = f"{(4 - paren) * ' '}" + str_list[index]
                            index += 1
                        paren += (4 - paren)
                        whitespace = f"{len(whitespace) * ' '}"

                    branch = whitespace[:paren] + "\\" + whitespace[paren + 1:]
                    node = whitespace[:paren - 4] + "(...)" + whitespace[paren + 1:]

                str_list.insert(0, branch)
                str_list.insert(0, node)

            if in_file:
                with open(file_name, "w") as file:
                    for string in str_list:
                        if keep_whitespace:
                            file.write(string)
                            file.write("\n")
                        else:
                            file.write(string.rstrip())
                            file.write("\n")

            else:
                for string in str_list:
                    if keep_whitespace:
                        print(string)
                    else:
                        print(string.rstrip())


    def copy(self):
        '''Returns a shallow copy of the BST'''

        new_tree = BST(self.node, self._self_balancing)

        new_tree.left = self.left
        new_tree.right = self.right
        new_tree.parent = self.parent

        new_tree._height = self._height

        return new_tree


    def deepcopy(self):
        '''Returns a deep copy of the BST, excluding the parent node
        if it exists
        '''

        new_tree = BST(self.node, self._self_balancing)
        new_tree._height = self._height

        if self.left is not None:
            new_tree.left = self.left.deepcopy()
            new_tree.left.parent = new_tree
        if self.right is not None:
            new_tree.right = self.right.deepcopy()
            new_tree.right.parent = new_tree

        return new_tree
