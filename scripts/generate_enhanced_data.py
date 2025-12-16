#!/usr/bin/env python3
"""
Generate Enhanced EEG Sample Data
Creates realistic EEG data with multiple frequency bands and health predictions

Generates:
- 4 frequency bands: Theta (4-8Hz), Alpha (8-13Hz), Beta (13-30Hz), Gamma (30-50Hz)
- Mental commands: NONE, FOCUS, RELAX, BLINK
- Health predictions: Visual, Motor, Attention impairments
"""

import numpy as np
import pandas as pd
import os

# Configuration
SAMPLING_RATE = 256  # Hz
DURATION = 10  # seconds
NUM_SAMPLES = SAMPLING_RATE * DURATION

# Frequency bands (Hz)
THETA_FREQ = 6.0
ALPHA_FREQ = 10.0
BETA_FREQ = 20.0
GAMMA_FREQ = 40.0

def generate_band_signal(freq, amplitude, duration, phase=0):
    """Generate a sinusoidal signal for a specific frequency band"""
    t = np.arange(0, duration, 1/SAMPLING_RATE)
    return amplitude * np.sin(2 * np.pi * freq * t + phase)

def add_noise(signal, noise_level=5.0):
    """Add realistic noise to signal"""
    return signal + np.random.normal(0, noise_level, len(signal))

def generate_eeg_data():
    """Generate complete EEG dataset with all scenarios"""
    
    t = np.arange(0, DURATION, 1/SAMPLING_RATE)
    data = []
    
    for i, time in enumerate(t):
        # Determine current scenario based on time
        if time < 2.0:
            # Normal baseline state
            scenario = "normal"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 15, 50, 30, 10
            command = "NONE"
        elif time < 4.0:
            # FOCUS state (high beta)
            scenario = "focus"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 10, 20, 60, 15
            command = "FOCUS"
        elif time < 6.0:
            # RELAX state (high alpha)
            scenario = "relax"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 15, 65, 20, 8
            command = "RELAX"
        elif time < 7.0:
            # Visual impairment scenario (low alpha)
            scenario = "visual_impaired"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 25, 15, 35, 12
            command = "NONE"
        elif time < 8.0:
            # Motor impairment scenario (low beta)
            scenario = "motor_impaired"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 20, 45, 10, 15
            command = "NONE"
        elif time < 9.0:
            # Attention deficit scenario (high theta, low beta)
            scenario = "attention_deficit"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 50, 25, 15, 8
            command = "NONE"
        else:
            # Mixed scenario
            scenario = "mixed"
            theta_amp, alpha_amp, beta_amp, gamma_amp = 20, 35, 30, 12
            command = "NONE"
        
        # Generate composite signal
        theta_signal = generate_band_signal(THETA_FREQ, theta_amp, 1/SAMPLING_RATE, i*0.1)
        alpha_signal = generate_band_signal(ALPHA_FREQ, alpha_amp, 1/SAMPLING_RATE, i*0.15)
        beta_signal = generate_band_signal(BETA_FREQ, beta_amp, 1/SAMPLING_RATE, i*0.2)
        gamma_signal = generate_band_signal(GAMMA_FREQ, gamma_amp, 1/SAMPLING_RATE, i*0.3)
        
        # Composite amplitude
        amplitude = theta_signal + alpha_signal + beta_signal + gamma_signal
        
        # Add noise
        amplitude = add_noise(np.array([amplitude]), noise_level=5.0)[0]
        amplitude = float(amplitude)  # Convert from numpy to python float
        
        # Add occasional blink artifacts
        if i % 512 == 0 and i > 0:
            amplitude += 150 * np.random.random()
            command = "BLINK"
        
        # Calculate normalized band powers
        total_power = theta_amp + alpha_amp + beta_amp + gamma_amp
        theta_power = theta_amp / total_power
        alpha_power = alpha_amp / total_power
        beta_power = beta_amp / total_power
        gamma_power = gamma_amp / total_power
        
        # Predict health impairments
        # Visual: based on alpha power
        if alpha_power >= 0.35:
            visual_impairment = "NORMAL"
        elif alpha_power >= 0.25:
            visual_impairment = "BORDERLINE"
        else:
            visual_impairment = "IMPAIRED"
        
        # Motor: based on beta power
        if beta_power >= 0.30:
            motor_impairment = "NORMAL"
        elif beta_power >= 0.20:
            motor_impairment = "BORDERLINE"
        else:
            motor_impairment = "IMPAIRED"
        
        # Attention: based on theta/beta ratio
        theta_beta_ratio = theta_power / beta_power if beta_power > 0.01 else 10.0
        if theta_beta_ratio <= 1.5:
            attention_deficit = "NORMAL"
        elif theta_beta_ratio <= 2.0:
            attention_deficit = "BORDERLINE"
        else:
            attention_deficit = "IMPAIRED"
        
        # Store data point
        data.append({
            'time': round(time, 3),
            'amplitude': round(amplitude, 2),
            'theta_power': round(theta_power, 2),
            'alpha_power': round(alpha_power, 2),
            'beta_power': round(beta_power, 2),
            'gamma_power': round(gamma_power, 2),
            'command': command,
            'visual_impairment': visual_impairment,
            'motor_impairment': motor_impairment,
            'attention_deficit': attention_deficit
        })
    
    return pd.DataFrame(data)

def main():
    print("🧠 Generating Enhanced EEG Sample Data...")
    print(f"📊 Parameters: {SAMPLING_RATE}Hz, {DURATION}s, {NUM_SAMPLES} samples")
    
    # Generate data
    df = generate_eeg_data()
    
    # Save to file
    output_path = "data/raw/sample_eeg_data.csv"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} samples")
    print(f"📁 Saved to: {output_path}")
    print(f"\n📋 Columns: {list(df.columns)}")
    print(f"\n🔍 Sample data (first 5 rows):")
    print(df.head())
    
    # Print scenario summary
    print(f"\n📈 Scenario Distribution:")
    print(f"  0-2s: Normal baseline")
    print(f"  2-4s: FOCUS (high beta)")
    print(f"  4-6s: RELAX (high alpha)")
    print(f"  6-7s: Visual impairment (low alpha)")
    print(f"  7-8s: Motor impairment (low beta)")
    print(f"  8-9s: Attention deficit (high theta/beta ratio)")
    print(f"  9-10s: Mixed state")
    
    print(f"\n✨ Ready for visualization!")
    print(f"Run: python scripts/visualizer_from_file.py {output_path}")

if __name__ == "__main__":
    main()
