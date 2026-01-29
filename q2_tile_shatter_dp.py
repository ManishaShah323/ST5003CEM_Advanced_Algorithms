# ============================================================
# QUESTION 2: Strategic Tile Shatter Game (Dynamic Programming)
#
# Objective:
# Given a sequence of tiles, each with a value, determine the
# maximum points obtainable by shattering tiles in an optimal order.
#
# Algorithm Used:
# Interval Dynamic Programming
#
# Time Complexity:
# O(n³), where n is the number of tiles
# ============================================================

def maxPoints(nums):
    """
    Computes the maximum points obtainable by optimally
    shattering the tiles using Interval Dynamic Programming.

    nums : list of integers representing tile values
    """

    # Step 1: Add virtual boundary tiles with value 1
    # This simplifies edge case handling
    nums = [1] + nums + [1]
    n = len(nums)

    # Step 2: Initialize DP table
    # dp[i][j] stores the maximum points obtainable
    # by shattering tiles between index i and j (exclusive)
    dp = [[0] * n for _ in range(n)]

    # Step 3: Interval DP computation
    # length represents the distance between left and right indices
    for length in range(2, n):
        for left in range(n - length):
            right = left + length

            # Try each tile k as the last tile to be shattered
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    nums[left] * nums[k] * nums[right]
                    + dp[left][k]
                    + dp[k][right]
                )

    # Final answer is stored for the full interval
    return dp[0][n - 1]


# -----------------------------
# TEST CASES
# -----------------------------
if __name__ == "__main__":

    # Example 1
    tiles1 = [3, 1, 5, 8]
    print("Example 1 Output:", maxPoints(tiles1))

    # Example 2
    tiles2 = [1, 5]
    print("Example 2 Output:", maxPoints(tiles2))
