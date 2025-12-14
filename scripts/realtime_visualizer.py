#!/usr/bin/env python3
"""
Real-time BCI Waveform Visualization System
Displays EEG signals, frequency spectrum, and classification results
Like modern professional BCI systems

SUPPORTS:
- Test mode: Generates simulated signals
- File mode: Loads EEG data from CSV/Excel files
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from scipy import signal
from scipy.fft import fft, fftfreq
import subprocess
import threading
import queue
import time
import re
import os
import sys

# Optional: pandas for CSV/Excel loading
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class BCIVisualizer:
    def __init__(self):
        # Configuration
        self.sampling_rate = 256  # Hz
        self.window_size = 256  # samples
        self.display_seconds = 3  # seconds to display
        self.update_interval = 50  # ms
        
        # Data buffers (use deque for O(1) pops)
        from collections import deque
        self.max_points = int(self.sampling_rate * self.display_seconds)
        self.time_data = deque(maxlen=self.max_points)
        self.signal_data = deque(maxlen=self.max_points)
        self.alpha_power_history = deque(maxlen=100)
        self.beta_power_history = deque(maxlen=100)
        
        # Pre-allocate arrays for plotting to avoid list->array conversion overhead
        self.plot_time = np.zeros(self.max_points)
        self.plot_signal = np.zeros(self.max_points)
        
        # Current state
        self.current_command = "NONE"
        self.current_alpha = 0.5
        self.current_beta = 0.5
        self.led_state = False
        self.buzzer_active = False
        
        # Data queue for thread-safe communication
        self.data_queue = queue.Queue()
        
        # Setup the figure
        self.setup_figure()
        
    def setup_figure(self):
        """Create the professional BCI interface"""
        # Create figure with dark background
        self.fig = plt.figure(figsize=(12, 8), facecolor='#1e1e1e')
        self.fig.canvas.manager.set_window_title('RISC-V Brain-Computer Interface - Real-time Monitor')
        
        # Create grid layout (3 columns for bottom section)
        gs = GridSpec(4, 3, figure=self.fig, hspace=0.4, wspace=0.3,
                     left=0.05, right=0.95, top=0.90, bottom=0.08)
        
        # 1. Main EEG Waveform (top, spans all 3 columns)
        self.ax_waveform = self.fig.add_subplot(gs[0:2, :])
        self.setup_waveform_plot()
        
        # 2. Frequency Spectrum (bottom left)
        self.ax_spectrum = self.fig.add_subplot(gs[2:, 0])
        self.setup_spectrum_plot()
        
        # 3. Feature Blocks (bottom middle) - Split into two rows
        self.ax_alpha = self.fig.add_subplot(gs[2, 1])
        self.ax_beta = self.fig.add_subplot(gs[3, 1])
        self.setup_feature_blocks()
        
        # 4. Status Panel (bottom right)
        self.ax_status = self.fig.add_subplot(gs[2:, 2])
        self.setup_status_panel()
        
    def setup_waveform_plot(self):
        """Setup the main EEG waveform display"""
        self.ax_waveform.set_facecolor('#0a0a0a')
        self.ax_waveform.set_title('EEG Signal - Time Domain', 
                                   fontsize=12, color='#00ff00', fontweight='bold')
        self.ax_waveform.set_xlabel('Time (seconds)', color='white')
        self.ax_waveform.set_ylabel('Amplitude (µV)', color='white')
        self.ax_waveform.grid(True, alpha=0.2, color='#00ff00', linestyle='--')
        self.ax_waveform.tick_params(colors='white')
        
        # Create the line plot
        self.line_waveform, = self.ax_waveform.plot([], [], color='#00ff00', 
                                                     linewidth=1.0, label='EEG Signal')
        
        # Autoscaling will handle limits
        self.ax_waveform.set_xlim(0, self.display_seconds)
        self.ax_waveform.set_ylim(-10, 10) # Start small so it expands
        
    def setup_spectrum_plot(self):
        """Setup frequency spectrum (FFT) display"""
        self.ax_spectrum.set_facecolor('#0a0a0a')
        self.ax_spectrum.set_title('Frequency Spectrum', 
                                   fontsize=10, color='#00ffff', fontweight='bold')
        self.ax_spectrum.set_xlabel('Frequency (Hz)', color='white')
        self.ax_spectrum.set_ylabel('Power', color='white')
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.set_ylim(0, 1000)
        self.ax_spectrum.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
        self.ax_spectrum.tick_params(colors='white')
        
        self.ax_spectrum.axvspan(8, 13, alpha=0.1, color='yellow')
        self.ax_spectrum.axvspan(13, 30, alpha=0.1, color='cyan')
        self.line_spectrum, = self.ax_spectrum.plot([], [], color='#00ffff', linewidth=1.5)
        
    def setup_feature_blocks(self):
        """Setup Alpha/Beta feature blocks (Alpha top, Beta bottom)"""
        # Alpha (Top)
        self.ax_alpha.set_facecolor('#0a0a0a')
        self.ax_alpha.set_title('Alpha Power (8-13Hz)', fontsize=10, color='yellow')
        self.ax_alpha.set_xlim(0, 1.0)
        self.ax_alpha.set_xticks([])
        self.ax_alpha.set_yticks([])
        self.bar_alpha = self.ax_alpha.barh([0], [0.5], color='yellow', alpha=0.7, height=0.5)
        self.text_alpha = self.ax_alpha.text(0.5, 0.5, '0.00', ha='center', va='center', 
                                            color='black', fontweight='bold')
        
        # Beta (Bottom)
        self.ax_beta.set_facecolor('#0a0a0a')
        self.ax_beta.set_title('Beta Power (13-30Hz)', fontsize=10, color='cyan')
        self.ax_beta.set_xlim(0, 1.0)
        self.ax_beta.set_xticks([])
        self.ax_beta.set_yticks([])
        self.bar_beta = self.ax_beta.barh([0], [0.5], color='cyan', alpha=0.7, height=0.5)
        self.text_beta = self.ax_beta.text(0.5, 0.5, '0.00', ha='center', va='center', 
                                          color='black', fontweight='bold')
        
    def setup_waveform_plot(self):
        """Setup the main EEG waveform display"""
        self.ax_waveform.set_facecolor('#0a0a0a')
        self.ax_waveform.set_title('EEG Signal - Time Domain', 
                                   fontsize=12, color='#00ff00', fontweight='bold')
        self.ax_waveform.set_xlabel('Time (seconds)', color='white')
        self.ax_waveform.set_ylabel('Amplitude (µV)', color='white')
        self.ax_waveform.grid(True, alpha=0.2, color='#00ff00', linestyle='--')
        self.ax_waveform.tick_params(colors='white')
        
        # Create the line plot
        self.line_waveform, = self.ax_waveform.plot([], [], color='#00ff00', 
                                                     linewidth=1.0, label='EEG Signal')
        
        # Initialization
        self.ax_waveform.set_xlim(0, self.display_seconds)
        self.ax_waveform.set_ylim(-100, 100)
        
    def setup_spectrum_plot(self):
        """Setup frequency spectrum (FFT) display"""
        self.ax_spectrum.set_facecolor('#0a0a0a')
        self.ax_spectrum.set_title('Frequency Spectrum (FFT)', 
                                   fontsize=10, color='#00ffff', fontweight='bold')
        self.ax_spectrum.set_xlabel('Frequency (Hz)', color='white')
        self.ax_spectrum.set_ylabel('Power', color='white')
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.set_ylim(0, 1000) # Fixed scale for performance
        self.ax_spectrum.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
        self.ax_spectrum.tick_params(colors='white')
        
        # Highlight frequency bands
        self.ax_spectrum.axvspan(8, 13, alpha=0.1, color='yellow')
        self.ax_spectrum.axvspan(13, 30, alpha=0.1, color='cyan')
        
        # Create the spectrum line (reused)
        self.line_spectrum, = self.ax_spectrum.plot([], [], color='#00ffff', linewidth=1.5)
        # We simulate fill using a polygon if needed, but line is faster
        
    def setup_feature_plot(self):
        """Setup feature bar chart"""
        self.ax_features.set_facecolor('#0a0a0a')
        self.ax_features.set_title('Band Power Features', 
                                   fontsize=10, color='#ffff00', fontweight='bold')
        self.ax_features.set_ylabel('Normalized Power', color='white')
        self.ax_features.set_ylim(0, 1.0)
        self.ax_features.tick_params(colors='white')
        self.ax_features.grid(True, alpha=0.2, axis='y', color='white')
        
        # Create initial bars
        self.bars_features = self.ax_features.bar(['Alpha', 'Beta'], [0.0, 0.0],
                                                   color=['yellow', 'cyan'], alpha=0.7)
        
    def setup_status_panel(self):
        """Setup status and classification display"""
        self.ax_status.set_facecolor('#0a0a0a')
        self.ax_status.axis('off')
        
        # Create text elements
        self.text_elements = {
            'command': self.ax_status.text(0.5, 0.80, 'Command: NONE', 
                                          ha='center', va='top', fontsize=14, 
                                          color='white', fontweight='bold'),
            'led': self.ax_status.text(0.5, 0.65, 'LED: OFF', 
                                       ha='center', va='top', fontsize=12, 
                                       color='#ff0000'),
            'stats': self.ax_status.text(0.5, 0.40, 'Alpha: 0.00 | Beta: 0.00', 
                                         ha='center', va='top', fontsize=10, 
                                         color='white'),
        }
        
    def generate_test_signal(self, command='NONE'):
        """Generate simulated EEG signal for testing"""
        t = np.arange(self.window_size) / self.sampling_rate
        
        if command == 'FOCUS':
            # High beta (21.5 Hz)
            signal_eeg = 30 * np.sin(2 * np.pi * 21.5 * t) + 15 * np.sin(2 * np.pi * 10.5 * t)
        elif command == 'RELAX':
            # High alpha (10.5 Hz)
            signal_eeg = 50 * np.sin(2 * np.pi * 10.5 * t) + 15 * np.sin(2 * np.pi * 21.5 * t)
        elif command == 'BLINK':
            # Normal + spike
            signal_eeg = 25 * np.sin(2 * np.pi * 10.5 * t) + 25 * np.sin(2 * np.pi * 21.5 * t)
            spike_idx = len(t) // 2
            signal_eeg[spike_idx-10:spike_idx+10] += 150 * np.exp(-((np.arange(20)-10)**2) / 10)
        else:
            signal_eeg = 25 * np.sin(2 * np.pi * 10.5 * t) + 25 * np.sin(2 * np.pi * 21.5 * t)
        
        # Add noise
        signal_eeg += np.random.normal(0, 5, len(t))
        return signal_eeg
    
    def compute_fft(self, signal_data):
        """Compute FFT of signal"""
        n = len(signal_data)
        if n < self.window_size:
            return None, None
        
        # Use numpy arrays for speed
        signal_arr = np.array(signal_data)
        yf = np.abs(fft(signal_arr[-self.window_size:]))
        xf = fftfreq(self.window_size, 1/self.sampling_rate)
        
        # Get positive frequencies 0-50Hz
        mask = (xf >= 0) & (xf <= 50)
        return xf[mask], yf[mask]
    
    def update_plot(self, frame):
        """Update all plots - optimized for speed"""
        # Process queue (limit to avoid blocking)
        points_processed = 0
        try:
            while not self.data_queue.empty() and points_processed < 50:
                data = self.data_queue.get_nowait()
                self.process_data(data)
                points_processed += 1
        except queue.Empty:
            pass
        
        artists = []
        
        # Update waveform
        if len(self.time_data) > 0:
            # Shift time to look continuous or fixed window? 
            # For performance, just plot the buffer against relative time or index
            t_data = list(self.time_data)
            y_data = list(self.signal_data)
            
            # Auto-scroll X axis if needed
            if t_data[-1] > self.ax_waveform.get_xlim()[1]:
                 self.ax_waveform.set_xlim(t_data[-1] - self.display_seconds, t_data[-1])
            
            # Auto-scale Y axis (every 10 frames)
            if frame % 10 == 0 and len(y_data) > 0:
                y_min, y_max = min(y_data), max(y_data)
                padding = max(10, (y_max - y_min) * 0.1)
                self.ax_waveform.set_ylim(y_min - padding, y_max + padding)
                 
            self.line_waveform.set_data(t_data, y_data)
            artists.append(self.line_waveform)
        
        # Update FFT spectrum (every 5th frame to save CPU)
        if frame % 5 == 0 and len(self.signal_data) >= self.window_size:
            xf, yf = self.compute_fft(self.signal_data)
            if xf is not None:
                self.line_spectrum.set_data(xf, yf)
                artists.append(self.line_spectrum)
        else:
            artists.append(self.line_spectrum)
        
        # Update feature bars
        # Update feature bars
        if len(self.alpha_power_history) > 0:
            self.bar_alpha[0].set_width(self.current_alpha)
            self.text_alpha.set_text(f'{self.current_alpha:.2f}')
            artists.append(self.bar_alpha[0])
            artists.append(self.text_alpha)
            
            self.bar_beta[0].set_width(self.current_beta)
            self.text_beta.set_text(f'{self.current_beta:.2f}')
            artists.append(self.bar_beta[0])
            artists.append(self.text_beta)
        
        # Update status panel
        self.update_status_panel()
        artists.extend(self.text_elements.values())
        
        return artists
    
    def update_status_panel(self):
        """Update the status text"""
        # Command color coding
        cmd_colors = {'FOCUS': '#00ff00', 'RELAX': '#00aaff', 'BLINK': '#ff9900', 'NONE': '#888888'}
        
        self.text_elements['command'].set_text(f'Command: {self.current_command}')
        self.text_elements['command'].set_color(cmd_colors.get(self.current_command, 'white'))
        
        led_text = 'LED: ON' if self.led_state else 'LED: OFF'
        self.text_elements['led'].set_text(led_text)
        self.text_elements['led'].set_color('#00ff00' if self.led_state else '#ff0000')
        
        self.text_elements['stats'].set_text(f'Alpha: {self.current_alpha:.2f} | Beta: {self.current_beta:.2f}')
    
    def process_data(self, data):
        """Process incoming data point"""
        self.time_data.append(data['time'])
        self.signal_data.append(data['amplitude'])
        
        if 'command' in data: self.current_command = data['command']
        if 'alpha_power' in data: 
            self.current_alpha = data['alpha_power']
            self.alpha_power_history.append(data['alpha_power'])
        if 'beta_power' in data: 
            self.current_beta = data['beta_power']
            self.beta_power_history.append(data['beta_power'])
        if 'led_state' in data: self.led_state = data['led_state']
    
    def run_from_stream(self, filepath='data/realtime_stream.csv'):
        """Run by reading a CSV file that is being written to in real-time"""
        print(f"Monitoring real-time stream: {filepath}")
        print("Waiting for data...")
        
        def monitor_file():
            last_pos = 0
            while True:
                try:
                    if os.path.exists(filepath):
                        with open(filepath, 'r') as f:
                            f.seek(last_pos)
                            lines = f.readlines()
                            last_pos = f.tell()
                            
                            for line in lines:
                                if line.startswith('time'): continue
                                try:
                                    parts = line.strip().split(',')
                                    if len(parts) >= 2:
                                        data = {
                                            'time': float(parts[0]),
                                            'amplitude': float(parts[1]),
                                            'alpha_power': float(parts[2]) if len(parts)>2 else 0.5,
                                            'beta_power': float(parts[3]) if len(parts)>3 else 0.5,
                                            'command': parts[4] if len(parts)>4 else 'NONE',
                                            'led_state': int(parts[5])==1 if len(parts)>5 else False
                                        }
                                        self.data_queue.put(data)
                                except:
                                    continue
                except:
                    pass
                time.sleep(0.05)
        
        thread = threading.Thread(target=monitor_file, daemon=True)
        thread.start()
        
        anim = animation.FuncAnimation(self.fig, self.update_plot, 
                                      interval=30, blit=True, cache_frame_data=False)
        plt.show()
    
    def run_with_bci(self, bci_executable='bin/bci_system.exe'):
        """Run with actual BCI system (TODO: implement data reading)"""
        print(f"Running with BCI system: {bci_executable}")
        print("This will be implemented once C code exports data")
        # TODO: Read data from BCI program output
        # For now, fall back to test mode
        self.run_test_mode()


def main():
    import sys
    
    visualizer = BCIVisualizer()
    
    # Check for test mode
    # Check mode
    if '--size' in sys.argv:
        pass # Handle resizing manually if needed?
        
    if '--stream' in sys.argv:
        visualizer.run_from_stream()
    elif '--test-mode' in sys.argv or '--test' in sys.argv:
        visualizer.run_test_mode()
    else:
        # Try to run with BCI, fall back to test mode
        print("BCI Waveform Visualizer")
        print("=" * 60)
        print("Usage:")
        print("  python realtime_visualizer.py --test-mode   # Test with simulated data")
        print("  python realtime_visualizer.py               # Connect to BCI system")
        print()
        visualizer.run_test_mode()


if __name__ == '__main__':
    main()
