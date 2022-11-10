import random

class BST:


    def __init__(self, item = None, balancing = False):

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

        return self.node is None


    def height(self):

        return self._height


    def _update_height(self):

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
                    self.left = BST(item)
                    self.left.parent = self
                    self.left._update_height()
                else:
                    self.left.add(item)

            elif item > self.node:
                if self.right is None:
                    self.right = BST(item)
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
                    direction = -1
                else:
                    index = inorder_list.index(node.node) + 1
                    direction = 1

                successor = node.find(inorder_list[index])
                node.remove(successor.node)
                node.node = successor.node
                node._update_height()

                del successor

        if self._self_balancing:
            self.balance()

        if len(args) > 0:
            for arg in args:
                self.remove(arg)

        return self


    def find(self, item):

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


    def set_balancing(self, balancing):

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

        left_bal = 0
        if self.left is not None:
            left_bal = self.left._height + 1

        right_bal = 0
        if self.right is not None:
            right_bal = self.right._height + 1

        return left_bal - right_bal


    def _is_balanced(self):

        node_factor = self._find_bal_factor()
        if (node_factor > 1) or (node_factor < -1):
            return False

        left_balanced = True
        if self.left is not None:
            left_balanced = self.left._is_balanced()

        right_balanced = True
        if self.right is not None:
            right_balanced = self.right._is_balanced()

        if left_balanced and right_balanced:
            return True
        return False


    def balance(self):

        # balance left side
        if self.left is not None:
            left_bal = self.left._is_balanced()
            if left_bal is False:
                self.left.balance()

        # balance right side
        if self.right is not None:
            right_bal = self.right._is_balanced()
            if right_bal is False:
                self.right.balance()

        if self._is_balanced() is False:
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
        if self._is_balanced() is False:
            self.balance()


    def _rotate_left(self):

        # references
        node = BST(self.node)
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

        # references
        node = BST(self.node)
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

        if dot:
            node_str = "(.)"
        else:
            node_str = f"({self.node})"

        if (self.left == None) and (self.right == None):
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

                
                if line == len(left_list):
                    line -= 1

                if (len(left_list[line]) > 0) and (len(right_list[line]) > 0):
                    if (not left_list[line][-1].isspace()) and (not right_list[line][0].isspace()):
                        index = 0
                        while index < len(left_list):
                            left_list[index] += "  "
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
            last_index = paren + len(node_str)
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


    def print_tree(self, keep_whitespace = False, dot = False, in_file = False, file_name = "bst.txt"):

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
                with open(file_name, "w") as f:
                    f.write("()\n")
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
                with open(file_name, "w") as f:
                    for string in str_list:
                        if keep_whitespace:
                            f.write(string)
                            f.write("\n")
                        else:
                            f.write(string.rstrip())
                            f.write("\n")

            else:
                for string in str_list:
                    if keep_whitespace:
                        print(string)
                    else:
                        print(string.rstrip())


'''
for _ in range(5):
    t = BST(0)
    for _ in range(10):
        t.add(random.randint(-100,100))
    t.print_tree(False)
    print()
    t.set_balancing(True)
    t.print_tree(False)
    print("==========================================")
'''

'''
t = BST(50, True)
t.add(75).add(30, 60)
bt = BST(10)
bt.add(80, 90, 45)
bt.print_tree()
t.add(bt)

t.print_tree()
print("height:", t.height())
print("size:", t.size())
print("inorder:", t.inorder())
print("=========================================")

#t.remove(30, 50)
bs = t.find(30)
t.remove(bs, 80)
t.remove(80)

t.print_tree()
#print(t.left.height())
#print(t.right.height())
print("height:", t.height())
print("size:", t.size())
print("inorder:", t.inorder())
'''

'''
t = BST(0)
for _ in range(15):
    t.add((random.randint(-100,100)))
t.print_tree()
print("==========================================")

value = input("input number to remove: ")
while value != "q":
    t.remove(int(value))
    t.print_tree()
    print("height:", t.height())
    print("size:", t.size())
    print("inorder:", t.inorder())
    print("==========================================")
    value = input("input number to remove: ")
'''

'''
t = BST(40)
t.add(50).add(60).add(45).add(55).add(65).add(43).add(30).add(20).add(35)

t.print_tree()
print("height:", t.height())
print("size:", t.size())
print("inorder:", t.inorder())
print("=========================================")

t._rotate_right()

t.print_tree()
#print(t.left.height())
#print(t.right.height())
print("height:", t.height())
print("size:", t.size())
print("inorder:", t.inorder())
'''
