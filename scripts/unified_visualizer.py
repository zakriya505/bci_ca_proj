#!/usr/bin/env python3
"""
BCI Unified Visualizer - All Visualizations in One Window
Navigate between different visualization modes using buttons.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk
import subprocess
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

class UnifiedBCIVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("BCI Unified Visualizer")
        self.root.geometry("500x480")
        self.root.configure(bg='#1a1a2e')
        self.current_process = None
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🧠 BCI Visualization System",
            font=("Segoe UI", 20, "bold"),
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Select a visualization mode:",
            font=("Segoe UI", 12),
            fg='#888888',
            bg='#1a1a2e'
        )
        subtitle.pack(pady=5)
        
        # Button frame
        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(pady=20, padx=40, fill='x')
        
        # Visualization buttons
        buttons = [
            ("📊 General EEG", "sample_eeg_data.csv", "#4CAF50"),
            ("👁️ Visual Impairment", "visual_impairment_data.csv", "#9C27B0"),
            ("🏃 Motor Impairment", "motor_impairment_data.csv", "#2196F3"),
            ("🎯 Attention Deficit", "attention_deficit_data.csv", "#FF9800"),
            ("📈 Compare All", "comparison", "#E91E63"),
            ("🖥️ Complete CA View", "complete", "#00BCD4"),
        ]
        
        for text, dataset, color in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 11, "bold"),
                fg='white',
                bg=color,
                activebackground=color,
                activeforeground='white',
                relief='flat',
                cursor='hand2',
                command=lambda d=dataset: self.launch_visualizer(d)
            )
            btn.pack(fill='x', pady=5, ipady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready - Select a visualization mode")
        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            fg='#666666',
            bg='#1a1a2e'
        )
        status.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Close visualization window to return here",
            font=("Segoe UI", 9, "italic"),
            fg='#555555',
            bg='#1a1a2e'
        )
        instructions.pack(side='bottom', pady=10)
    
    def launch_visualizer(self, dataset):
        self.status_var.set(f"Launching {dataset}...")
        self.root.update()
        
        if dataset == "comparison":
            script = os.path.join(script_dir, "visualize_all_predictions.py")
            cmd = [sys.executable, script]
        elif dataset == "complete":
            # Launch complete CA visualizer with default dataset
            script = os.path.join(script_dir, "complete_visualizer.py")
            filepath = os.path.join(os.path.dirname(script_dir), "data", "raw", "sample_eeg_data.csv")
            cmd = [sys.executable, script, filepath]
        else:
            if dataset == "sample_eeg_data.csv":
                filepath = os.path.join(os.path.dirname(script_dir), "data", "raw", dataset)
                if not os.path.exists(filepath):
                    filepath = os.path.join(os.path.dirname(script_dir), dataset)
            else:
                filepath = os.path.join(os.path.dirname(script_dir), "data", "raw", dataset)
            
            script = os.path.join(script_dir, "visualizer_from_file.py")
            cmd = [sys.executable, script, filepath]
        
        def run_viz():
            try:
                self.current_process = subprocess.Popen(cmd, cwd=os.path.dirname(script_dir))
                self.current_process.wait()
                self.root.after(100, lambda: self.status_var.set("Ready - Select a visualization mode"))
            except Exception as e:
                self.root.after(100, lambda: self.status_var.set(f"Error: {str(e)[:30]}"))
        
        thread = threading.Thread(target=run_viz, daemon=True)
        thread.start()
        self.status_var.set(f"Running: {dataset}")
    
    def on_closing(self):
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = UnifiedBCIVisualizer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
