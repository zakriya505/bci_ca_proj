#!/usr/bin/env python3
"""
BCI All Predictions Visualizer - Clean High-End Design
Displays all three prediction datasets side-by-side for comparison
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

DATASETS = {
    'Visual': 'data/raw/visual_impairment_data.csv',
    'Motor': 'data/raw/motor_impairment_data.csv',
    'Attention': 'data/raw/attention_deficit_data.csv'
}

def load_dataset(filepath):
    if not os.path.exists(filepath):
        print(f"ERROR: Dataset not found: {filepath}")
        return None
    return pd.read_csv(filepath)

def plot_comparison():
    datasets = {}
    for name, path in DATASETS.items():
        df = load_dataset(path)
        if df is None:
            return
        datasets[name] = df
    
    # Larger figure with more margins
    fig = plt.figure(figsize=(20, 14), facecolor='white')
    
    # More top/bottom margin to prevent overlap
    gs = GridSpec(4, 3, figure=fig, 
                  height_ratios=[1.2, 1, 1, 0.8],
                  hspace=0.45, wspace=0.28,
                  left=0.06, right=0.96, 
                  top=0.90, bottom=0.08)  # More margin
    
    # Title with padding
    fig.suptitle('BCI Multi-Dataset Comparison Dashboard', 
                 fontsize=18, fontweight='bold', color='#1a1a2e', y=0.96)
    
    colors = {'Visual': '#8e44ad', 'Motor': '#2980b9', 'Attention': '#d35400'}
    prediction_cols = {'Visual': 'visual_impairment', 'Motor': 'motor_impairment', 'Attention': 'attention_deficit'}
    primary_bands = {'Visual': 'alpha_power', 'Motor': 'beta_power', 'Attention': None}
    
    for col_idx, (name, df) in enumerate(datasets.items()):
        color = colors[name]
        
        # Row 0: EEG Signal
        ax1 = fig.add_subplot(gs[0, col_idx])
        ax1.set_facecolor('#0d1117')
        ax1.plot(df['time'], df['amplitude'], color=color, linewidth=0.8, alpha=0.9)
        ax1.set_title(f'{name} Impairment Dataset', fontweight='bold', fontsize=13, 
                      color='white', pad=12, backgroundcolor=color)
        ax1.set_ylabel('Amplitude (uV)', fontsize=10, color='#333', fontweight='bold')
        ax1.set_xlim(0, 10)
        ax1.tick_params(labelsize=9, colors='#333')
        for spine in ax1.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
        ax1.grid(True, alpha=0.15, color='white')
        
        # Row 1: Primary Metric
        ax2 = fig.add_subplot(gs[1, col_idx])
        ax2.set_facecolor('#fafafa')
        if name == 'Attention':
            ratio = df['theta_power'] / df['beta_power'].replace(0, 0.01)
            ax2.fill_between(df['time'], ratio, alpha=0.3, color=color)
            ax2.plot(df['time'], ratio, color=color, linewidth=2.5)
            ax2.set_ylabel('Theta/Beta Ratio', fontsize=10, color='#333', fontweight='bold')
            ax2.axhline(y=1.5, color='#27ae60', linestyle='--', alpha=0.8, lw=2, label='Normal')
            ax2.axhline(y=2.0, color='#e74c3c', linestyle='--', alpha=0.8, lw=2, label='Impaired')
            ax2.set_ylim(0, 6)
            ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)
        else:
            band = primary_bands[name]
            ax2.fill_between(df['time'], df[band], alpha=0.3, color=color)
            ax2.plot(df['time'], df[band], color=color, linewidth=2.5)
            label = 'Alpha Power' if name == 'Visual' else 'Beta Power'
            ax2.set_ylabel(label, fontsize=10, color='#333', fontweight='bold')
            ax2.axhline(y=0.35, color='#27ae60', linestyle='--', alpha=0.8, lw=2, label='Normal')
            ax2.axhline(y=0.20, color='#e74c3c', linestyle='--', alpha=0.8, lw=2, label='Impaired')
            ax2.set_ylim(0, 1)
            ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)
        ax2.set_xlim(0, 10)
        ax2.tick_params(labelsize=9, colors='#333')
        ax2.grid(True, alpha=0.4, color='#ddd')
        for spine in ax2.spines.values():
            spine.set_edgecolor('#ccc')
        
        # Row 2: All Band Powers
        ax3 = fig.add_subplot(gs[2, col_idx])
        ax3.set_facecolor('#fafafa')
        ax3.plot(df['time'], df['theta_power'], label='Theta (4-8Hz)', linewidth=2, color='#9b59b6')
        ax3.plot(df['time'], df['alpha_power'], label='Alpha (8-13Hz)', linewidth=2, color='#f39c12')
        ax3.plot(df['time'], df['beta_power'], label='Beta (13-30Hz)', linewidth=2, color='#3498db')
        ax3.plot(df['time'], df['gamma_power'], label='Gamma (30-50Hz)', linewidth=2, color='#e74c3c')
        ax3.set_ylabel('Band Power', fontsize=10, color='#333', fontweight='bold')
        ax3.set_xlabel('Time (seconds)', fontsize=10, color='#333')
        ax3.legend(fontsize=8, ncol=2, loc='upper center', framealpha=0.9, 
                   bbox_to_anchor=(0.5, 1.0))
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 1)
        ax3.tick_params(labelsize=9, colors='#333')
        ax3.grid(True, alpha=0.4, color='#ddd')
        for spine in ax3.spines.values():
            spine.set_edgecolor('#ccc')
        
        # Row 3: Prediction Timeline
        ax4 = fig.add_subplot(gs[3, col_idx])
        ax4.set_facecolor('#fafafa')
        pred_col = prediction_cols[name]
        pred_map = {'NORMAL': 0, 'BORDERLINE': 1, 'IMPAIRED': 2}
        pred_values = df[pred_col].map(pred_map)
        
        time = df['time'].values
        pred_colors = {0: '#27ae60', 1: '#f39c12', 2: '#e74c3c'}
        for i in range(len(time) - 1):
            ax4.axvspan(time[i], time[i+1], facecolor=pred_colors[pred_values.iloc[i]], alpha=0.85)
        
        ax4.set_ylabel(f'{name}', fontsize=10, color='#333', fontweight='bold')
        ax4.set_xlabel('Time (s)', fontsize=10, color='#333')
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 1)
        ax4.set_yticks([0.25, 0.5, 0.75])
        ax4.set_yticklabels(['NORMAL', 'BORDER', 'IMPAIR'], fontsize=8, fontweight='bold')
        ax4.tick_params(labelsize=9, colors='#333')
        for spine in ax4.spines.values():
            spine.set_edgecolor('#999')
            spine.set_linewidth(1.5)
    
    # Footer with better positioning
    fig.text(0.5, 0.02, 
             'Visual = Alpha Band Focus  |  Motor = Beta Band Focus  |  Attention = Theta/Beta Ratio Focus', 
             ha='center', fontsize=11, fontweight='bold', color='#555',
             bbox=dict(boxstyle='round', facecolor='#f0f0f0', edgecolor='#ccc', alpha=0.8))
    
    plt.show()

def main():
    print("=" * 70)
    print("  BCI Multi-Dataset Comparison Visualization")
    print("=" * 70)
    print("\nLoading all three specialized datasets...")
    print("  - Visual Impairment (Alpha Power Focus)")
    print("  - Motor Impairment (Beta Power Focus)")
    print("  - Attention Deficit (Theta/Beta Ratio Focus)")
    print("")
    
    plot_comparison()

if __name__ == "__main__":
    main()
