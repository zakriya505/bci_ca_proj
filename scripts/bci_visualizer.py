#!/usr/bin/env python3
"""
BCI Visual Display - Real-time LED and Command Visualization
Shows LED states, buzzer activations, and cursor movements
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import re
import time

class BCIVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("RISC-V BCI System - Visual Display")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # State variables
        self.led_state = False
        self.buzzer_active = False
        self.cursor_x = 0
        self.cursor_y = 0
        self.current_command = "NONE"
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🧠 RISC-V Brain-Computer Interface",
            font=("Arial", 24, "bold"),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        title.pack(pady=20)
        
        # LED Display
        led_frame = tk.Frame(self.root, bg='#1e1e1e')
        led_frame.pack(pady=20)
        
        tk.Label(
            led_frame,
            text="LED Status:",
            font=("Arial", 16),
            bg='#1e1e1e',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.led_canvas = tk.Canvas(
            led_frame,
            width=100,
            height=100,
            bg='#1e1e1e',
            highlightthickness=0
        )
        self.led_canvas.pack(side=tk.LEFT, padx=10)
        
        # Draw LED circle
        self.led_circle = self.led_canvas.create_oval(
            10, 10, 90, 90,
            fill='#333333',
            outline='#666666',
            width=3
        )
        
        self.led_label = tk.Label(
            led_frame,
            text="OFF",
            font=("Arial", 20, "bold"),
            bg='#1e1e1e',
            fg='#ff0000'
        )
        self.led_label.pack(side=tk.LEFT, padx=10)
        
        # Command Display
        cmd_frame = tk.Frame(self.root, bg='#1e1e1e')
        cmd_frame.pack(pady=20)
        
        tk.Label(
            cmd_frame,
            text="Current Command:",
            font=("Arial", 16),
            bg='#1e1e1e',
            fg='white'
        ).pack()
        
        self.command_label = tk.Label(
            cmd_frame,
            text="NONE",
            font=("Arial", 32, "bold"),
            bg='#1e1e1e',
            fg='#ffff00'
        )
        self.command_label.pack(pady=10)
        
        # Buzzer Indicator
        self.buzzer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 20, "bold"),
            bg='#1e1e1e',
            fg='#ff9900'
        )
        self.buzzer_label.pack(pady=10)
        
        # Cursor Position
        cursor_frame = tk.Frame(self.root, bg='#1e1e1e')
        cursor_frame.pack(pady=20)
        
        tk.Label(
            cursor_frame,
            text="Cursor Position:",
            font=("Arial", 14),
            bg='#1e1e1e',
            fg='white'
        ).pack()
        
        self.cursor_label = tk.Label(
            cursor_frame,
            text="(0, 0)",
            font=("Arial", 18),
            bg='#1e1e1e',
            fg='#00ffff'
        )
        self.cursor_label.pack(pady=5)
        
        # Status Log
        log_frame = tk.Frame(self.root, bg='#1e1e1e')
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(
            log_frame,
            text="Activity Log:",
            font=("Arial", 12),
            bg='#1e1e1e',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg='#2d2d2d',
            fg='#00ff00',
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Start/Stop Buttons
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start BCI System",
            font=("Arial", 14, "bold"),
            bg='#00aa00',
            fg='white',
            command=self.start_bci,
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=("Arial", 14, "bold"),
            bg='#aa0000',
            fg='white',
            command=self.stop_bci,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.running = False
        
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def update_led(self, state):
        """Update LED display"""
        self.led_state = state
        if state:
            self.led_canvas.itemconfig(self.led_circle, fill='#00ff00', outline='#00aa00')
            self.led_label.config(text="ON", fg='#00ff00')
            self.log("✓ LED turned ON")
        else:
            self.led_canvas.itemconfig(self.led_circle, fill='#333333', outline='#666666')
            self.led_label.config(text="OFF", fg='#ff0000')
            self.log("✗ LED turned OFF")
            
    def update_command(self, command):
        """Update current command display"""
        self.current_command = command
        self.command_label.config(text=command)
        
        if command == "FOCUS":
            self.command_label.config(fg='#00ff00')
        elif command == "RELAX":
            self.command_label.config(fg='#0099ff')
        elif command == "BLINK":
            self.command_label.config(fg='#ff9900')
        else:
            self.command_label.config(fg='#ffff00')
            
    def activate_buzzer(self):
        """Show buzzer activation"""
        self.buzzer_label.config(text="♪ BEEP! ♪")
        self.log("🔔 Buzzer activated!")
        self.root.after(500, lambda: self.buzzer_label.config(text=""))
        
    def update_cursor(self, x, y):
        """Update cursor position"""
        self.cursor_x = x
        self.cursor_y = y
        self.cursor_label.config(text=f"({x}, {y})")
        self.log(f"→ Cursor moved to ({x}, {y})")
        
    def parse_output(self, line):
        """Parse BCI output and update display"""
        # Detect LED state
        if "LED" in line and "ON" in line:
            self.root.after(0, lambda: self.update_led(True))
        elif "LED" in line and "OFF" in line:
            self.root.after(0, lambda: self.update_led(False))
            
        # Detect commands
        if "Detected: FOCUS" in line:
            self.root.after(0, lambda: self.update_command("FOCUS"))
        elif "Detected: RELAX" in line:
            self.root.after(0, lambda: self.update_command("RELAX"))
        elif "Detected: BLINK" in line:
            self.root.after(0, lambda: self.update_command("BLINK"))
        elif "Detected: NONE" in line:
            self.root.after(0, lambda: self.update_command("NONE"))
            
        # Detect buzzer
        if "BEEP" in line or "BUZZER" in line:
            self.root.after(0, self.activate_buzzer)
            
        # Detect cursor position
        cursor_match = re.search(r'Cursor Position: \((\d+), (\d+)\)', line)
        if cursor_match:
            x, y = int(cursor_match.group(1)), int(cursor_match.group(2))
            self.root.after(0, lambda: self.update_cursor(x, y))
            
    def run_bci_process(self):
        """Run BCI system and capture output"""
        try:
            process = subprocess.Popen(
                ['bin\\bci_system.exe'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace invalid characters
                bufsize=1
            )
            
            self.process = process
            
            for line in process.stdout:
                if not self.running:
                    process.terminate()
                    break
                self.parse_output(line)
                
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
        finally:
            self.root.after(0, self.on_bci_stopped)
            
    def start_bci(self):
        """Start BCI system"""
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log("🚀 Starting BCI System...")
        
        # Run in separate thread
        thread = threading.Thread(target=self.run_bci_process, daemon=True)
        thread.start()
        
    def stop_bci(self):
        """Stop BCI system"""
        self.running = False
        self.log("⏹ Stopping BCI System...")
        if hasattr(self, 'process'):
            self.process.terminate()
            
    def on_bci_stopped(self):
        """Called when BCI stops"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("✓ BCI System stopped")

def main():
    root = tk.Tk()
    app = BCIVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
