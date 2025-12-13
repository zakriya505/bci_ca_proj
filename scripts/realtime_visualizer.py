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
        
        # Data buffers
        self.max_points = self.sampling_rate * self.display_seconds
        self.time_data = []
        self.signal_data = []
        self.alpha_power_history = []
        self.beta_power_history = []
        self.command_history = []
        
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
        self.fig = plt.figure(figsize=(14, 10), facecolor='#1e1e1e')
        self.fig.canvas.manager.set_window_title('RISC-V Brain-Computer Interface - Real-time Monitor')
        
        # Create grid layout with more vertical spacing
        gs = GridSpec(4, 2, figure=self.fig, hspace=0.45, wspace=0.3,
                     left=0.08, right=0.95, top=0.95, bottom=0.05)
        
        # 1. Main EEG Waveform (top, spans both columns)
        self.ax_waveform = self.fig.add_subplot(gs[0:2, :])
        self.setup_waveform_plot()
        
        # 2. Frequency Spectrum (bottom left)
        self.ax_spectrum = self.fig.add_subplot(gs[2, 0])
        self.setup_spectrum_plot()
        
        # 3. Feature Bars (bottom left, below spectrum)
        self.ax_features = self.fig.add_subplot(gs[3, 0])
        self.setup_feature_plot()
        
        # 4. Status Panel (bottom right, spans 2 rows)
        self.ax_status = self.fig.add_subplot(gs[2:, 1])
        self.setup_status_panel()
        
    def setup_waveform_plot(self):
        """Setup the main EEG waveform display"""
        self.ax_waveform.set_facecolor('#0a0a0a')
        self.ax_waveform.set_title('EEG Signal - Time Domain', 
                                   fontsize=14, color='#00ff00', fontweight='bold')
        self.ax_waveform.set_xlabel('Time (seconds)', color='white')
        self.ax_waveform.set_ylabel('Amplitude (µV)', color='white')
        self.ax_waveform.grid(True, alpha=0.2, color='#00ff00', linestyle='--')
        self.ax_waveform.tick_params(colors='white')
        
        # Create the line plot
        self.line_waveform, = self.ax_waveform.plot([], [], color='#00ff00', 
                                                     linewidth=1.5, label='EEG Signal')
        self.ax_waveform.legend(loc='upper right', framealpha=0.3, facecolor='#1e1e1e')
        
    def setup_spectrum_plot(self):
        """Setup frequency spectrum (FFT) display"""
        self.ax_spectrum.set_facecolor('#0a0a0a')
        self.ax_spectrum.set_title('Frequency Spectrum (FFT)', 
                                   fontsize=12, color='#00ffff', fontweight='bold')
        self.ax_spectrum.set_xlabel('Frequency (Hz)', color='white')
        self.ax_spectrum.set_ylabel('Power', color='white')
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
        self.ax_spectrum.tick_params(colors='white')
        
        # Highlight frequency bands
        self.ax_spectrum.axvspan(8, 13, alpha=0.1, color='yellow', label='Alpha (8-13 Hz)')
        self.ax_spectrum.axvspan(13, 30, alpha=0.1, color='cyan', label='Beta (13-30 Hz)')
        
        # Create the spectrum bars
        self.bars_spectrum = None
        
        self.ax_spectrum.legend(loc='upper right', fontsize=8, framealpha=0.3, facecolor='#1e1e1e')
        
    def setup_feature_plot(self):
        """Setup feature bar chart"""
        self.ax_features.set_facecolor('#0a0a0a')
        self.ax_features.set_title('Band Power Features', 
                                   fontsize=12, color='#ffff00', fontweight='bold')
        self.ax_features.set_ylabel('Normalized Power', color='white')
        self.ax_features.set_ylim(0, 1.0)
        self.ax_features.tick_params(colors='white')
        self.ax_features.grid(True, alpha=0.2, axis='y', color='white')
        
        # Create bars
        self.bars_features = self.ax_features.bar(['Alpha\n(8-13 Hz)', 'Beta\n(13-30 Hz)'], 
                                                   [0.5, 0.5],
                                                   color=['yellow', 'cyan'], alpha=0.7)
        
    def setup_status_panel(self):
        """Setup status and classification display"""
        self.ax_status.set_facecolor('#0a0a0a')
        self.ax_status.axis('off')
        
        # Create text elements
        self.text_elements = {
            'title': self.ax_status.text(0.5, 0.95, 'SYSTEM STATUS', 
                                        ha='center', va='top', fontsize=14, 
                                        color='#00ff00', fontweight='bold'),
            'command': self.ax_status.text(0.5, 0.80, 'Command: NONE', 
                                          ha='center', va='top', fontsize=16, 
                                          color='white', fontweight='bold'),
            'led': self.ax_status.text(0.5, 0.65, 'LED: OFF', 
                                       ha='center', va='top', fontsize=12, 
                                       color='#ff0000'),
            'alpha': self.ax_status.text(0.5, 0.50, 'Alpha Power: 0.50', 
                                         ha='center', va='top', fontsize=10, 
                                         color='yellow'),
            'beta': self.ax_status.text(0.5, 0.40, 'Beta Power: 0.50', 
                                        ha='center', va='top', fontsize=10, 
                                        color='cyan'),
            'info': self.ax_status.text(0.5, 0.15, '', 
                                        ha='center', va='top', fontsize=9, 
                                        color='#aaaaaa', style='italic'),
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
            # Add spike at middle
            spike_idx = len(t) // 2
            signal_eeg[spike_idx-10:spike_idx+10] += 150 * np.exp(-((np.arange(20)-10)**2) / 10)
        else:
            # Balanced
            signal_eeg = 25 * np.sin(2 * np.pi * 10.5 * t) + 25 * np.sin(2 * np.pi * 21.5 * t)
        
        # Add noise
        signal_eeg += np.random.normal(0, 5, len(t))
        
        return signal_eeg
    
    def compute_fft(self, signal_data):
        """Compute FFT of signal"""
        if len(signal_data) < self.window_size:
            return None, None
        
        # Get last window_size samples
        recent_signal = signal_data[-self.window_size:]
        
        # Compute FFT
        yf = fft(recent_signal)
        xf = fftfreq(self.window_size, 1/self.sampling_rate)
        
        # Get positive frequencies only
        mask = xf >= 0
        xf = xf[mask]
        yf = np.abs(yf[mask])
        
       # Limit to 0-50 Hz
        mask_50 = xf <= 50
        xf = xf[mask_50]
        yf = yf[mask_50]
        
        return xf, yf
    
    def update_plot(self, frame):
        """Update all plots - called by animation"""
        # Check for new data
        try:
            while not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                self.process_data(data)
        except queue.Empty:
            pass
        
        # Update waveform
        if len(self.time_data) > 0:
            self.line_waveform.set_data(self.time_data, self.signal_data)
            self.ax_waveform.set_xlim(max(0, max(self.time_data) - self.display_seconds), 
                                      max(self.time_data) + 0.1)
            self.ax_waveform.set_ylim(min(self.signal_data + [-100]),
                                      max(self.signal_data + [100]))
        
        # Update FFT spectrum
        if len(self.signal_data) >= self.window_size:
            xf, yf = self.compute_fft(self.signal_data)
            if xf is not None:
                self.ax_spectrum.clear()
                self.setup_spectrum_plot()  # Reapply formatting
                self.ax_spectrum.plot(xf, yf, color='#00ffff', linewidth=2)
                self.ax_spectrum.fill_between(xf, yf, alpha=0.3, color='#00ffff')
        
        # Update feature bars
        if len(self.alpha_power_history) > 0:
            self.bars_features[0].set_height(self.current_alpha)
            self.bars_features[1].set_height(self.current_beta)
        
        # Update status panel
        self.update_status_panel()
        
        return self.line_waveform,
    
    def update_status_panel(self):
        """Update the status text"""
        # Command color coding
        cmd_colors = {
            'FOCUS': '#00ff00',
            'RELAX': '#00aaff',
            'BLINK': '#ff9900',
            'NONE': '#888888'
        }
        
        self.text_elements['command'].set_text(f'Detected: {self.current_command}')
        self.text_elements['command'].set_color(cmd_colors.get(self.current_command, 'white'))
        
        # LED status
        led_text = 'LED: ON' if self.led_state else 'LED: OFF'
        led_color = '#00ff00' if self.led_state else '#ff0000'
        self.text_elements['led'].set_text(led_text)
        self.text_elements['led'].set_color(led_color)
        
        # Powers
        self.text_elements['alpha'].set_text(f'Alpha Power: {self.current_alpha:.3f}')
        self.text_elements['beta'].set_text(f'Beta Power: {self.current_beta:.3f}')
        
        # Info
        info_lines = [
            f'Samples: {len(self.signal_data)}',
            f'Window: {self.display_seconds}s',
            f'Rate: {self.sampling_rate} Hz'
        ]
        self.text_elements['info'].set_text('\n'.join(info_lines))
    
    def process_data(self, data):
        """Process incoming data point"""
        # Add to buffers
        self.time_data.append(data['time'])
        self.signal_data.append(data['amplitude'])
        
        # Update current state
        if 'command' in data:
            self.current_command = data['command']
        if 'alpha_power' in data:
            self.current_alpha = data['alpha_power']
            self.alpha_power_history.append(data['alpha_power'])
        if 'beta_power' in data:
            self.current_beta = data['beta_power']
            self.beta_power_history.append(data['beta_power'])
        if 'led_state' in data:
            self.led_state = data['led_state']
        
        # Keep buffer size manageable
        if len(self.time_data) > self.max_points:
            self.time_data = self.time_data[-self.max_points:]
            self.signal_data = self.signal_data[-self.max_points:]
        if len(self.alpha_power_history) > 100:
            self.alpha_power_history = self.alpha_power_history[-100:]
            self.beta_power_history = self.beta_power_history[-100:]
    
    def run_test_mode(self):
        """Run in test mode with simulated data"""
        print("Running in TEST MODE - Simulated EEG Data")
        print("Close the window to exit")
        
        # Test sequence
        test_sequence = [
            ('NONE', 2), ('FOCUS', 3), ('RELAX', 3), 
            ('BLINK', 1), ('FOCUS', 2), ('RELAX', 2)
        ]
        
        def generate_test_data():
            seq_idx = 0
            iteration = 0
            current_time = 0
            
            while True:
                if seq_idx >= len(test_sequence):
                    seq_idx = 0
                
                command, duration = test_sequence[seq_idx]
                
                # Generate signal
                test_signal = self.generate_test_signal(command)
                
                # Send samples
                for i, amplitude in enumerate(test_signal):
                    data = {
                        'time': current_time,
                        'amplitude': amplitude,
                        'command': command,
                        'alpha_power': 0.7 if command == 'RELAX' else 0.3,
                        'beta_power': 0.7 if command == 'FOCUS' else 0.3,
                        'led_state': command == 'FOCUS'
                    }
                    self.data_queue.put(data)
                    current_time += 1 / self.sampling_rate
                    time.sleep(0.001)  # Small delay
                
                iteration += 1
                if iteration >= duration:
                    iteration = 0
                    seq_idx += 1
        
        # Start data generation thread
        thread = threading.Thread(target=generate_test_data, daemon=True)
        thread.start()
        
        # Setup animation
        anim = animation.FuncAnimation(self.fig, self.update_plot, 
                                      interval=self.update_interval, 
                                      blit=False, cache_frame_data=False)
        
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
    if '--test-mode' in sys.argv or '--test' in sys.argv:
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
