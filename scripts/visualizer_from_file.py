#!/usr/bin/env python3
"""
BCI Visualizer - Load from CSV/Excel File
This script loads EEG data from files and visualizes it.

Answers your group member's question:
"We need to load EEG signals from CSV/Excel files, not just generate them"

Usage:
    python visualizer_from_file.py sample_eeg_data.csv
    python visualizer_from_file.py your_data.xlsx
"""

import sys
import os

# Add scripts directory to path so we can import realtime_visualizer
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Check if file argument provided
if len(sys.argv) < 2:
    print("Usage: python visualizer_from_file.py <filename.csv>")
    print("Example: python visualizer_from_file.py sample_eeg_data.csv")
    sys.exit(1)

filepath = sys.argv[1]

# Import the visualizer
try:
    from realtime_visualizer import BCIVisualizer
except ImportError:
    print("ERROR: Could not import BCIVisualizer")
    print("Make sure realtime_visualizer.py is in the same directory")
    sys.exit(1)

# Try to import pandas
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import time
    import queue
    import threading
except ImportError as e:
    print(f"ERROR: Missing required library: {e}")
    print("Install with: pip install pandas numpy matplotlib")
    sys.exit(1)

# Load and validate file
if not os.path.exists(filepath):
    print(f"ERROR: File not found: {filepath}")
    sys.exit(1)

# Detect dataset type from filename
dataset_type = "General"
if "visual" in filepath.lower():
    dataset_type = "Visual Impairment"
elif "motor" in filepath.lower():
    dataset_type = "Motor Impairment"
elif "attention" in filepath.lower():
    dataset_type = "Attention Deficit"

print(f"Loading EEG data from: {filepath}")
print(f"Dataset Type: {dataset_type}")

try:
    if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        df = pd.read_excel(filepath)
    else:  # CSV
        df = pd.read_csv(filepath)
    
    print(f"✓ Loaded {len(df)} data points")
    print(f"✓ Columns: {list(df.columns)}")
    
except Exception as e:
    print(f"ERROR loading file: {e}")
    sys.exit(1)

# Validate columns
required = ['time', 'amplitude']
for col in required:
    if col not in df.columns:
        print(f"ERROR: Missing required column '{col}'")
        print(f"Required columns: {required}")
        print(f"Optional columns: alpha_power, beta_power, command")
        sys.exit(1)

# Create visualizer
vis = BCIVisualizer()
# Store dataset type for display
vis.dataset_name = dataset_type

# Feed data from file
def load_file_data():
    for _, row in df.iterrows():
        data = {
            'time': row['time'],
            'amplitude': row['amplitude'],
            'command': row.get('command', 'NONE'),
            'theta_power': row.get('theta_power', 0.25),
            'alpha_power': row.get('alpha_power', 0.25),
            'beta_power': row.get('beta_power', 0.25),
            'gamma_power': row.get('gamma_power', 0.25),
            'led_state': row.get('command', 'NONE') == 'FOCUS',
            'visual_impairment': row.get('visual_impairment', 'NORMAL'),
            'motor_impairment': row.get('motor_impairment', 'NORMAL'),
            'attention_deficit': row.get('attention_deficit', 'NORMAL')
        }
        vis.data_queue.put(data)
        time.sleep(0.01)  # Slow playback
    
    print(f"\n✓ {dataset_type} data loaded!")
    print("Visualization showing how input is processed → output")
    print("Close window to exit")

# Start loading thread
thread = threading.Thread(target=load_file_data, daemon=True)
thread.start()

# Setup animation
anim = animation.FuncAnimation(vis.fig, vis.update_plot, 
                              interval=vis.update_interval, 
                              blit=False, cache_frame_data=False)

print("\\n📊 Starting visualization...")
print("Watch how the EEG data is processed and classified!")
plt.show()
