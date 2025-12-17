#!/usr/bin/env python3
"""
Visual Impairment BCI Visualization System
Specialized visualizer focusing on Alpha band power and visual impairment prediction
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button
from scipy.fft import fft, fftfreq
import queue
import time
from collections import deque
from datetime import datetime
import csv

class VisualImpairmentVisualizer:
    def __init__(self):
        # Configuration
        self.sampling_rate = 256
        self.window_size = 256
        self.display_seconds = 3
        self.update_interval = 50
        
        # Data buffers
        self.max_points = int(self.sampling_rate * self.display_seconds)
        self.time_data = deque(maxlen=self.max_points)
        self.signal_data = deque(maxlen=self.max_points)
        self.alpha_power_history = deque(maxlen=100)
        
        # Current state
        self.current_command = "NONE"
        self.current_alpha = 0.25
        self.led_state = False
        
        # Only visual impairment prediction
        self.visual_impairment = "NORMAL"
        
        # SESSION STATISTICS
        self.session_start = datetime.now()
        self.alpha_values = []
        self.prediction_counts = {'NORMAL': 0, 'BORDERLINE': 0, 'IMPAIRED': 0}
        self.total_samples = 0
        
        # Data queue
        self.data_queue = queue.Queue()
        
        # Setup figure
        self.setup_figure()
        
    def setup_figure(self):
        """Create the BCI interface"""
        # WHITE background
        self.fig = plt.figure(figsize=(14, 9), facecolor='white')  # Slightly larger for stats
        self.fig.canvas.manager.set_window_title('BCI - Visual Impairment')
        
        # Grid layout - with statistics panel
        gs = GridSpec(6, 3, figure=self.fig, 
                     hspace=1.0,
                     wspace=0.6,
                     left=0.08, right=0.92, 
                     top=0.94,
                     bottom=0.08)
        
        # Waveform (BLACK background)
        self.ax_waveform = self.fig.add_subplot(gs[0:2, :])
        self.setup_waveform_plot()
        
        # Spectrum (BLACK background)
        self.ax_spectrum = self.fig.add_subplot(gs[2:4, 0])
        self.setup_spectrum_plot()
        
        # Statistics Panel (NEW!)
        self.ax_stats_panel = self.fig.add_subplot(gs[2, 1:])
        self.setup_statistics_panel()
        
        # ONLY Alpha band power
        self.ax_alpha = self.fig.add_subplot(gs[3, 1])
        self.setup_feature_blocks()
        
        # Status panel
        self.ax_status = self.fig.add_subplot(gs[3, 2])
        self.setup_status_panel()
        
        # Visual impairment prediction
        self.ax_health = self.fig.add_subplot(gs[4, :])
        self.setup_health_panel()
        
        # Export buttons
        self.ax_btn_screenshot = self.fig.add_subplot(gs[5, 0])
        self.ax_btn_export = self.fig.add_subplot(gs[5, 1])
        self.setup_export_buttons()
        
        # Add system info at bottom
        info_text = f'Sampling Rate: {self.sampling_rate} Hz  |  Window: {self.window_size} samples  |  Display: {self.display_seconds}s  |  Dataset: Visual Impairment'
        self.fig.text(0.5, 0.02, info_text, ha='center', va='bottom', 
                     fontsize=8, color='black', fontweight='bold')
        
    def setup_waveform_plot(self):
        """Setup waveform with BLACK axis text"""
        self.ax_waveform.set_facecolor('#0a0a0a')
        self.ax_waveform.set_title('EEG Signal - Time Domain', 
                                   fontsize=12, color='#00ff00', fontweight='bold', pad=10)
        self.ax_waveform.set_xlabel('Time (seconds)', color='black', fontsize=10, fontweight='bold')
        self.ax_waveform.set_ylabel('Amplitude (µV)', color='black', fontsize=10, fontweight='bold')
        self.ax_waveform.grid(True, alpha=0.2, color='#00ff00', linestyle='--')
        self.ax_waveform.tick_params(axis='both', colors='black', labelsize=9, width=2, length=6)
        
        # White borders
        for spine in self.ax_waveform.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(2)
        
        self.line_waveform, = self.ax_waveform.plot([], [], color='#00ff00', linewidth=1.0)
        self.ax_waveform.set_xlim(0, self.display_seconds)
        self.ax_waveform.set_ylim(-10, 10)
        
    def setup_spectrum_plot(self):
        """Setup spectrum with BLACK axis text"""
        self.ax_spectrum.set_facecolor('#0a0a0a')
        self.ax_spectrum.set_title('Frequency Spectrum', 
                                   fontsize=10, color='#00ffff', fontweight='bold', pad=8)
        self.ax_spectrum.set_xlabel('Frequency (Hz)', color='black', fontsize=9, fontweight='bold')
        self.ax_spectrum.set_ylabel('Power', color='black', fontsize=9, fontweight='bold')
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.set_ylim(0, 1000)
        self.ax_spectrum.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
        self.ax_spectrum.tick_params(axis='both', colors='black', labelsize=8, width=2, length=6)
        
        # White borders
        for spine in self.ax_spectrum.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(2)
        
        self.ax_spectrum.axvspan(8, 13, alpha=0.15, color='yellow')
        self.line_spectrum, = self.ax_spectrum.plot([], [], color='#00ffff', linewidth=1.5)
        
    def setup_feature_blocks(self):
        """Setup ONLY Alpha band - PRIMARY focus for visual impairment"""
        # Alpha - PRIMARY (visual processing)
        self.ax_alpha.set_facecolor('white')
        self.ax_alpha.set_title('Alpha (8-13Hz)', fontsize=11, color='#cc9900', fontweight='bold', pad=8)
        self.ax_alpha.set_xlim(0, 1.0)
        self.ax_alpha.set_ylim(-0.15, 0.15)  # Tight fit around bar!
        self.ax_alpha.set_xticks([])
        self.ax_alpha.set_yticks([])
        for spine in self.ax_alpha.spines.values():
            spine.set_edgecolor('#cc9900')
            spine.set_linewidth(3)
        # Thicker bar for better visibility in compact layout
        self.bar_alpha = self.ax_alpha.barh([0], [0.25], color='gold', alpha=1.0, height=0.2)
        self.text_alpha = self.ax_alpha.text(0.5, 0, '0.25', ha='center', va='center', 
                                            color='black', fontweight='bold', fontsize=11)
        
    def setup_health_panel(self):
        """Setup ONLY visual impairment prediction"""
        self.ax_health.set_facecolor('white')
        self.ax_health.axis('off')
        self.ax_health.set_title('Visual Impairment Prediction', fontsize=10, color='#0066cc', fontweight='bold', loc='left')
        
        # Single centered prediction
        self.health_text = self.ax_health.text(
            0.5, 0.5, 'Visual: NORMAL', 
            ha='center', va='center', fontsize=10, 
            color='#00aa00', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#f0f0f0', 
                     edgecolor='#00aa00', linewidth=2, alpha=0.9))
    
    def setup_status_panel(self):
        """Setup status panel"""
        self.ax_status.set_facecolor('white')
        self.ax_status.axis('off')
        
        self.text_elements = {
            'command': self.ax_status.text(0.5, 0.90, 'Command:\nNONE', 
                                          ha='center', va='top', fontsize=11, 
                                          color='#333333', fontweight='bold'),
            'led': self.ax_status.text(0.5, 0.60, 'LED: OFF', 
                                       ha='center', va='top', fontsize=10, 
                                       color='#cc0000'),
            'stats': self.ax_status.text(0.5, 0.35, 'Alpha Power:\n0.25', 
                                         ha='center', va='top', fontsize=10, 
                                         color='#333333', fontweight='bold'),
        }
    
    def setup_statistics_panel(self):
        """Setup session statistics panel"""
        self.ax_stats_panel.set_facecolor('#f8f8f8')
        self.ax_stats_panel.axis('off')
        self.ax_stats_panel.set_title('📊 Session Statistics', fontsize=10, color='#0066cc', fontweight='bold', loc='left')
        
        self.stats_text = self.ax_stats_panel.text(
            0.5, 0.5, 'Session: 0s | Alpha Avg: 0.00 | Min: 0.00 | Max: 0.00 | Predictions: N:0 B:0 I:0', 
            ha='center', va='center', fontsize=9, color='#333333', fontweight='bold')
    
    def setup_export_buttons(self):
        """Setup export control buttons"""
        self.ax_btn_screenshot.axis('off')
        self.ax_btn_export.axis('off')
        
        # Save screenshot button
        self.btn_screenshot = Button(self.ax_btn_screenshot, '💾 Save Screenshot', color='#4CAF50', hovercolor='#45a049')
        self.btn_screenshot.label.set_fontsize(9)
        self.btn_screenshot.label.set_color('white')
        self.btn_screenshot.on_clicked(self.save_screenshot)
        
        # Export data button  
        self.btn_export = Button(self.ax_btn_export, '📁 Export Session Data', color='#2196F3', hovercolor='#0b7dda')
        self.btn_export.label.set_fontsize(9)
        self.btn_export.label.set_color('white')
        self.btn_export.on_clicked(self.export_session_data)
    
    def save_screenshot(self, event):
        """Save current visualization as PNG"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'visual_impairment_session_{timestamp}.png'
        self.fig.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
        print(f'\n✅ Screenshot saved: {filename}')
    
    def export_session_data(self, event):
        """Export session data to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'visual_impairment_data_{timestamp}.csv'
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Session Start', self.session_start.strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(['Session Duration (s)', (datetime.now() - self.session_start).total_seconds()])
            writer.writerow(['Total Samples', self.total_samples])
            writer.writerow(['Alpha Avg', np.mean(self.alpha_values) if self.alpha_values else 0])
            writer.writerow(['Alpha Min', np.min(self.alpha_values) if self.alpha_values else 0])
            writer.writerow(['Alpha Max', np.max(self.alpha_values) if self.alpha_values else 0])
            writer.writerow(['Predictions NORMAL', self.prediction_counts['NORMAL']])
            writer.writerow(['Predictions BORDERLINE', self.prediction_counts['BORDERLINE']])
            writer.writerow(['Predictions IMPAIRED', self.prediction_counts['IMPAIRED']])
        
        print(f'\n✅ Session data exported: {filename}')
    
    def update_statistics(self):
        """Update statistics display"""
        duration = (datetime.now() - self.session_start).total_seconds()
        avg_alpha = np.mean(self.alpha_values) if self.alpha_values else 0
        min_alpha = np.min(self.alpha_values) if self.alpha_values else 0
        max_alpha = np.max(self.alpha_values) if self.alpha_values else 0
        
        stats_text = (f'Session: {duration:.0f}s | '
                     f'Alpha Avg: {avg_alpha:.2f} Min: {min_alpha:.2f} Max: {max_alpha:.2f} | '
                     f'Predictions N:{self.prediction_counts["NORMAL"]} '
                     f'B:{self.prediction_counts["BORDERLINE"]} I:{self.prediction_counts["IMPAIRED"]}')
        self.stats_text.set_text(stats_text)
    
    def compute_fft(self, signal_data):
        """Compute FFT"""
        n = len(signal_data)
        if n < self.window_size:
            return None, None
        
        signal_arr = np.array(signal_data)
        yf = np.abs(fft(signal_arr[-self.window_size:]))
        xf = fftfreq(self.window_size, 1/self.sampling_rate)
        
        mask = (xf >= 0) & (xf <= 50)
        return xf[mask], yf[mask]
    
    def update_plot(self, frame):
        """Update all plots"""
        # Process queue
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
            t_data = list(self.time_data)
            y_data = list(self.signal_data)
            
            if t_data[-1] > self.ax_waveform.get_xlim()[1]:
                 self.ax_waveform.set_xlim(t_data[-1] - self.display_seconds, t_data[-1])
            
            if frame % 10 == 0 and len(y_data) > 0:
                y_min, y_max = min(y_data), max(y_data)
                padding = max(10, (y_max - y_min) * 0.1)
                self.ax_waveform.set_ylim(y_min - padding, y_max + padding)
                 
            self.line_waveform.set_data(t_data, y_data)
            artists.append(self.line_waveform)
        
        # Update FFT
        if frame % 5 == 0 and len(self.signal_data) >= self.window_size:
            xf, yf = self.compute_fft(self.signal_data)
            if xf is not None:
                self.line_spectrum.set_data(xf, yf)
                artists.append(self.line_spectrum)
        else:
            artists.append(self.line_spectrum)
        
        # Update Alpha band only
        if len(self.alpha_power_history) > 0:
            self.bar_alpha[0].set_width(self.current_alpha)
            self.text_alpha.set_text(f'{self.current_alpha:.2f}')
        
        # Update visual impairment prediction
        pred_colors = {'NORMAL': '#00aa00', 'BORDERLINE': '#cc8800', 'IMPAIRED': '#cc0000'}
        self.health_text.set_text(f'Visual: {self.visual_impairment}')
        self.health_text.set_color(pred_colors.get(self.visual_impairment, '#333333'))
        self.health_text.get_bbox_patch().set_edgecolor(pred_colors.get(self.visual_impairment, '#999999'))
        
        # Update status
        self.update_status_panel()
        artists.extend(self.text_elements.values())
        
        # Update session statistics (NEW!)
        if frame % 10 == 0:  # Update every 10 frames to avoid slowdown
            self.update_statistics()
        
        return artists
    
    def update_status_panel(self):
        """Update status text"""
        cmd_colors = {'FOCUS': '#00aa00', 'RELAX': '#0088cc', 'BLINK': '#cc6600', 'NONE': '#666666'}
        
        self.text_elements['command'].set_text(f'Command:\n{self.current_command}')
        self.text_elements['command'].set_color(cmd_colors.get(self.current_command, '#333333'))
        
        led_text = 'LED: ON' if self.led_state else 'LED: OFF'
        self.text_elements['led'].set_text(led_text)
        self.text_elements['led'].set_color('#00aa00' if self.led_state else '#cc0000')
        
        # Only Alpha band power - visual focus
        stats_text = f'Alpha Power:\n{self.current_alpha:.2f}'
        self.text_elements['stats'].set_text(stats_text)
        self.text_elements['stats'].set_color('#333333')
    
    def process_data(self, data):
        """Process incoming data - only visual impairment prediction"""
        self.time_data.append(data['time'])
        self.signal_data.append(data['amplitude'])
        
        if 'command' in data: self.current_command = data['command']
        if 'alpha_power' in data: 
            self.current_alpha = data['alpha_power']
            self.alpha_power_history.append(data['alpha_power'])
            # Track statistics
            self.alpha_values.append(data['alpha_power'])
        if 'led_state' in data: self.led_state = data['led_state']
        # ONLY visual impairment prediction
        if 'visual_impairment' in data:
            self.visual_impairment = data['visual_impairment']
            # Track prediction counts
            if data['visual_impairment'] in self.prediction_counts:
                self.prediction_counts[data['visual_impairment']] += 1
        
        self.total_samples += 1


# Main entry point
if __name__ == "__main__":
    # Check if file argument provided
    if len(sys.argv) < 2:
        print("Usage: python visualizer_visual_impairment.py <filename.csv>")
        print("Example: python visualizer_visual_impairment.py data/raw/visual_impairment_data.csv")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Try to import pandas
    try:
        import pandas as pd
        import threading
    except ImportError as e:
        print(f"ERROR: Missing required library: {e}")
        print("Install with: pip install pandas numpy matplotlib scipy")
        sys.exit(1)
    
    # Load and validate file
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    
    print(f"Loading Visual Impairment EEG data from: {filepath}")
    
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
            sys.exit(1)
    
    # Create visualizer
    vis = VisualImpairmentVisualizer()
    
    # Feed data from file
    def load_file_data():
        for _, row in df.iterrows():
            data = {
                'time': row['time'],
                'amplitude': row['amplitude'],
                'command': row.get('command', 'NONE'),
                'alpha_power': row.get('alpha_power', 0.25),
                'led_state': row.get('command', 'NONE') == 'FOCUS',
                'visual_impairment': row.get('visual_impairment', 'NORMAL'),
            }
            vis.data_queue.put(data)
            time.sleep(0.01)  # Slow playback
        
        print(f"\n✓ Visual Impairment data loaded!")
        print("Visualization showing Alpha band analysis")
        print("Close window to exit")
    
    # Start loading thread
    thread = threading.Thread(target=load_file_data, daemon=True)
    thread.start()
    
    # Setup animation
    anim = animation.FuncAnimation(vis.fig, vis.update_plot, 
                                  interval=vis.update_interval, 
                                  blit=False, cache_frame_data=False)
    
    print("\n📊 Starting Visual Impairment visualization...")
    print("Watch how Alpha band power relates to visual processing!")
    plt.show()
