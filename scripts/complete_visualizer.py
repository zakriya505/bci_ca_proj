#!/usr/bin/env python3
"""
BCI Complete Visualizer - Clean High-End Dashboard
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from scipy.fft import fft, fftfreq
import queue
import time
from collections import deque
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

class RISCVSimulator:
    def __init__(self):
        self.reset()
        self.c_baseline_cycles = 0
        self.asm_optimized_cycles = 0
        
    def reset(self):
        self.total_instructions = 0
        self.total_cycles = 0
        self.instruction_breakdown = {'ALU': 0, 'Mem': 0, 'Branch': 0, 'FPU': 0, 'Custom': 0}
        self.cache_hits = 0
        self.cache_misses = 0
        self.pipeline_stalls = 0
        self.branch_predictions = 0
        self.branch_mispredictions = 0
        
    def simulate_fft_processing(self, window_size=256):
        n = window_size
        log_n = int(np.log2(n))
        butterflies = (n // 2) * log_n
        
        self.c_baseline_cycles = butterflies * 20
        self.asm_optimized_cycles = butterflies * 8
        
        self.instruction_breakdown['ALU'] += butterflies * 2
        self.instruction_breakdown['Mem'] += butterflies
        self.instruction_breakdown['FPU'] += butterflies * 2
        self.instruction_breakdown['Custom'] += butterflies
        self.instruction_breakdown['Branch'] += log_n * 2
        
        self.total_instructions += butterflies * 6 + log_n * 2
        self.total_cycles += self.asm_optimized_cycles
        
        # Shared correlation factor (-1.0 to 1.0) to make metrics move in sync
        correlation_factor = np.random.uniform(-1, 1)
        
        # Dynamic Cache Simulation (80-85% range)
        cache_hit_rate = 0.825 + (correlation_factor * 0.025)
        self.cache_hits += int(butterflies * cache_hit_rate)
        self.cache_misses += int(butterflies * (1 - cache_hit_rate))
        
        # Dynamic Stall Simulation (linked to cache misses)
        stall_rate = 0.03 + (1 - cache_hit_rate) * 0.2
        self.pipeline_stalls += int(butterflies * stall_rate)
        
        # Dynamic Branch Simulation (90-97% range)
        branch_acc = 0.935 + (correlation_factor * 0.035)
        # Scale up branch count for more realistic percentage display in mock
        pseudo_branches = log_n * 10
        self.branch_predictions += int(pseudo_branches * branch_acc)
        self.branch_mispredictions += max(1, int(pseudo_branches * (1 - branch_acc)))
        
    def get_ipc(self):
        return self.total_instructions / max(1, self.total_cycles)
    
    def get_speedup(self):
        return self.c_baseline_cycles / max(1, self.asm_optimized_cycles)
    
    def get_cache_hit_rate(self):
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / max(1, total) * 100
    
    def get_branch_accuracy(self):
        total = self.branch_predictions + self.branch_mispredictions
        return self.branch_predictions / max(1, total) * 100


class CompleteBCIVisualizer:
    def __init__(self, dataset_path=None, dataset_type="General"):
        self.sampling_rate = 256
        self.window_size = 256
        self.display_seconds = 3
        self.update_interval = 50
        self.dataset_type = dataset_type
        
        self.max_points = int(self.sampling_rate * self.display_seconds)
        self.time_data = deque(maxlen=self.max_points)
        self.signal_data = deque(maxlen=self.max_points)
        
        self.current_command = "NONE"
        self.current_theta = 0.25
        self.current_alpha = 0.25
        self.current_beta = 0.25
        self.current_gamma = 0.25
        self.led_state = False
        
        self.visual_impairment = "NORMAL"
        self.motor_impairment = "NORMAL"
        self.attention_deficit = "NORMAL"
        
        self.riscv = RISCVSimulator()
        self.data_queue = queue.Queue()
        self.cycles_history = deque(maxlen=50)
        
        self.setup_figure()
        
    def setup_figure(self):
        plt.style.use('default')
        self.fig = plt.figure(figsize=(22, 14), facecolor='white')
        self.fig.canvas.manager.set_window_title(f'BCI RISC-V Dashboard - {self.dataset_type}')
        
        # 4x4 grid with MUCH more spacing
        gs = GridSpec(4, 4, figure=self.fig, 
                     height_ratios=[1.2, 1, 1, 1],
                     hspace=0.55,  # More vertical space
                     wspace=0.4,   # More horizontal space
                     left=0.06, right=0.96, 
                     top=0.88,     # More top margin
                     bottom=0.06)
        
        # Title - positioned higher
        self.fig.suptitle('BCI RISC-V Signal Processing Dashboard', 
                         fontsize=16, fontweight='bold', color='#1a1a2e', y=0.96)
        
        # Row 0: EEG Waveform (full width)
        self.ax_wave = self.fig.add_subplot(gs[0, :])
        self.setup_waveform()
        
        # Row 1
        self.ax_spectrum = self.fig.add_subplot(gs[1, 0])
        self.ax_bands = self.fig.add_subplot(gs[1, 1])
        self.ax_health = self.fig.add_subplot(gs[1, 2:4]) # Expanded Health panel
        self.setup_row1()
        
        # Row 2
        self.ax_pie = self.fig.add_subplot(gs[2, 0])
        self.ax_bench = self.fig.add_subplot(gs[2, 1])
        self.ax_metrics = self.fig.add_subplot(gs[2, 2])
        self.ax_pipeline = self.fig.add_subplot(gs[2, 3])
        self.setup_row2()
        
        # Row 3
        self.ax_perf = self.fig.add_subplot(gs[3, 0:2])
        self.ax_cache = self.fig.add_subplot(gs[3, 2:4])
        self.setup_row3()
        
    def setup_waveform(self):
        self.ax_wave.set_facecolor('#0d1117')
        self.ax_wave.set_title('EEG Signal', fontsize=11, color='#00ff41', fontweight='bold', pad=5)
        self.ax_wave.set_xlabel('Time (s)', color='#333', fontsize=9)
        self.ax_wave.set_ylabel('Amplitude', color='#333', fontsize=9)
        self.ax_wave.grid(True, alpha=0.2, color='#00ff41')
        self.ax_wave.tick_params(colors='#333', labelsize=8)
        for spine in self.ax_wave.spines.values():
            spine.set_edgecolor('#00ff41')
            spine.set_linewidth(1.5)
        self.line_wave, = self.ax_wave.plot([], [], color='#00ff41', linewidth=1)
        self.ax_wave.set_xlim(0, self.display_seconds)
        self.ax_wave.set_ylim(-10, 10)
        
    def setup_row1(self):
        # Spectrum - NO xlabel to avoid overlap
        self.ax_spectrum.set_facecolor('#0d1117')
        self.ax_spectrum.set_title('Spectrum', fontsize=10, color='#00d4ff', fontweight='bold', pad=5)
        self.ax_spectrum.set_xlim(0, 50)
        self.ax_spectrum.set_ylim(0, 500)
        self.ax_spectrum.tick_params(colors='#333', labelsize=7)
        for spine in self.ax_spectrum.spines.values():
            spine.set_edgecolor('#00d4ff')
        self.line_spec, = self.ax_spectrum.plot([], [], color='#00d4ff', linewidth=1)
        
        # Bands - NO xlabel
        self.ax_bands.set_facecolor('#fafafa')
        self.ax_bands.set_title('Bands', fontsize=10, fontweight='bold', pad=5)
        self.bars = self.ax_bands.bar(['T', 'A', 'B', 'G'], [0.25]*4,
                                      color=['#9b59b6', '#f1c40f', '#3498db', '#e74c3c'])
        self.ax_bands.set_ylim(0, 1)
        self.ax_bands.tick_params(labelsize=8)
        
        # Health
        self.ax_health.set_facecolor('#f0f4f8')
        self.ax_health.axis('off')
        self.ax_health.set_title('Health Predictions', fontsize=10, fontweight='bold', color='#2980b9', pad=5)
        self.health_txt = {
            'v': self.ax_health.text(0.5, 0.72, 'Visual: NORMAL', ha='center', fontsize=10, color='#27ae60', fontweight='bold'),
            'm': self.ax_health.text(0.5, 0.42, 'Motor: NORMAL', ha='center', fontsize=10, color='#27ae60', fontweight='bold'),
            'a': self.ax_health.text(0.5, 0.12, 'Attn: NORMAL', ha='center', fontsize=10, color='#27ae60', fontweight='bold')
        }
        
    def setup_row2(self):
        # Pie
        self.ax_pie.set_facecolor('white')
        self.ax_pie.set_title('Instructions', fontsize=10, fontweight='bold', pad=5)
        
        # Benchmark
        self.ax_bench.set_facecolor('#fafafa')
        self.ax_bench.set_title('C vs ASM', fontsize=10, fontweight='bold', pad=5)
        self.bench_bars = self.ax_bench.bar(['C', 'ASM'], [0, 0], color=['#e74c3c', '#27ae60'])
        self.ax_bench.tick_params(labelsize=8)
        self.speed_txt = self.ax_bench.text(0.5, 0.88, '1.0x', transform=self.ax_bench.transAxes,
                                            ha='center', fontsize=11, fontweight='bold')
        
        # Metrics
        self.ax_metrics.set_facecolor('#1a1a2e')
        self.ax_metrics.axis('off')
        self.ax_metrics.set_title('Metrics', fontsize=10, fontweight='bold', color='#333', pad=5)
        self.metric_txt = {
            'inst': self.ax_metrics.text(0.08, 0.78, 'Instr: 0', fontsize=10, color='#2ecc71', family='monospace', fontweight='bold'),
            'cyc': self.ax_metrics.text(0.08, 0.54, 'Cycles: 0', fontsize=10, color='#3498db', family='monospace', fontweight='bold'),
            'ipc': self.ax_metrics.text(0.08, 0.30, 'IPC: 0', fontsize=10, color='#f1c40f', family='monospace', fontweight='bold'),
            'stall': self.ax_metrics.text(0.08, 0.06, 'Stalls: 0', fontsize=10, color='#e67e22', family='monospace', fontweight='bold')
        }
        
        # Pipeline
        self.ax_pipeline.set_facecolor('#1a1a2e')
        self.ax_pipeline.axis('off')
        self.ax_pipeline.set_title('Pipeline', fontsize=10, fontweight='bold', color='#333', pad=5)
        stages = ['IF', 'ID', 'EX', 'ME', 'WB']
        colors = ['#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#27ae60']
        for i, (s, c) in enumerate(zip(stages, colors)):
            x = 0.05 + i * 0.19
            self.ax_pipeline.add_patch(plt.Rectangle((x, 0.3), 0.15, 0.5, fc=c, ec='white', lw=2))
            self.ax_pipeline.text(x + 0.075, 0.55, s, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        self.stall_txt = self.ax_pipeline.text(0.5, 0.08, 'Stalls: 0', ha='center', fontsize=9, color='#bdc3c7')
        
    def setup_row3(self):
        # Performance graph
        self.ax_perf.set_facecolor('#0d1117')
        self.ax_perf.set_title('Cycles Over Time', fontsize=10, fontweight='bold', color='#e74c3c', pad=5)
        self.ax_perf.set_xlabel('Samples', fontsize=9, color='#333')
        self.ax_perf.tick_params(colors='#333', labelsize=8)
        self.line_perf, = self.ax_perf.plot([], [], color='#e74c3c', linewidth=2)
        self.ax_perf.set_xlim(0, 50)
        self.ax_perf.set_ylim(0, 15000)
        self.ax_perf.grid(True, alpha=0.2, color='#e74c3c')
        for spine in self.ax_perf.spines.values():
            spine.set_edgecolor('#e74c3c')
        
        # Cache & Branch
        self.ax_cache.set_facecolor('#fafafa')
        self.ax_cache.set_title('Cache & Branch %', fontsize=10, fontweight='bold', pad=5)
        self.cache_bars = self.ax_cache.bar(['Cache', 'Branch'], [0, 0], color=['#27ae60', '#3498db'])
        self.ax_cache.set_ylim(0, 100)
        self.ax_cache.tick_params(labelsize=8)
        self.cache_txt = self.ax_cache.text(0, 10, '0%', ha='center', fontsize=10, fontweight='bold', color='white')
        self.branch_txt = self.ax_cache.text(1, 10, '0%', ha='center', fontsize=10, fontweight='bold', color='white')
        
    def compute_fft(self, data):
        if len(data) < self.window_size:
            return None, None
        arr = np.array(data)[-self.window_size:]
        yf = np.abs(fft(arr))
        xf = fftfreq(self.window_size, 1/self.sampling_rate)
        mask = (xf >= 0) & (xf <= 50)
        return xf[mask], yf[mask]
        
    def update_plot(self, frame):
        for _ in range(min(50, self.data_queue.qsize())):
            try:
                data = self.data_queue.get_nowait()
                self.process_data(data)
            except:
                break
                
        if frame % 5 == 0:
            self.riscv.simulate_fft_processing()
            self.cycles_history.append(self.riscv.total_cycles % 15000)
        
        if len(self.time_data) > 0:
            t, y = list(self.time_data), list(self.signal_data)
            if t[-1] > self.ax_wave.get_xlim()[1]:
                self.ax_wave.set_xlim(t[-1] - self.display_seconds, t[-1])
            if frame % 10 == 0 and len(y) > 0:
                ymin, ymax = min(y), max(y)
                pad = max(10, (ymax - ymin) * 0.1)
                self.ax_wave.set_ylim(ymin - pad, ymax + pad)
            self.line_wave.set_data(t, y)
            
        if frame % 5 == 0 and len(self.signal_data) >= self.window_size:
            xf, yf = self.compute_fft(self.signal_data)
            if xf is not None:
                self.line_spec.set_data(xf, yf)
                
        for bar, val in zip(self.bars, [self.current_theta, self.current_alpha, self.current_beta, self.current_gamma]):
            bar.set_height(val)
            
        # Update health prediction text
        colors = {'NORMAL': '#27ae60', 'BORDERLINE': '#f39c12', 'IMPAIRED': '#c0392b'}
        self.health_txt['v'].set_text(f'Visual: {self.visual_impairment}')
        self.health_txt['v'].set_color(colors.get(self.visual_impairment, '#333'))
        self.health_txt['m'].set_text(f'Motor: {self.motor_impairment}')
        self.health_txt['m'].set_color(colors.get(self.motor_impairment, '#333'))
        self.health_txt['a'].set_text(f'Attn: {self.attention_deficit}')
        self.health_txt['a'].set_color(colors.get(self.attention_deficit, '#333'))
        
        if frame % 20 == 0:
            self.ax_pie.clear()
            self.ax_pie.set_title('Instructions', fontsize=10, fontweight='bold', pad=5)
            bd = self.riscv.instruction_breakdown
            if sum(bd.values()) > 0:
                self.ax_pie.pie(bd.values(), labels=bd.keys(), autopct='%1.0f%%',
                               colors=['#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#27ae60'],
                               textprops={'fontsize': 8})
                               
        c, a = self.riscv.c_baseline_cycles, self.riscv.asm_optimized_cycles
        self.bench_bars[0].set_height(c)
        self.bench_bars[1].set_height(a)
        self.ax_bench.set_ylim(0, max(c, a, 100) * 1.2)
        self.speed_txt.set_text(f'{self.riscv.get_speedup():.1f}x')
        
        self.metric_txt['inst'].set_text(f'Instr: {self.riscv.total_instructions:,}')
        self.metric_txt['cyc'].set_text(f'Cycles: {self.riscv.total_cycles:,}')
        self.metric_txt['ipc'].set_text(f'IPC: {self.riscv.get_ipc():.2f}')
        self.metric_txt['stall'].set_text(f'Stalls: {self.riscv.pipeline_stalls:,}')
        
        self.stall_txt.set_text(f'Stalls: {self.riscv.pipeline_stalls:,}')
        
        if len(self.cycles_history) > 0:
            self.line_perf.set_data(range(len(self.cycles_history)), list(self.cycles_history))
            
        cache_rate = self.riscv.get_cache_hit_rate()
        branch_acc = self.riscv.get_branch_accuracy()
        self.cache_bars[0].set_height(cache_rate)
        self.cache_bars[1].set_height(branch_acc)
        self.cache_txt.set_position((0, cache_rate / 2))
        self.cache_txt.set_text(f'{cache_rate:.0f}%')
        self.branch_txt.set_position((1, branch_acc / 2))
        self.branch_txt.set_text(f'{branch_acc:.0f}%')
        
        return []
        
    def process_data(self, data):
        self.time_data.append(data['time'])
        self.signal_data.append(data['amplitude'])
        if 'command' in data: self.current_command = data['command']
        if 'theta_power' in data: self.current_theta = data['theta_power']
        if 'alpha_power' in data: self.current_alpha = data['alpha_power']
        if 'beta_power' in data: self.current_beta = data['beta_power']
        if 'gamma_power' in data: self.current_gamma = data['gamma_power']
        if 'led_state' in data: self.led_state = data['led_state']
        if 'visual_impairment' in data: self.visual_impairment = data['visual_impairment']
        if 'motor_impairment' in data: self.motor_impairment = data['motor_impairment']
        if 'attention_deficit' in data: self.attention_deficit = data['attention_deficit']


def load_and_visualize(filepath, dataset_type):
    import pandas as pd
    
    print(f"Loading: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"ERROR: File not found")
        return
        
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} samples")
    
    vis = CompleteBCIVisualizer(filepath, dataset_type)
    
    def feed_data():
        for _, row in df.iterrows():
            led_on = (row.get('visual_impairment', 'NORMAL') != 'NORMAL' or
                     row.get('motor_impairment', 'NORMAL') != 'NORMAL' or
                     row.get('attention_deficit', 'NORMAL') != 'NORMAL')
            
            vis.data_queue.put({
                'time': row['time'],
                'amplitude': row['amplitude'],
                'command': row.get('command', 'NONE'),
                'theta_power': row.get('theta_power', 0.25),
                'alpha_power': row.get('alpha_power', 0.25),
                'beta_power': row.get('beta_power', 0.25),
                'gamma_power': row.get('gamma_power', 0.25),
                'led_state': led_on,
                'visual_impairment': row.get('visual_impairment', 'NORMAL'),
                'motor_impairment': row.get('motor_impairment', 'NORMAL'),
                'attention_deficit': row.get('attention_deficit', 'NORMAL')
            })
            time.sleep(0.008)
        print("Done!")
    
    threading.Thread(target=feed_data, daemon=True).start()
    
    anim = animation.FuncAnimation(vis.fig, vis.update_plot, interval=vis.update_interval, blit=False, cache_frame_data=False)
    plt.show()


if __name__ == "__main__":
    project_dir = os.path.dirname(script_dir)
    default_file = os.path.join(project_dir, "data", "raw", "sample_eeg_data.csv")
    
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_file
        
    dataset_type = "General"
    if "visual" in filepath.lower():
        dataset_type = "Visual"
    elif "motor" in filepath.lower():
        dataset_type = "Motor"
    elif "attention" in filepath.lower():
        dataset_type = "Attention"
        
    load_and_visualize(filepath, dataset_type)
