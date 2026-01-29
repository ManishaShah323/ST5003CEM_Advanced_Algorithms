from collections import defaultdict

# =====================================================
# QUESTION 4: Smart Energy Grid Load Optimization
#
# Objective:
# Allocate energy from Solar, Hydro, and Diesel sources
# to meet hourly district demand at minimum cost while:
# - Respecting capacity and availability constraints
# - Allowing ±10% demand tolerance
# - Explicitly minimizing diesel usage
#
# Algorithm Used:
# Dynamic Programming (Knapsack-style) + Greedy Ordering
#
# Time Complexity:
# O(h × s × c²)
# h = number of hours
# s = number of energy sources
# c = capacity range
# =====================================================


# ---------------------
# INPUT DATA
# ---------------------
hours = [6, 7, 18, 19]

district_demands = {
    6: {"A": 20, "B": 15, "C": 25},
    7: {"A": 22, "B": 16, "C": 28},
    18: {"A": 30, "B": 20, "C": 35},
    19: {"A": 32, "B": 22, "C": 38},
}

energy_sources = {
    "Solar": {
        "capacity": 50,
        "cost": 1.0,
        "available": lambda h: 6 <= h <= 18,
        "renewable": True
    },
    "Hydro": {
        "capacity": 40,
        "cost": 1.5,
        "available": lambda h: True,
        "renewable": True
    },
    "Diesel": {
        "capacity": 60,
        "cost": 3.0,
        "available": lambda h: 17 <= h <= 23,
        "renewable": False
    }
}

# ±10% demand tolerance
TOLERANCE = 0.10

# Explicit diesel penalty to discourage its usage
DIESEL_PENALTY = 1000


# =====================================================
# DYNAMIC PROGRAMMING ENERGY ALLOCATION FUNCTION
# =====================================================
def allocate_energy_dp(hour, demand_total):
    """
    DP + GREEDY HYBRID MODEL

    DP State:
    dp[i][e] = minimum cost to generate 'e' kWh
               using first 'i' available energy sources

    Objective:
    Minimize total cost such that:
    demand*(1 - tolerance) ≤ e ≤ demand*(1 + tolerance)

    Diesel Minimization:
    Diesel usage is penalized in DP cost so it is used
    only if renewable sources cannot meet demand.
    """

    # Select sources available at this hour
    sources = [
        s for s in energy_sources
        if energy_sources[s]["available"](hour)
    ]

    # Greedy ordering: cheapest source first
    sources.sort(key=lambda s: energy_sources[s]["cost"])

    min_required = int(demand_total * (1 - TOLERANCE))
    max_required = int(demand_total * (1 + TOLERANCE))

    # DP table: (i, energy) → min cost
    dp = defaultdict(lambda: float("inf"))
    parent = {}

    # Base case
    dp[(0, 0)] = 0

    # ---------------------
    # DP TABLE CONSTRUCTION
    # ---------------------
    for i, src in enumerate(sources):
        cap = energy_sources[src]["capacity"]
        cost = energy_sources[src]["cost"]

        for (prev_i, prev_energy), prev_cost in list(dp.items()):
            if prev_i != i:
                continue

            for used in range(cap + 1):
                new_energy = prev_energy + used

                # Explicit diesel penalty
                penalty = DIESEL_PENALTY if src == "Diesel" and used > 0 else 0
                new_cost = prev_cost + used * cost + penalty

                state = (i + 1, new_energy)

                if new_cost < dp[state]:
                    dp[state] = new_cost
                    parent[state] = (src, used, prev_energy)

    # ---------------------
    # SELECT BEST FEASIBLE SOLUTION
    # ---------------------
    best_state = None
    best_cost = float("inf")

    for (i, energy), cost in dp.items():
        if i == len(sources) and min_required <= energy <= max_required:
            if cost < best_cost:
                best_cost = cost
                best_state = (i, energy)

    if best_state is None:
        return None, None

    # ---------------------
    # BACKTRACK SOLUTION
    # ---------------------
    allocation = defaultdict(int)
    i, energy = best_state

    while i > 0:
        src, used, prev_energy = parent[(i, energy)]
        allocation[src] += used
        energy = prev_energy
        i -= 1

    return allocation, best_cost


# =====================================================
# MAIN HOURLY ALLOCATION LOOP
# =====================================================
total_cost = 0
total_energy = 0
renewable_energy = 0
diesel_hours = []

print("\nFINAL ENERGY ALLOCATION TABLE")
print("Hour | Demand | Solar | Hydro | Diesel | Total Used | Cost")
print("-" * 65)

for hour in hours:
    demand = sum(district_demands[hour].values())
    allocation, cost = allocate_energy_dp(hour, demand)

    if allocation is None:
        print(f"{hour} | Demand not satisfied")
        continue

    solar = allocation.get("Solar", 0)
    hydro = allocation.get("Hydro", 0)
    diesel = allocation.get("Diesel", 0)

    total_used = solar + hydro + diesel

    total_energy += total_used
    total_cost += cost

    if solar:
        renewable_energy += solar
    if hydro:
        renewable_energy += hydro
    if diesel > 0:
        diesel_hours.append(hour)

    print(f"{hour:>4} | {demand:>6} | {solar:>5} | {hydro:>5} | {diesel:>6} | {total_used:>10} | Rs.{cost}")

# =====================================================
# FINAL ANALYSIS REPORT
# =====================================================
renewable_percentage = (renewable_energy / total_energy) * 100 if total_energy else 0

print("\nSUMMARY ANALYSIS")
print("----------------------------")
print(f"Total Energy Supplied     : {total_energy} kWh")
print(f"Renewable Energy Supplied : {renewable_energy} kWh")
print(f"Renewable Energy %        : {renewable_percentage:.2f}%")
print(f"Total Cost               : Rs. {total_cost}")
print(f"Diesel Used In Hours      : {sorted(set(diesel_hours))}")
print("Diesel usage occurred only when renewable sources could not meet demand within ±10% tolerance.")
