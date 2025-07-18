import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Serial settings
port = 'COM11'  # Change this to your actual port
baud_rate = 9600

# Initialize variables
ser = None
is_running = False
data = []

# Function to start serial connection and data acquisition
def start_acquisition():
    global ser, is_running
    if is_running:
        messagebox.showinfo("Info", "Data acquisition is already running!")
        return

    try:
        ser = serial.Serial(port, baud_rate)
        is_running = True
        data.clear()
        thread = threading.Thread(target=acquire_data)
        thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Could not open serial port: {e}")

# Function to stop data acquisition
def stop_acquisition():
    global is_running
    if not is_running:
        messagebox.showinfo("Info", "Data acquisition is not running!")
        return
    is_running = False

# Function to acquire data from serial
def acquire_data():
    global is_running, data
    while is_running:
        if ser and ser.is_open and ser.in_waiting > 0:
            try:
                line = ser.readline().decode().strip()
                if line:  # Check if the line is not empty
                    emg_value = int(line)
                    timestamp = time.time()
                    data.append((timestamp, emg_value))
                    update_plot()
            except ValueError:
                print("Received invalid data, skipping line...")
            except serial.SerialException:
                print("Serial connection issue, stopping acquisition.")
                is_running = False
        time.sleep(0.01)  # Adjust this delay as needed

# Function to update the plot
def update_plot():
    timestamps = [item[0] for item in data]
    emg_values = [item[1] for item in data]

    ax.clear()
    ax.plot(timestamps, emg_values, color='blue')
    ax.set_title("Real-Time EMG Data")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("EMG Signal")
    canvas.draw()

# Save the collected data to a CSV file
def save_data():
    if not data:
        messagebox.showinfo("Info", "No data to save!")
        return
    df = pd.DataFrame(data, columns=["Timestamp", "EMG Value"])
    df.to_csv("emg_data.csv", index=False)
    messagebox.showinfo("Info", "Data saved successfully!")

# Setup the GUI
root = tk.Tk()
root.title("EMG Data Acquisition")

# Create Start and Stop buttons
start_button = tk.Button(root, text="Start", command=start_acquisition)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_acquisition)
stop_button.pack(pady=5)

save_button = tk.Button(root, text="Save Data", command=save_data)
save_button.pack(pady=5)

# Matplotlib Figure
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the GUI event loop
root.protocol("WM_DELETE_WINDOW", stop_acquisition)  # Stop acquisition when closing the window
root.mainloop()

# Close the serial connection if open
if ser and ser.is_open:
    ser.close()
