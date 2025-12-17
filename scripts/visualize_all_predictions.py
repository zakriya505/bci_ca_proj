#!/usr/bin/env python3
"""
BCI All Predictions Visualizer
Displays all three prediction datasets side-by-side for comparison

This shows how each specialized dataset affects its corresponding prediction.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Dataset paths
DATASETS = {
    'Visual': 'data/raw/visual_impairment_data.csv',
    'Motor': 'data/raw/motor_impairment_data.csv',
    'Attention': 'data/raw/attention_deficit_data.csv'
}

def load_dataset(filepath):
    """Load a dataset from CSV"""
    if not os.path.exists(filepath):
        print(f"ERROR: Dataset not found: {filepath}")
        print("Run: python scripts/generate_separate_datasets.py")
        return None
    return pd.read_csv(filepath)

def plot_comparison():
    """Create comparison visualization of all three datasets"""
    
    # Load all datasets
    datasets = {}
    for name, path in DATASETS.items():
        df = load_dataset(path)
        if df is None:
            return
        datasets[name] = df
    
    # Create figure
    fig = plt.figure(figsize=(16, 10), facecolor='white')
    fig.suptitle('BCI Multi-Dataset Comparison - Each Dataset Specializes in One Prediction', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.3,
                  left=0.06, right=0.96, top=0.92, bottom=0.08)
    
    # Color schemes
    colors = {
        'Visual': '#9c27b0',    # Purple
        'Motor': '#2196f3',     # Blue
        'Attention': '#ff9800'  # Orange
    }
    
    prediction_cols = {
        'Visual': 'visual_impairment',
        'Motor': 'motor_impairment',
        'Attention': 'attention_deficit'
    }
    
    primary_bands = {
        'Visual': 'alpha_power',
        'Motor': 'beta_power',
        'Attention': None  # theta/beta ratio
    }
    
    # Plot each dataset
    for col_idx, (name, df) in enumerate(datasets.items()):
        color = colors[name]
        
        # Row 1: EEG Signal
        ax1 = fig.add_subplot(gs[0, col_idx])
        ax1.plot(df['time'], df['amplitude'], color=color, linewidth=0.5, alpha=0.7)
        ax1.set_title(f'{name} Impairment Dataset', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Amplitude (µV)', fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 10)
        
        # Row 2: Primary Band Power / Ratio
        ax2 = fig.add_subplot(gs[1, col_idx])
        if name == 'Attention':
            # Plot theta/beta ratio
            ratio = df['theta_power'] / df['beta_power']
            ax2.plot(df['time'], ratio, color=color, linewidth=2)
            ax2.set_ylabel('Theta/Beta Ratio', fontsize=9, fontweight='bold')
            ax2.axhline(y=1.5, color='green', linestyle='--', alpha=0.5, label='Normal')
            ax2.axhline(y=2.0, color='orange', linestyle='--', alpha=0.5, label='Borderline')
            ax2.legend(fontsize=7, loc='upper right')
        else:
            band = primary_bands[name]
            ax2.plot(df['time'], df[band], color=color, linewidth=2)
            band_label = band.replace('_power', '').capitalize()
            ax2.set_ylabel(f'{band_label} Power', fontsize=9, fontweight='bold')
            
            # Add threshold lines
            if name == 'Visual':
                ax2.axhline(y=0.35, color='green', linestyle='--', alpha=0.5, label='Normal')
                ax2.axhline(y=0.25, color='orange', linestyle='--', alpha=0.5, label='Borderline')
            else:  # Motor
                ax2.axhline(y=0.30, color='green', linestyle='--', alpha=0.5, label='Normal')
                ax2.axhline(y=0.20, color='orange', linestyle='--', alpha=0.5, label='Borderline')
            ax2.legend(fontsize=7, loc='upper right')
        
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 10)
        ax2.set_ylim(bottom=0)
        
        # Row 3: All Band Powers
        ax3 = fig.add_subplot(gs[2, col_idx])
        ax3.plot(df['time'], df['theta_power'], label='Theta', alpha=0.7, linewidth=1.5)
        ax3.plot(df['time'], df['alpha_power'], label='Alpha', alpha=0.7, linewidth=1.5)
        ax3.plot(df['time'], df['beta_power'], label='Beta', alpha=0.7, linewidth=1.5)
        ax3.plot(df['time'], df['gamma_power'], label='Gamma', alpha=0.7, linewidth=1.5)
        ax3.set_ylabel('Band Powers', fontsize=9)
        ax3.set_xlabel('Time (s)', fontsize=9)
        ax3.legend(fontsize=7, ncol=2)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 1)
        
        # Row 4: Prediction Timeline
        ax4 = fig.add_subplot(gs[3, col_idx])
        pred_col = prediction_cols[name]
        
        # Map predictions to numeric values for plotting
        pred_map = {'NORMAL': 0, 'BORDERLINE': 1, 'IMPAIRED': 2}
        pred_values = df[pred_col].map(pred_map)
        
        # Create color-coded background
        time = df['time'].values
        for i in range(len(time) - 1):
            pred_val = pred_values.iloc[i]
            if pred_val == 0:  # Normal
                bar_color = '#4caf50'
            elif pred_val == 1:  # Borderline
                bar_color = '#ff9800'
            else:  # Impaired
                bar_color = '#f44336'
            
            ax4.axvspan(time[i], time[i+1], facecolor=bar_color, alpha=0.7)
        
        ax4.set_ylabel(f'{name} Status', fontsize=9, fontweight='bold')
        ax4.set_xlabel('Time (s)', fontsize=9)
        ax4.set_xlim(0, 10)
        ax4.set_ylim(-0.5, 2.5)
        ax4.set_yticks([0, 1, 2])
        ax4.set_yticklabels(['NORMAL', 'BORDERLINE', 'IMPAIRED'], fontsize=8)
        ax4.grid(True, alpha=0.3, axis='x')
    
    # Add footer info
    info_text = 'Each dataset is optimized to demonstrate its specific prediction type | ' \
                'Visual focuses on Alpha | Motor focuses on Beta | Attention focuses on Theta/Beta ratio'
    fig.text(0.5, 0.02, info_text, ha='center', va='bottom', 
             fontsize=9, style='italic', color='#666666')
    
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
