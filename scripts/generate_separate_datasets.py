#!/usr/bin/env python3
"""
Generate Separate EEG Datasets for Each Prediction Type

Creates three specialized datasets:
1. visual_impairment_data.csv - Focuses on alpha power variations
2. motor_impairment_data.csv - Focuses on beta power variations
3. attention_deficit_data.csv - Focuses on theta/beta ratio variations

Each dataset is optimized to showcase its specific prediction type.
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

def generate_visual_impairment_dataset():
    """Generate dataset focused on visual impairment (alpha power variations)"""
    print("📊 Generating Visual Impairment Dataset...")
    
    t = np.arange(0, DURATION, 1/SAMPLING_RATE)
    data = []
    
    for i, time in enumerate(t):
        # Vary alpha power to demonstrate visual impairment detection
        if time < 2.0:
            # Normal alpha - good visual processing
            theta_amp, alpha_amp, beta_amp, gamma_amp = 15, 55, 30, 10
            visual_status = "NORMAL"
        elif time < 4.0:
            # High alpha - excellent visual processing
            theta_amp, alpha_amp, beta_amp, gamma_amp = 12, 65, 28, 8
            visual_status = "NORMAL"
        elif time < 6.0:
            # Borderline alpha - slight visual concerns
            theta_amp, alpha_amp, beta_amp, gamma_amp = 18, 35, 32, 12
            visual_status = "BORDERLINE"
        elif time < 8.0:
            # Low alpha - visual impairment
            theta_amp, alpha_amp, beta_amp, gamma_amp = 25, 18, 38, 15
            visual_status = "IMPAIRED"
        else:
            # Very low alpha - severe visual impairment
            theta_amp, alpha_amp, beta_amp, gamma_amp = 30, 12, 40, 18
            visual_status = "IMPAIRED"
        
        # Generate composite signal
        theta_signal = generate_band_signal(THETA_FREQ, theta_amp, 1/SAMPLING_RATE, i*0.1)
        alpha_signal = generate_band_signal(ALPHA_FREQ, alpha_amp, 1/SAMPLING_RATE, i*0.15)
        beta_signal = generate_band_signal(BETA_FREQ, beta_amp, 1/SAMPLING_RATE, i*0.2)
        gamma_signal = generate_band_signal(GAMMA_FREQ, gamma_amp, 1/SAMPLING_RATE, i*0.3)
        
        amplitude = theta_signal + alpha_signal + beta_signal + gamma_signal
        amplitude = add_noise(np.array([amplitude]), noise_level=5.0)[0]
        amplitude = float(amplitude)
        
        # Calculate normalized band powers
        total_power = theta_amp + alpha_amp + beta_amp + gamma_amp
        theta_power = theta_amp / total_power
        alpha_power = alpha_amp / total_power
        beta_power = beta_amp / total_power
        gamma_power = gamma_amp / total_power
        
        # Command detection (secondary to visual prediction)
        if beta_power > 0.6:
            command = "FOCUS"
        elif alpha_power > 0.6:
            command = "RELAX"
        else:
            command = "NONE"
        
        data.append({
            'time': round(time, 3),
            'amplitude': round(amplitude, 2),
            'theta_power': round(theta_power, 2),
            'alpha_power': round(alpha_power, 2),
            'beta_power': round(beta_power, 2),
            'gamma_power': round(gamma_power, 2),
            'command': command,
            'visual_impairment': visual_status
        })
    
    return pd.DataFrame(data)

def generate_motor_impairment_dataset():
    """Generate dataset focused on motor impairment (beta power variations)"""
    print("📊 Generating Motor Impairment Dataset...")
    
    t = np.arange(0, DURATION, 1/SAMPLING_RATE)
    data = []
    
    for i, time in enumerate(t):
        # Vary beta power to demonstrate motor impairment detection
        if time < 2.0:
            # High beta - good motor control
            theta_amp, alpha_amp, beta_amp, gamma_amp = 12, 35, 60, 10
            motor_status = "NORMAL"
        elif time < 4.0:
            # Normal beta - healthy motor function
            theta_amp, alpha_amp, beta_amp, gamma_amp = 15, 38, 45, 12
            motor_status = "NORMAL"
        elif time < 6.0:
            # Borderline beta - slight motor concerns
            theta_amp, alpha_amp, beta_amp, gamma_amp = 20, 42, 30, 15
            motor_status = "BORDERLINE"
        elif time < 8.0:
            # Low beta - motor impairment
            theta_amp, alpha_amp, beta_amp, gamma_amp = 25, 48, 18, 18
            motor_status = "IMPAIRED"
        else:
            # Very low beta - severe motor impairment
            theta_amp, alpha_amp, beta_amp, gamma_amp = 30, 52, 10, 20
            motor_status = "IMPAIRED"
        
        # Generate composite signal
        theta_signal = generate_band_signal(THETA_FREQ, theta_amp, 1/SAMPLING_RATE, i*0.1)
        alpha_signal = generate_band_signal(ALPHA_FREQ, alpha_amp, 1/SAMPLING_RATE, i*0.15)
        beta_signal = generate_band_signal(BETA_FREQ, beta_amp, 1/SAMPLING_RATE, i*0.2)
        gamma_signal = generate_band_signal(GAMMA_FREQ, gamma_amp, 1/SAMPLING_RATE, i*0.3)
        
        amplitude = theta_signal + alpha_signal + beta_signal + gamma_signal
        amplitude = add_noise(np.array([amplitude]), noise_level=5.0)[0]
        amplitude = float(amplitude)
        
        # Calculate normalized band powers
        total_power = theta_amp + alpha_amp + beta_amp + gamma_amp
        theta_power = theta_amp / total_power
        alpha_power = alpha_amp / total_power
        beta_power = beta_amp / total_power
        gamma_power = gamma_amp / total_power
        
        # Command detection
        if beta_power > 0.6:
            command = "FOCUS"
        elif alpha_power > 0.6:
            command = "RELAX"
        else:
            command = "NONE"
        
        data.append({
            'time': round(time, 3),
            'amplitude': round(amplitude, 2),
            'theta_power': round(theta_power, 2),
            'alpha_power': round(alpha_power, 2),
            'beta_power': round(beta_power, 2),
            'gamma_power': round(gamma_power, 2),
            'command': command,
            'motor_impairment': motor_status
        })
    
    return pd.DataFrame(data)

def generate_attention_deficit_dataset():
    """Generate dataset focused on attention deficit (theta/beta ratio variations)"""
    print("📊 Generating Attention Deficit Dataset...")
    
    t = np.arange(0, DURATION, 1/SAMPLING_RATE)
    data = []
    
    for i, time in enumerate(t):
        # Vary theta/beta ratio to demonstrate attention deficit detection
        if time < 2.0:
            # Low theta, high beta - good attention (ratio ~0.5)
            theta_amp, alpha_amp, beta_amp, gamma_amp = 10, 35, 50, 12
            attention_status = "NORMAL"
        elif time < 4.0:
            # Normal ratio (~1.0) - healthy attention
            theta_amp, alpha_amp, beta_amp, gamma_amp = 20, 38, 40, 15
            attention_status = "NORMAL"
        elif time < 6.0:
            # Borderline ratio (~1.75) - slight attention concerns
            theta_amp, alpha_amp, beta_amp, gamma_amp = 35, 40, 30, 12
            attention_status = "BORDERLINE"
        elif time < 8.0:
            # High ratio (~2.5) - attention deficit
            theta_amp, alpha_amp, beta_amp, gamma_amp = 50, 42, 20, 10
            attention_status = "IMPAIRED"
        else:
            # Very high ratio (~5.0) - severe attention deficit
            theta_amp, alpha_amp, beta_amp, gamma_amp = 60, 45, 12, 8
            attention_status = "IMPAIRED"
        
        # Generate composite signal
        theta_signal = generate_band_signal(THETA_FREQ, theta_amp, 1/SAMPLING_RATE, i*0.1)
        alpha_signal = generate_band_signal(ALPHA_FREQ, alpha_amp, 1/SAMPLING_RATE, i*0.15)
        beta_signal = generate_band_signal(BETA_FREQ, beta_amp, 1/SAMPLING_RATE, i*0.2)
        gamma_signal = generate_band_signal(GAMMA_FREQ, gamma_amp, 1/SAMPLING_RATE, i*0.3)
        
        amplitude = theta_signal + alpha_signal + beta_signal + gamma_signal
        amplitude = add_noise(np.array([amplitude]), noise_level=5.0)[0]
        amplitude = float(amplitude)
        
        # Calculate normalized band powers
        total_power = theta_amp + alpha_amp + beta_amp + gamma_amp
        theta_power = theta_amp / total_power
        alpha_power = alpha_amp / total_power
        beta_power = beta_amp / total_power
        gamma_power = gamma_amp / total_power
        
        # Command detection
        if beta_power > 0.6:
            command = "FOCUS"
        elif alpha_power > 0.6:
            command = "RELAX"
        else:
            command = "NONE"
        
        data.append({
            'time': round(time, 3),
            'amplitude': round(amplitude, 2),
            'theta_power': round(theta_power, 2),
            'alpha_power': round(alpha_power, 2),
            'beta_power': round(beta_power, 2),
            'gamma_power': round(gamma_power, 2),
            'command': command,
            'attention_deficit': attention_status
        })
    
    return pd.DataFrame(data)

def main():
    print("🧠 Generating Separate EEG Datasets for Each Prediction Type...")
    print(f"📊 Parameters: {SAMPLING_RATE}Hz, {DURATION}s, {NUM_SAMPLES} samples each\n")
    
    # Ensure directory exists
    os.makedirs("data/raw", exist_ok=True)
    
    # Generate and save visual impairment dataset
    df_visual = generate_visual_impairment_dataset()
    visual_path = "data/raw/visual_impairment_data.csv"
    df_visual.to_csv(visual_path, index=False)
    print(f"✅ Visual Impairment Dataset: {len(df_visual)} samples")
    print(f"   Saved to: {visual_path}")
    print(f"   Columns: {list(df_visual.columns)}\n")
    
    # Generate and save motor impairment dataset
    df_motor = generate_motor_impairment_dataset()
    motor_path = "data/raw/motor_impairment_data.csv"
    df_motor.to_csv(motor_path, index=False)
    print(f"✅ Motor Impairment Dataset: {len(df_motor)} samples")
    print(f"   Saved to: {motor_path}")
    print(f"   Columns: {list(df_motor.columns)}\n")
    
    # Generate and save attention deficit dataset
    df_attention = generate_attention_deficit_dataset()
    attention_path = "data/raw/attention_deficit_data.csv"
    df_attention.to_csv(attention_path, index=False)
    print(f"✅ Attention Deficit Dataset: {len(df_attention)} samples")
    print(f"   Saved to: {attention_path}")
    print(f"   Columns: {list(df_attention.columns)}\n")
    
    # Print summary
    print("=" * 60)
    print("📈 Dataset Summaries:\n")
    
    print("📁 Visual Impairment Dataset (Alpha Power Focus):")
    print("   0-2s:  NORMAL (alpha ~0.50)")
    print("   2-4s:  NORMAL (alpha ~0.59)")
    print("   4-6s:  BORDERLINE (alpha ~0.32)")
    print("   6-8s:  IMPAIRED (alpha ~0.19)")
    print("   8-10s: IMPAIRED (alpha ~0.10)\n")
    
    print("📁 Motor Impairment Dataset (Beta Power Focus):")
    print("   0-2s:  NORMAL (beta ~0.51)")
    print("   2-4s:  NORMAL (beta ~0.41)")
    print("   4-6s:  BORDERLINE (beta ~0.28)")
    print("   6-8s:  IMPAIRED (beta ~0.16)")
    print("   8-10s: IMPAIRED (beta ~0.09)\n")
    
    print("📁 Attention Deficit Dataset (Theta/Beta Ratio Focus):")
    print("   0-2s:  NORMAL (ratio ~0.20)")
    print("   2-4s:  NORMAL (ratio ~0.50)")
    print("   4-6s:  BORDERLINE (ratio ~1.75)")
    print("   6-8s:  IMPAIRED (ratio ~2.50)")
    print("   8-10s: IMPAIRED (ratio ~5.00)\n")
    
    print("=" * 60)
    print("✨ All datasets generated successfully!")
    print("\n🚀 Run visualizations:")
    print("   .\\run_visual_impairment.ps1")
    print("   .\\run_motor_impairment.ps1")
    print("   .\\run_attention_deficit.ps1")

if __name__ == "__main__":
    main()
