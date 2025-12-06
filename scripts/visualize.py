#!/usr/bin/env python3
"""
EEG Signal Visualization Tool
Generates plots of simulated EEG signals for analysis
"""

import numpy as np
import matplotlib.pyplot as plt

# Configuration
SAMPLING_RATE = 256  # Hz
DURATION = 2.0  # seconds
ALPHA_FREQ = 10.5  # Hz (middle of alpha band)
BETA_FREQ = 21.5  # Hz (middle of beta band)

def generate_alpha_wave(t, amplitude=50.0):
    """Generate alpha wave (8-13 Hz)"""
    return amplitude * np.sin(2 * np.pi * ALPHA_FREQ * t)

def generate_beta_wave(t, amplitude=30.0):
    """Generate beta wave (13-30 Hz)"""
    return amplitude * np.sin(2 * np.pi * BETA_FREQ * t)

def generate_blink(t, blink_time=0.5, amplitude=200.0):
    """Generate blink artifact"""
    sigma = 0.05
    return amplitude * np.exp(-((t - blink_time)**2) / (2 * sigma**2))

def add_noise(signal, noise_level=5.0):
    """Add Gaussian noise"""
    return signal + np.random.normal(0, noise_level, len(signal))

def plot_signals():
    """Generate and plot all signal types"""
    t = np.linspace(0, DURATION, int(SAMPLING_RATE * DURATION))
    
    # Create figure with subplots
    fig, axes = plt.subplots(4, 1, figsize=(12, 10))
    fig.suptitle('RISC-V BCI System - EEG Signal Simulation', fontsize=16, fontweight='bold')
    
    # 1. Focus signal (high beta)
    focus_signal = generate_beta_wave(t, 1.0) + generate_alpha_wave(t, 0.3)
    focus_signal = add_noise(focus_signal)
    axes[0].plot(t, focus_signal, 'b-', linewidth=0.8)
    axes[0].set_title('FOCUS Command - High Beta Activity', fontweight='bold')
    axes[0].set_ylabel('Amplitude (µV)')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim([0, DURATION])
    
    # 2. Relax signal (high alpha)
    relax_signal = generate_alpha_wave(t, 1.0) + generate_beta_wave(t, 0.3)
    relax_signal = add_noise(relax_signal)
    axes[1].plot(t, relax_signal, 'g-', linewidth=0.8)
    axes[1].set_title('RELAX Command - High Alpha Activity', fontweight='bold')
    axes[1].set_ylabel('Amplitude (µV)')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim([0, DURATION])
    
    # 3. Blink signal
    blink_signal = generate_alpha_wave(t, 0.5) + generate_beta_wave(t, 0.5)
    blink_signal += generate_blink(t, 0.5)
    blink_signal = add_noise(blink_signal)
    axes[2].plot(t, blink_signal, 'r-', linewidth=0.8)
    axes[2].set_title('BLINK Command - Sharp Artifact Spike', fontweight='bold')
    axes[2].set_ylabel('Amplitude (µV)')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim([0, DURATION])
    
    # 4. Baseline (balanced)
    baseline_signal = generate_alpha_wave(t, 0.5) + generate_beta_wave(t, 0.5)
    baseline_signal = add_noise(baseline_signal)
    axes[3].plot(t, baseline_signal, 'gray', linewidth=0.8)
    axes[3].set_title('Baseline - Balanced Activity', fontweight='bold')
    axes[3].set_ylabel('Amplitude (µV)')
    axes[3].set_xlabel('Time (seconds)')
    axes[3].grid(True, alpha=0.3)
    axes[3].set_xlim([0, DURATION])
    
    plt.tight_layout()
    plt.savefig('eeg_signals.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: eeg_signals.png")
    plt.show()

def plot_frequency_spectrum():
    """Plot frequency spectrum of signals"""
    t = np.linspace(0, 2.0, int(SAMPLING_RATE * 2.0))
    
    # Generate signals
    focus = generate_beta_wave(t, 1.0) + generate_alpha_wave(t, 0.3)
    relax = generate_alpha_wave(t, 1.0) + generate_beta_wave(t, 0.3)
    
    # Compute FFT
    focus_fft = np.abs(np.fft.fft(focus))
    relax_fft = np.abs(np.fft.fft(relax))
    freqs = np.fft.fftfreq(len(t), 1/SAMPLING_RATE)
    
    # Plot only positive frequencies up to 50 Hz
    mask = (freqs >= 0) & (freqs <= 50)
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle('Frequency Spectrum Analysis', fontsize=16, fontweight='bold')
    
    # Focus spectrum
    axes[0].plot(freqs[mask], focus_fft[mask], 'b-', linewidth=1.5)
    axes[0].axvspan(8, 13, alpha=0.2, color='green', label='Alpha Band (8-13 Hz)')
    axes[0].axvspan(13, 30, alpha=0.2, color='blue', label='Beta Band (13-30 Hz)')
    axes[0].set_title('FOCUS - Beta Dominant', fontweight='bold')
    axes[0].set_ylabel('Magnitude')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Relax spectrum
    axes[1].plot(freqs[mask], relax_fft[mask], 'g-', linewidth=1.5)
    axes[1].axvspan(8, 13, alpha=0.2, color='green', label='Alpha Band (8-13 Hz)')
    axes[1].axvspan(13, 30, alpha=0.2, color='blue', label='Beta Band (13-30 Hz)')
    axes[1].set_title('RELAX - Alpha Dominant', fontweight='bold')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Magnitude')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('frequency_spectrum.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: frequency_spectrum.png")
    plt.show()

if __name__ == "__main__":
    print("EEG Signal Visualization Tool")
    print("=" * 50)
    print("Generating signal plots...")
    
    plot_signals()
    plot_frequency_spectrum()
    
    print("\n✓ All visualizations complete!")
