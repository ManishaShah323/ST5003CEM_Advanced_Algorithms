"""
QUESTION 1(a): Optimizing Sensor Placement for Data Collection

Problem:
Given multiple sensor locations on a 2D plane, determine the optimal position
of a data aggregation hub such that the total sum of Euclidean distances
from the hub to all sensors is minimized.

Why Geometric Median?
- The objective minimizes SUM of Euclidean distances.
- Arithmetic mean minimizes SUM of SQUARED distances, not Euclidean distances.
- Hence, the correct solution is the GEOMETRIC MEDIAN.

Algorithm Used:
Weiszfeld’s Algorithm (Iterative Optimization)

Time Complexity:
O(n × k)
n = number of sensors
k = number of iterations until convergence
"""

import math


def geometric_median(points, eps=1e-6):
    """
    Computes the geometric median using Weiszfeld's Algorithm.

    Parameters:
    points : list of (x, y) sensor coordinates
    eps    : convergence threshold

    Returns:
    (x, y) : coordinates of optimal hub location
    """

    # Initial guess: arithmetic mean (only for starting point)
    x = sum(p[0] for p in points) / len(points)
    y = sum(p[1] for p in points) / len(points)

    while True:
        num_x = 0
        num_y = 0
        den = 0
        coincident = False

        for px, py in points:
            d = math.hypot(x - px, y - py)

            # If hub coincides with a sensor, it is optimal
            if d < eps:
                x, y = px, py
                coincident = True
                break

            num_x += px / d
            num_y += py / d
            den += 1 / d

        if coincident:
            break

        new_x = num_x / den
        new_y = num_y / den

        # Convergence check
        if math.hypot(new_x - x, new_y - y) < eps:
            break

        x, y = new_x, new_y

    return x, y


# -------------------------------
# TEST CASE 1
# -------------------------------
# Input: [[0,1],[1,0],[1,2],[2,1]]
# Expected Output: 4.00000

sensors1 = [(0, 1), (1, 0), (1, 2), (2, 1)]
hub1 = geometric_median(sensors1)

total_distance1 = sum(
    math.hypot(hub1[0] - x, hub1[1] - y) for x, y in sensors1
)

print("Output:", format(total_distance1, ".5f"))


# -------------------------------
# TEST CASE 2
# -------------------------------
# Input: [[0,0],[2,2]]
# Expected Output: 2.82843

sensors2 = [(0, 0), (2, 2)]
hub2 = geometric_median(sensors2)

total_distance2 = sum(
    math.hypot(hub2[0] - x, hub2[1] - y) for x, y in sensors2
)

print("Output:", format(total_distance2, ".5f"))
