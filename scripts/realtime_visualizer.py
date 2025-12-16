#!/usr/bin/env python3
"""
Real-time BCI Waveform Visualization System with Health Predictions
Displays EEG signals, 4 frequency bands, and 3 health predictions
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from scipy.fft import fft, fftfreq
import queue
import time

class BCIVisualizer:
    def __init__(self):
        # Configuration
        self.sampling_rate = 256
        self.window_size = 256
        self.display_seconds = 3
        self.update_interval = 50
        
        # Data buffers
        from collections import deque
        self.max_points = int(self.sampling_rate * self.display_seconds)
        self.time_data = deque(maxlen=self.max_points)
        self.signal_data = deque(maxlen=self.max_points)
        self.theta_power_history = deque(maxlen=100)
        self.alpha_power_history = deque(maxlen=100)
        self.beta_power_history = deque(maxlen=100)
        self.gamma_power_history = deque(maxlen=100)
        
        # Current state
        self.current_command = "NONE"
        self.current_theta = 0.25
        self.current_alpha = 0.25
        self.current_beta = 0.25
        self.current_gamma = 0.25
        self.led_state = False
        
        # Health predictions
        self.visual_impairment = "NORMAL"
        self.motor_impairment = "NORMAL"
        self.attention_deficit = "NORMAL"
        
        # Data queue
        self.data_queue = queue.Queue()
        
        # Setup figure
        self.setup_figure()
        
    def setup_figure(self):
        """Create the BCI interface"""
        # WHITE background
        self.fig = plt.figure(figsize=(12, 8), facecolor='white')
        self.fig.canvas.manager.set_window_title('BCI - Real-time Monitor')
        
        # Grid layout with MORE SPACING
        gs = GridSpec(5, 4, figure=self.fig, 
                     hspace=0.8,    # Increased from 0.5 - more vertical space
                     wspace=0.4,    # Increased from 0.3 - more horizontal space
                     left=0.06, right=0.94, 
                     top=0.92,      # More space at top
                     bottom=0.08)   # More space at bottom
        
        # Waveform (BLACK background)
        self.ax_waveform = self.fig.add_subplot(gs[0:2, :])
        self.setup_waveform_plot()
        
        # Spectrum (BLACK background)
        self.ax_spectrum = self.fig.add_subplot(gs[2:4, 0])
        self.setup_spectrum_plot()
        
        # Band powers (WHITE backgrounds)
        self.ax_theta = self.fig.add_subplot(gs[2, 1])
        self.ax_alpha = self.fig.add_subplot(gs[2, 2])
        self.ax_beta = self.fig.add_subplot(gs[3, 1])
        self.ax_gamma = self.fig.add_subplot(gs[3, 2])
        self.setup_feature_blocks()
        
        # Status panel (WHITE)
        self.ax_status = self.fig.add_subplot(gs[2:4, 3])
        self.setup_status_panel()
        
        # Health predictions (WHITE)
        self.ax_health = self.fig.add_subplot(gs[4, :])
        self.setup_health_panel()
        
        # Add system info at bottom
        info_text = f'Sampling Rate: {self.sampling_rate} Hz  |  Window Size: {self.window_size} samples  |  Display: {self.display_seconds}s'
        self.fig.text(0.5, 0.02, info_text, ha='center', va='bottom', 
                     fontsize=9, color='black', fontweight='bold')
        
    def setup_waveform_plot(self):
        """Setup waveform with BLACK axis text"""
        self.ax_waveform.set_facecolor('#0a0a0a')
        self.ax_waveform.set_title('EEG Signal - Time Domain', 
                                   fontsize=12, color='#00ff00', fontweight='bold')
        self.ax_waveform.set_xlabel('Time (seconds)', color='black', fontsize=11, fontweight='bold')
        self.ax_waveform.set_ylabel('Amplitude (µV)', color='black', fontsize=11, fontweight='bold')
        self.ax_waveform.grid(True, alpha=0.2, color='#00ff00', linestyle='--')
        self.ax_waveform.tick_params(axis='both', colors='black', labelsize=10, width=2, length=6)
        
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
                                   fontsize=10, color='#00ffff', fontweight='bold')
        self.ax_spectrum.set_xlabel('Frequency (Hz)', color='black', fontsize=10, fontweight='bold')
        self.ax_spectrum.set_ylabel('Power', color='black', fontsize=10, fontweight='bold')
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.set_ylim(0, 1000)
        self.ax_spectrum.grid(True, alpha=0.2, color='#00ffff', linestyle='--')
        self.ax_spectrum.tick_params(axis='both', colors='black', labelsize=9, width=2, length=6)
        
        # White borders
        for spine in self.ax_spectrum.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(2)
        
        self.ax_spectrum.axvspan(8, 13, alpha=0.1, color='yellow')
        self.ax_spectrum.axvspan(13, 30, alpha=0.1, color='cyan')
        self.line_spectrum, = self.ax_spectrum.plot([], [], color='#00ffff', linewidth=1.5)
        
    def setup_feature_blocks(self):
        """Setup 4 band power blocks"""
        # Theta
        self.ax_theta.set_facecolor('white')
        self.ax_theta.set_title('Theta (4-8Hz)', fontsize=8, color='purple', fontweight='bold')
        self.ax_theta.set_xlim(0, 1.0)
        self.ax_theta.set_xticks([])
        self.ax_theta.set_yticks([])
        for spine in self.ax_theta.spines.values():
            spine.set_edgecolor('#dddddd')
        self.bar_theta = self.ax_theta.barh([0], [0.25], color='purple', alpha=0.8, height=0.5)
        self.text_theta = self.ax_theta.text(0.5, 0, '0.25', ha='center', va='center', 
                                            color='black', fontweight='bold', fontsize=10)
        
        # Alpha
        self.ax_alpha.set_facecolor('white')
        self.ax_alpha.set_title('Alpha (8-13Hz)', fontsize=8, color='#cc9900', fontweight='bold')
        self.ax_alpha.set_xlim(0, 1.0)
        self.ax_alpha.set_xticks([])
        self.ax_alpha.set_yticks([])
        for spine in self.ax_alpha.spines.values():
            spine.set_edgecolor('#dddddd')
        self.bar_alpha = self.ax_alpha.barh([0], [0.25], color='gold', alpha=0.9, height=0.5)
        self.text_alpha = self.ax_alpha.text(0.5, 0, '0.25', ha='center', va='center', 
                                            color='black', fontweight='bold', fontsize=10)
        
        # Beta
        self.ax_beta.set_facecolor('white')
        self.ax_beta.set_title('Beta (13-30Hz)', fontsize=8, color='#0088aa', fontweight='bold')
        self.ax_beta.set_xlim(0, 1.0)
        self.ax_beta.set_xticks([])
        self.ax_beta.set_yticks([])
        for spine in self.ax_beta.spines.values():
            spine.set_edgecolor('#dddddd')
        self.bar_beta = self.ax_beta.barh([0], [0.25], color='deepskyblue', alpha=0.9, height=0.5)
        self.text_beta = self.ax_beta.text(0.5, 0, '0.25', ha='center', va='center', 
                                          color='black', fontweight='bold', fontsize=10)
        
        # Gamma
        self.ax_gamma.set_facecolor('white')
        self.ax_gamma.set_title('Gamma (30-50Hz)', fontsize=8, color='#cc3300', fontweight='bold')
        self.ax_gamma.set_xlim(0, 1.0)
        self.ax_gamma.set_xticks([])
        self.ax_gamma.set_yticks([])
        for spine in self.ax_gamma.spines.values():
            spine.set_edgecolor('#dddddd')
        self.bar_gamma = self.ax_gamma.barh([0], [0.25], color='orangered', alpha=0.9, height=0.5)
        self.text_gamma = self.ax_gamma.text(0.5, 0, '0.25', ha='center', va='center', 
                                            color='black', fontweight='bold', fontsize=10)
        
    def setup_health_panel(self):
        """Setup health predictions"""
        self.ax_health.set_facecolor('white')
        self.ax_health.axis('off')
        self.ax_health.set_title('Health Predictions', fontsize=10, color='#0066cc', fontweight='bold', loc='left')
        
        self.health_texts = {
            'visual': self.ax_health.text(0.17, 0.5, 'Visual: NORMAL', 
                                         ha='center', va='center', fontsize=10, 
                                         color='#00aa00', fontweight='bold',
                                         bbox=dict(boxstyle='round', facecolor='#f0f0f0', 
                                                  edgecolor='#00aa00', linewidth=2, alpha=0.9)),
            'motor': self.ax_health.text(0.50, 0.5, 'Motor: NORMAL', 
                                        ha='center', va='center', fontsize=10, 
                                        color='#00aa00', fontweight='bold',
                                        bbox=dict(boxstyle='round', facecolor='#f0f0f0', 
                                                 edgecolor='#00aa00', linewidth=2, alpha=0.9)),
            'attention': self.ax_health.text(0.83, 0.5, 'Attention: NORMAL', 
                                           ha='center', va='center', fontsize=10, 
                                           color='#00aa00', fontweight='bold',
                                           bbox=dict(boxstyle='round', facecolor='#f0f0f0', 
                                                    edgecolor='#00aa00', linewidth=2, alpha=0.9))
        }
    
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
            'stats': self.ax_status.text(0.5, 0.35, 'Band Powers:', 
                                         ha='center', va='top', fontsize=8, 
                                         color='#333333'),
        }
    
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
        
        # Update bands
        if len(self.alpha_power_history) > 0:
            self.bar_theta[0].set_width(self.current_theta)
            self.text_theta.set_text(f'{self.current_theta:.2f}')
            
            self.bar_alpha[0].set_width(self.current_alpha)
            self.text_alpha.set_text(f'{self.current_alpha:.2f}')
            
            self.bar_beta[0].set_width(self.current_beta)
            self.text_beta.set_text(f'{self.current_beta:.2f}')
            
            self.bar_gamma[0].set_width(self.current_gamma)
            self.text_gamma.set_text(f'{self.current_gamma:.2f}')
        
        # Update health predictions
        pred_colors = {'NORMAL': '#00aa00', 'BORDERLINE': '#cc8800', 'IMPAIRED': '#cc0000'}
        
        self.health_texts['visual'].set_text(f'Visual: {self.visual_impairment}')
        self.health_texts['visual'].set_color(pred_colors.get(self.visual_impairment, '#333333'))
        self.health_texts['visual'].get_bbox_patch().set_edgecolor(pred_colors.get(self.visual_impairment, '#999999'))
        
        self.health_texts['motor'].set_text(f'Motor: {self.motor_impairment}')
        self.health_texts['motor'].set_color(pred_colors.get(self.motor_impairment, '#333333'))
        self.health_texts['motor'].get_bbox_patch().set_edgecolor(pred_colors.get(self.motor_impairment, '#999999'))
        
        self.health_texts['attention'].set_text(f'Attention: {self.attention_deficit}')
        self.health_texts['attention'].set_color(pred_colors.get(self.attention_deficit, '#333333'))
        self.health_texts['attention'].get_bbox_patch().set_edgecolor(pred_colors.get(self.attention_deficit, '#999999'))
        
        # Update status
        self.update_status_panel()
        artists.extend(self.text_elements.values())
        
        return artists
    
    def update_status_panel(self):
        """Update status text"""
        cmd_colors = {'FOCUS': '#00aa00', 'RELAX': '#0088cc', 'BLINK': '#cc6600', 'NONE': '#666666'}
        
        self.text_elements['command'].set_text(f'Command:\n{self.current_command}')
        self.text_elements['command'].set_color(cmd_colors.get(self.current_command, '#333333'))
        
        led_text = 'LED: ON' if self.led_state else 'LED: OFF'
        self.text_elements['led'].set_text(led_text)
        self.text_elements['led'].set_color('#00aa00' if self.led_state else '#cc0000')
        
        stats_text = f'θ:{self.current_theta:.2f}\nα:{self.current_alpha:.2f}\nβ:{self.current_beta:.2f}\nγ:{self.current_gamma:.2f}'
        self.text_elements['stats'].set_text(stats_text)
        self.text_elements['stats'].set_color('#333333')
    
    def process_data(self, data):
        """Process incoming data"""
        self.time_data.append(data['time'])
        self.signal_data.append(data['amplitude'])
        
        if 'command' in data: self.current_command = data['command']
        if 'theta_power' in data: 
            self.current_theta = data['theta_power']
            self.theta_power_history.append(data['theta_power'])
        if 'alpha_power' in data: 
            self.current_alpha = data['alpha_power']
            self.alpha_power_history.append(data['alpha_power'])
        if 'beta_power' in data: 
            self.current_beta = data['beta_power']
            self.beta_power_history.append(data['beta_power'])
        if 'gamma_power' in data: 
            self.current_gamma = data['gamma_power']
            self.gamma_power_history.append(data['gamma_power'])
        if 'led_state' in data: self.led_state = data['led_state']
        if 'visual_impairment' in data: self.visual_impairment = data['visual_impairment']
        if 'motor_impairment' in data: self.motor_impairment = data['motor_impairment']
        if 'attention_deficit' in data: self.attention_deficit = data['attention_deficit']
