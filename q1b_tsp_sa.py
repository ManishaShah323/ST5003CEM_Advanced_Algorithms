# ============================================================
# QUESTION 1(b): Traveling Salesperson Problem (TSP)
# Solved using Simulated Annealing with two cooling schedules
# ============================================================

import random
import math
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Fix random seed for reproducibility
# ------------------------------------------------------------
random.seed(42)

# ------------------------------------------------------------
# CITY GENERATION
# ------------------------------------------------------------
def generate_cities(n, lower=0, upper=1000):
    """
    Generates n cities with random (x, y) coordinates.
    """
    return [
        (random.uniform(lower, upper),
         random.uniform(lower, upper))
        for _ in range(n)
    ]


# ------------------------------------------------------------
# DISTANCE FUNCTIONS
# ------------------------------------------------------------
def euclidean_distance(a, b):
    """
    Computes Euclidean distance between two points.
    """
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def total_tour_distance(tour, cities):
    """
    Computes total distance of a closed TSP tour.
    """
    distance = 0
    for i in range(len(tour)):
        city_a = cities[tour[i]]
        city_b = cities[tour[(i + 1) % len(tour)]]
        distance += euclidean_distance(city_a, city_b)
    return distance


# ------------------------------------------------------------
# NEIGHBORHOOD OPERATORS
# ------------------------------------------------------------
def swap_neighborhood(tour):
    """
    Swap two random cities in the tour.
    """
    i, j = random.sample(range(len(tour)), 2)
    new_tour = tour[:]
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour


def two_opt_neighborhood(tour):
    """
    Reverse a segment of the tour (2-opt move).
    """
    i, j = sorted(random.sample(range(len(tour)), 2))
    return tour[:i] + tour[i:j][::-1] + tour[j:]


# ------------------------------------------------------------
# SIMULATED ANNEALING ALGORITHM
# ------------------------------------------------------------
def simulated_annealing(
    cities,
    cooling_type,
    T_initial=800,
    alpha=0.998,
    beta=5,
    max_iterations=2500
):
    """
    Simulated Annealing algorithm for TSP.

    cooling_type:
    - 'exponential' : T = T * alpha
    - 'linear'      : T = T - beta
    """

    n = len(cities)

    # Initial random tour
    current_tour = list(range(n))
    random.shuffle(current_tour)

    current_distance = total_tour_distance(current_tour, cities)
    best_distance = current_distance

    T = T_initial
    history = []

    for _ in range(max_iterations):

        # Select neighborhood operator
        if random.random() < 0.5:
            new_tour = swap_neighborhood(current_tour)
        else:
            new_tour = two_opt_neighborhood(current_tour)

        new_distance = total_tour_distance(new_tour, cities)
        delta = new_distance - current_distance

        # Acceptance condition
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = new_tour
            current_distance = new_distance

            if current_distance < best_distance:
                best_distance = current_distance

        history.append(best_distance)

        # Cooling schedule
        if cooling_type == "exponential":
            T *= alpha
        elif cooling_type == "linear":
            T = max(0.001, T - beta)

        # Stopping condition
        if T <= 0.001:
            break

    return best_distance, history


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
if __name__ == "__main__":

    # Number of cities
    N = 35
    cities = generate_cities(N)

    # Run Simulated Annealing with Exponential Cooling
    dist_exp, history_exp = simulated_annealing(
        cities, cooling_type="exponential"
    )

    # Run Simulated Annealing with Linear Cooling
    dist_lin, history_lin = simulated_annealing(
        cities, cooling_type="linear"
    )

    # Comparison
    improvement = dist_lin - dist_exp
    improvement_percent = (improvement / dist_lin) * 100 if dist_lin != 0 else 0

    print("\n================ FINAL COMPARISON ================")
    print("Number of Cities:", N)
    print("Exponential Cooling Distance:", round(dist_exp, 2))
    print("Linear Cooling Distance     :", round(dist_lin, 2))

    if improvement > 0:
        print(
            f"Exponential cooling improved the tour by "
            f"{round(improvement, 2)} units "
            f"({round(improvement_percent, 2)}%)."
        )
    else:
        print("Both cooling schedules produced similar results.")

    # --------------------------------------------------------
    # Plot convergence graph
    # --------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.plot(history_exp, label="Exponential Cooling")
    plt.plot(history_lin, label="Linear Cooling")
    plt.xlabel("Iteration")
    plt.ylabel("Best Tour Distance")
    plt.title("Simulated Annealing – Cooling Schedule Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()
