import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def simulate_parking(num_trials=100000, max_wait_time=30, num_parking_spots=4, fast_forward=10):
    min_wait_times = []  # Store the minimum wait times for each trial
    avg_wait_times = []  # Store the running average of wait times

    # Set up the figure and axis
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Configure the top subplot for individual parking spots
    axs[0].set_xlim(-0.5, num_parking_spots - 0.5)
    axs[0].set_ylim(0, max_wait_time)
    axs[0].set_xticks(range(num_parking_spots))
    axs[0].set_xlabel('Parking Spot')
    axs[0].set_ylabel('Time Remaining (minutes)')
    axs[0].set_title('Parking Spot Availability')

    # Configure the bottom subplot for minimum and average wait times
    axs[1].set_xlim(0, num_trials)
    axs[1].set_ylim(0, max_wait_time)
    axs[1].set_xlabel('Trial')
    axs[1].set_ylabel('Time (minutes)')
    axs[1].set_title('Wait Time Simulation')

    # Line objects for the minimum wait time and average wait time
    min_line, = axs[1].plot([], [], label='Min Wait Time', lw=2, color='blue')
    avg_line, = axs[1].plot([], [], label='Average Wait Time', lw=2, color='red', linestyle='--')

    # Add a legend
    axs[1].legend(loc='upper right')

    # Initialize bar objects for parking spots
    bars = axs[0].bar(range(num_parking_spots), [0] * num_parking_spots, color='lightblue')

    # Initialize text annotations
    avg_text = axs[1].text(0.02, 0.92, '', transform=axs[1].transAxes, fontsize=12, color='red')
    min_text = axs[1].text(0.02, 0.85, '', transform=axs[1].transAxes, fontsize=12, color='blue')
    spot_texts = [axs[0].text(i, 0, '', ha='center', va='bottom', fontsize=10, color='black', clip_on=True) for i in range(num_parking_spots)]

    # Initialize the lines
    def init():
        min_line.set_data([], [])
        avg_line.set_data([], [])
        for bar in bars:
            bar.set_height(0)
        avg_text.set_text('')
        min_text.set_text('')
        for text in spot_texts:
            text.set_text('')
        return min_line, avg_line, *bars, avg_text, min_text, *spot_texts

    # Update function for each frame
    def update(frame):
        # Fast forward by `fast_forward` steps
        for _ in range(fast_forward):
            parking_spots = np.random.uniform(0, max_wait_time, num_parking_spots)
            min_wait = np.min(parking_spots)
            min_wait_times.append(min_wait)
            avg_wait_times.append(np.mean(min_wait_times))

        # Update parking spot bars and text
        for i, (bar, wait_time, text) in enumerate(zip(bars, parking_spots, spot_texts)):
            bar.set_height(wait_time)
            text.set_text(f'{wait_time:.1f}')
            # Adjust text position to avoid overlap
            text.set_position((i, wait_time + 1 if wait_time < max_wait_time - 1 else wait_time - 1))

        # Update line data
        min_line.set_data(range(len(min_wait_times)), min_wait_times)
        avg_line.set_data(range(len(avg_wait_times)), avg_wait_times)

        # Update text annotations
        avg_text.set_text(f'Avg Wait: {avg_wait_times[-1]:.2f} min')
        min_text.set_text(f'Min Wait: {min_wait_times[-1]:.2f} min')

        return min_line, avg_line, *bars, avg_text, min_text, *spot_texts

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=num_trials // fast_forward, init_func=init, blit=True, repeat=False)

    # Show the animation
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)  # Adjust the top of the plots to make space for the text
    plt.show()

    # Print the final average wait time
    final_avg_wait_time = np.mean(min_wait_times)
    print(f"Final Average Minimum Wait Time: {final_avg_wait_time:.2f} minutes")

# Run the simulation
simulate_parking()