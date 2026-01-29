# ============================================================
# QUESTION 5(b): Multithreaded Sorting Application
#
# Objective:
# - Divide a list into two equal halves
# - Sort each half using two separate threads
# - Merge the two sorted halves using a third thread
#
# Algorithm Used:
# Multithreaded Merge Sort
#
# Thread Structure:
# - Parent Thread: Creates and synchronizes all threads
# - Sorting Thread 1: Sorts first half of the array
# - Sorting Thread 2: Sorts second half of the array
# - Merging Thread: Merges the two sorted halves
#
# Synchronization:
# - join() is used to ensure:
#   1) Sorting threads complete BEFORE merging starts
#   2) Merging completes BEFORE final output is printed
#
# Time Complexity:
# Sorting: O(n log n)
# Merging: O(n)
# ============================================================

import threading

# ------------------------------------------------------------
# GLOBAL SHARED DATA
# ------------------------------------------------------------
# Global arrays are shared among all threads.
# This avoids passing large data structures between threads.

arr = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
n = len(arr)
mid = n // 2

# Temporary global array for merged result
temp = [0] * n


# ------------------------------------------------------------
# SORTING THREAD FUNCTION
# ------------------------------------------------------------
def sort_subarray(start, end):
    """
    Sorts a portion of the global array 'arr'
    from index 'start' to 'end' (exclusive).

    Each sorting thread operates on a DISTINCT
    subarray, so no race condition occurs.
    """
    arr[start:end] = sorted(arr[start:end])
    print(f"Thread sorting indices {start} to {end}: {arr[start:end]}")


# ------------------------------------------------------------
# MERGING THREAD FUNCTION
# ------------------------------------------------------------
def merge_subarrays(start, mid, end):
    """
    Merges two already sorted halves of 'arr'
    into the global temporary array 'temp'.

    IMPORTANT:
    This thread must execute ONLY AFTER
    both sorting threads have finished.
    """
    i = start
    j = mid
    k = start

    # Merge elements from both halves
    while i < mid and j < end:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1

    # Copy remaining elements from left half
    while i < mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    # Copy remaining elements from right half
    # (corrected boundary condition)
    while j < end:
        temp[k] = arr[j]
        j += 1
        k += 1

    print("Merging thread completed:", temp)


# ------------------------------------------------------------
# MAIN THREAD (PARENT THREAD)
# ------------------------------------------------------------
# The parent thread is responsible for:
# - Creating worker threads
# - Starting them
# - Synchronizing them using join()
# - Printing final output

print("Original Array:", arr)

# Create two sorting threads
t1 = threading.Thread(target=sort_subarray, args=(0, mid))
t2 = threading.Thread(target=sort_subarray, args=(mid, n))

# Start sorting threads
t1.start()
t2.start()

# ------------------------------------------------------------
# SYNCHRONIZATION POINT 1
# ------------------------------------------------------------
# join() ensures both sorting threads finish
# before the merging thread starts.
# This prevents race conditions.

t1.join()
t2.join()

# Create and start merging thread
t3 = threading.Thread(target=merge_subarrays, args=(0, mid, n))
t3.start()

# ------------------------------------------------------------
# SYNCHRONIZATION POINT 2
# ------------------------------------------------------------
# join() ensures merging completes
# before the parent thread prints final output.

t3.join()

# Final output printed by parent thread
print("Final Sorted Array:", temp)
