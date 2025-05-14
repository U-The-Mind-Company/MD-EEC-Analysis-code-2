import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import csv

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("XVG Files", "*.xvg")])
    if file_path:
        # Step 1: Read eigenvalues from the selected file
        eigenvalues = np.loadtxt(file_path, skiprows=24)  # Adjust the number of skiprows as needed

        # Initialize empty lists to store entropy and enthalpy values
        entropy_values = []
        enthalpy_values = []

        # Step 2: Calculate entropy and enthalpy for each time step
        for eigenvalue_set in eigenvalues:
            # Convert eigenvalues to frequencies (omega)
            frequencies = np.sqrt(eigenvalue_set)

            # Boltzmann's constant in kJ/(mol*K)
            kb = 0.0083144621

            # Temperature in Kelvin
            temperature = 300  # Replace with the temperature of your simulation

            # Calculate entropy using Schlitter's formula
            entropy = kb * temperature * np.log(2.0 * np.pi * np.e / frequencies[1])

            # Calculate enthalpy using the frequencies (assuming harmonic oscillator model)
            enthalpy = np.sum(0.5 * kb * temperature * frequencies)

            # Append the entropy and enthalpy values to their respective lists
            entropy_values.append(entropy)
            enthalpy_values.append(enthalpy)

        # Step 3: Create three subplots, one for entropy, one for enthalpy, and one for entropy vs. enthalpy
        time_steps = np.arange(0, len(entropy_values))  # Assuming time steps are uniformly spaced

        # Create a figure with three subplots (1 row, 3 columns)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

        # Plot entropy vs. time in the first subplot
        ax1.plot(time_steps, entropy_values, label='Entropy vs. Time', color='blue')
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Entropy')
        ax1.set_title('Entropy vs. Time for MD Simulation')
        ax1.grid(True)

        # Plot enthalpy vs. time in the second subplot
        ax2.plot(time_steps, enthalpy_values, label='Enthalpy vs. Time', color='red')
        ax2.set_xlabel('Time Step')
        ax2.set_ylabel('Enthalpy')
        ax2.set_title('Enthalpy vs. Time for MD Simulation')
        ax2.grid(True)

        # Plot entropy vs. enthalpy in the third subplot
        ax3.plot(entropy_values, enthalpy_values, label='Entropy vs. Enthalpy', color='green')
        ax3.set_xlabel('Entropy')
        ax3.set_ylabel('Enthalpy')
        ax3.set_title('Entropy vs. Enthalpy for MD Simulation')
        ax3.grid(True)

        # Adjust spacing between subplots
        plt.tight_layout()

        # Step 4: Save entropy and enthalpy data to a CSV file
        csv_filename = "entropy_and_enthalpy_data.csv"
        with open(csv_filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Time Step", "Entropy", "Enthalpy"])  # Write the header

            for time_step, entropy, enthalpy in zip(time_steps, entropy_values, enthalpy_values):
                csv_writer.writerow([time_step, entropy, enthalpy])

        print(f"Data saved to {csv_filename}")

        # Step 5: Create three subplots and display them
        plt.show()

# Create a Tkinter window
root = tk.Tk()
root.title("MD Simulation Analysis")

# Set the window size
root.geometry("50x100")  # Set your desired width and height

# Create a frame to hold the button and center it
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

# Create the "Load File" button and center it in the frame
load_button = tk.Button(frame, text="Load File", command=load_file)
load_button.pack(pady=20)  # Add some padding to center the button vertically

root.mainloop()
