# ============================================================
# QUESTION 3: Service Center Placement in a Binary Tree
#
# Objective:
# Place the MINIMUM number of service centers so that
# every city (node) in the binary tree is covered.
#
# Coverage Rule:
# A service center placed at a node covers:
# - The node itself
# - Its parent
# - Its immediate children
#
# Algorithm:
# Greedy strategy using POST-ORDER DFS
#
# Time Complexity:
# O(n), where n is the number of nodes
# ============================================================


from collections import deque


class TreeNode:
    """Represents a node (city) in the binary tree."""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def build_tree(level_order):
    """
    Builds a binary tree from a level-order list.
    None represents missing nodes.

    Example:
    [0, 0, None, 0, None, 0, None, None, 0]
    """

    if not level_order or level_order[0] is None:
        return None

    root = TreeNode(level_order[0])
    queue = deque([root])
    i = 1

    while queue and i < len(level_order):
        current = queue.popleft()

        # Left child
        if i < len(level_order) and level_order[i] is not None:
            current.left = TreeNode(level_order[i])
            queue.append(current.left)
        i += 1

        # Right child
        if i < len(level_order) and level_order[i] is not None:
            current.right = TreeNode(level_order[i])
            queue.append(current.right)
        i += 1

    return root


class Solution:
    """Computes minimum number of service centers."""
    def __init__(self):
        self.centers = 0

    def minServiceCenters(self, root):

        # DFS states:
        # 0 → needs coverage
        # 1 → covered
        # 2 → has service center

        def dfs(node):
            if not node:
                return 1  # null nodes are treated as covered

            left = dfs(node.left)
            right = dfs(node.right)

            # If any child needs coverage, place service center here
            if left == 0 or right == 0:
                self.centers += 1
                return 2

            # If any child has a service center, this node is covered
            if left == 2 or right == 2:
                return 1

            # Otherwise, this node needs coverage
            return 0

        root_state = dfs(root)

        # Final check for root
        if root_state == 0:
            self.centers += 1

        return self.centers


# -----------------------------
# TEST CASE (FROM QUESTION)
# -----------------------------
if __name__ == "__main__":

    # Input (level-order):
    # {0, 0, null, 0, null, 0, null, null, 0}
    tree_input = [0, 0, None, 0, None, 0, None, None, 0]

    root = build_tree(tree_input)

    solution = Solution()
    print(
        "Minimum service centers required:",
        solution.minServiceCenters(root)
    )
