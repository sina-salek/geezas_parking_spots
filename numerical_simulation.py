import numpy as np

def avg_wait(num_trials, max_wait_time = 30, num_parking_spots = 4 ):
    min_wait = []
    for i in range(num_trials):
        parking_spots = np.random.uniform(0, max_wait_time, num_parking_spots)
        min_wait.append(np.min(parking_spots))
    return np.mean(min_wait)

print(avg_wait(1000000))

