import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import stats


def simulate_parking(num_trials=1000, max_wait_time=30, num_parking_spots=4, fast_forward=10):
    min_wait_times = []  # Store the minimum wait times for each trial
    avg_wait_times = []  # Store the running average of wait times
    std_wait_times = []  # Store the running standard deviation of wait times

    # Set up the placeholders for the plots
    spot_chart_placeholder = st.empty()
    wait_time_chart_placeholder = st.empty()

    # Initialize matplotlib figures
    fig_spots, ax_spots = plt.subplots(figsize=(6, 4))
    fig_wait, ax_wait = plt.subplots(figsize=(6, 4))

    # Configure the parking spots plot
    ax_spots.set_xlim(-0.5, num_parking_spots - 0.5)
    ax_spots.set_ylim(0, max_wait_time)
    ax_spots.set_xticks(range(num_parking_spots))
    ax_spots.set_xlabel('Parking Spot')
    ax_spots.set_ylabel('Time Remaining (minutes)')
    ax_spots.set_title('Parking Spot Availability')

    # Initialize bar objects for parking spots
    bars_spots = ax_spots.bar(range(num_parking_spots), [0] * num_parking_spots, color='lightblue')

    # Initialize text annotations for parking spots
    spot_texts = [ax_spots.text(i, 0, '', ha='center', va='bottom', fontsize=10, color='black') for i in
                  range(num_parking_spots)]

    # Configure the wait time plot
    ax_wait.set_xlim(0, num_trials)
    ax_wait.set_ylim(0, max_wait_time)
    ax_wait.set_xlabel('Trial')
    ax_wait.set_ylabel('Time (minutes)')
    ax_wait.set_title('Wait Time Simulation')
    min_line, = ax_wait.plot([], [], label='Min Wait Time', lw=2, color='blue')
    avg_line, = ax_wait.plot([], [], label='Average Wait Time', lw=2, color='red', linestyle='--')
    ax_wait.legend(loc='upper right')

    # Initialize text annotations for average and min wait time
    avg_text = ax_wait.text(0.02, 0.92, '', transform=ax_wait.transAxes, fontsize=12, color='red')
    min_text = ax_wait.text(0.02, 0.85, '', transform=ax_wait.transAxes, fontsize=12, color='blue')

    # Run the simulation
    for trial in range(0, num_trials, fast_forward):
        # Fast forward by `fast_forward` steps
        for _ in range(fast_forward):
            parking_spots = np.random.uniform(0, max_wait_time, num_parking_spots)
            min_wait = np.min(parking_spots)
            min_wait_times.append(min_wait)
            avg_wait_times.append(np.mean(min_wait_times))
            std_wait_times.append(np.std(min_wait_times))

        # Update parking spot bars and texts
        for i, (bar, wait_time, text) in enumerate(zip(bars_spots, parking_spots, spot_texts)):
            bar.set_height(wait_time)
            # Adjust text position to avoid overlap
            text.set_position((i, wait_time + 1 if wait_time < max_wait_time - 1 else wait_time - 1))
            text.set_text(f'{wait_time:.1f}')

        # Refresh the parking spots plot
        ax_spots.figure.canvas.draw()
        spot_chart_placeholder.pyplot(fig_spots)

        # Update wait time lines
        min_line.set_data(range(len(min_wait_times)), min_wait_times)
        avg_line.set_data(range(len(avg_wait_times)), avg_wait_times)
        ax_wait.relim()
        ax_wait.autoscale_view()

        # Update text annotations for average and min wait time
        avg_text.set_text(f'Avg Wait: {avg_wait_times[-1]:.2f} min')
        # min_text.set_text(f'Min Wait: {min_wait_times[-1]:.2f} min')

        # Refresh the wait time plot
        ax_wait.figure.canvas.draw()
        wait_time_chart_placeholder.pyplot(fig_wait)

        # Optional: Control the speed of the animation
        time.sleep(0.1)

    # Return final average wait time
    final_avg_wait_time = avg_wait_times[-1]
    final_standard_error = std_wait_times[-1] / np.sqrt(num_trials)
    z_value = stats.norm.ppf(0.975)
    confidence_interval = z_value * final_standard_error
    return final_avg_wait_time, confidence_interval


def main():
    st.title("Geeza's Parking Spots Simulation")

    st.write("""
    This simulation calculates and visualises the average wait time before a parking spot 
    becomes available in the following setting.
    
    **Assumption:**
    
    We assume there are number of parking spots with constant demand. There is hard limit on 
    the maximum time a car can be parked in a spot. Each parking spot can become available uniformly
    between 0 and the maximum wait time. As soon as a parking spot becomes available, you can park your car.
    
    **Question: Assuming you arrive at a random time and want to park your car, what is the average minimum wait time?**
    
    **How to use this app:**
    
    Adjust the parameters below and click **Run Simulation** to see the animated results. When you start, the simulation
    will run for the number of trials you specify. For each trial, you will see the parking spots availability in the top plot.
    These are the time remaining for each parking spot to become available. The bottom plot shows the minimum wait time
    in blue and the average wait time in red. The average wait time is the average of all minimum wait times up to that point.
    You should see that the average wait time converges to a value as the number of trials increases.
    
    The default parameters are set to 20000 trials, 30 minutes maximum wait time, 4 parking spots, and 1 fast forward steps.
    Running the simulation for 20000 trials may result in the plots looking a bit dense, but is needed to get a good estimate.
    If you want to inspect the plots more closely, you can reduce the number of trials in a separate run.
    """)

    # Input parameters
    num_trials = st.number_input('Number of Trials', min_value=100, max_value=1000000, value=20000, step=100)
    max_wait_time = st.number_input('Maximum Wait Time (minutes)', min_value=1, max_value=120, value=30)
    num_parking_spots = st.number_input('Number of Parking Spots', min_value=1, max_value=20, value=4)
    fast_forward = st.number_input('Fast Forward Steps', min_value=1, max_value=100, value=1)

    if st.button('Run Simulation'):
        with st.spinner('Running simulation...'):
            final_avg_wait_time, confidence_interval = simulate_parking(
                num_trials=int(num_trials),
                max_wait_time=float(max_wait_time),
                num_parking_spots=int(num_parking_spots),
                fast_forward=int(fast_forward)
            )

        st.write(f"**Final Average Minimum Wait Time**: {final_avg_wait_time:.2f} minutes")
        st.write(f"**If you run the simulation many more times, you can expect the average wait time to be in the range of "
                 f"{final_avg_wait_time:.2f}±{ confidence_interval:.2f} minutes 95% of the time. The longer"
                 f"you run the trials, the smaller the uncertainty gets.**")


if __name__ == '__main__':
    main()