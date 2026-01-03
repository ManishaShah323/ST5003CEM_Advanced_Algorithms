"""
Question 1(a): Optimizing Sensor Placement for Data Collection
Module: Advanced Algorithms (ST5003CEM)

This program finds the optimal location of a data aggregation hub
that minimizes the total Euclidean distance to all sensors.
The solution uses Weiszfeld’s Algorithm to compute the geometric median.
"""

import math


def min_total_distance(sensor_locations, epsilon=1e-7):
    """
    Computes the minimum total Euclidean distance from an optimal hub
    location to all given sensor locations.

    Parameters:
    sensor_locations (list): List of [x, y] coordinates of sensors
    epsilon (float): Convergence threshold

    Returns:
    float: Minimum total distance rounded to 5 decimal places
    """

    # Step 1: Initial guess using centroid
    x = sum(p[0] for p in sensor_locations) / len(sensor_locations)
    y = sum(p[1] for p in sensor_locations) / len(sensor_locations)

    # Step 2: Iterative optimization (Weiszfeld’s Algorithm)
    while True:
        num_x = 0
        num_y = 0
        den = 0

        for xi, yi in sensor_locations:
            dist = math.sqrt((x - xi) ** 2 + (y - yi) ** 2)

            # Avoid division by zero
            if dist == 0:
                continue

            num_x += xi / dist
            num_y += yi / dist
            den += 1 / dist

        new_x = num_x / den
        new_y = num_y / den

        # Step 3: Check convergence
        if abs(new_x - x) < epsilon and abs(new_y - y) < epsilon:
            break

        x, y = new_x, new_y

    # Step 4: Calculate minimum total distance
    total_distance = 0
    for xi, yi in sensor_locations:
        total_distance += math.sqrt((x - xi) ** 2 + (y - yi) ** 2)

    return round(total_distance, 5)


# ------------------- MAIN EXECUTION -------------------

if __name__ == "__main__":
    # Example Test Case 1
    sensors1 = [[0, 1], [1, 0], [1, 2], [2, 1]]
    print("Test Case 1 Sensor Locations:", sensors1)
    print("Minimum Total Distance:", min_total_distance(sensors1))
    print()

    # Example Test Case 2
    sensors2 = [[1, 1], [3, 3]]
    print("Test Case 2 Sensor Locations:", sensors2)
    print("Minimum Total Distance:", min_total_distance(sensors2))
