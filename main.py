import tkinter as tk
import serial
import time
import threading

class WASDKeyboardVisualization(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WASD Robot Controller")
        self.geometry("400x500")
        
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'key_bg': '#2d2d2d',
            'key_active': '#00ff9d',
            'text': '#ffffff',
            'status_good': '#4CAF50',
            'status_error': '#f44336'
        }
        
        self.configure(bg=self.colors['bg'])
        
        # Create main frame with padding
        self.main_frame = tk.Frame(self, bg=self.colors['bg'], padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Status display
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.status_frame.pack(fill='x', pady=(0, 20))
        
        self.status_label = tk.Label(self.status_frame, text="STATUS", 
                                    font=("Helvetica", 12, "bold"),
                                    fg=self.colors['text'], bg=self.colors['bg'])
        self.status_label.pack()
        
        self.connection_status = tk.Label(self.status_frame, text="Connecting...",
                                         font=("Helvetica", 10),
                                         fg=self.colors['text'], bg=self.colors['bg'])
        self.connection_status.pack(pady=5)
        
        # Movement status
        self.movement_status = tk.Label(self.status_frame, text="Stopped",
                                       font=("Helvetica", 10),
                                       fg=self.colors['text'], bg=self.colors['bg'])
        self.movement_status.pack(pady=5)
        
        # Keys frame
        self.keys_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.keys_frame.pack(expand=True)
        
        # Create dictionary for key widgets and state tracking
        self.keys = {}
        self.key_states = {"w": False, "a": False, "s": False, "d": False}
        self.current_direction = None
        self.running = True
        
        # Create modern key buttons
        key_style = {
            'font': ("Helvetica", 24, "bold"),
            'width': 3,
            'height': 1,
            'bg': self.colors['key_bg'],
            'fg': self.colors['text'],
            'relief': 'flat',
            'bd': 0
        }
        
        # Layout keys
        self.keys['w'] = tk.Label(self.keys_frame, text="W", **key_style)
        self.keys['w'].grid(row=0, column=1, padx=10, pady=10)
        
        self.keys['a'] = tk.Label(self.keys_frame, text="A", **key_style)
        self.keys['a'].grid(row=1, column=0, padx=10, pady=10)
        
        self.keys['s'] = tk.Label(self.keys_frame, text="S", **key_style)
        self.keys['s'].grid(row=1, column=1, padx=10, pady=10)
        
        self.keys['d'] = tk.Label(self.keys_frame, text="D", **key_style)
        self.keys['d'].grid(row=1, column=2, padx=10, pady=10)
        
        # Attempt to connect to Arduino
        try:
            self.ser = serial.Serial('COM3', 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            self.connection_status.config(text="Connected to Arduino", fg=self.colors['status_good'])
        except Exception as e:
            self.connection_status.config(text=f"Connection Error: {str(e)}", fg=self.colors['status_error'])
            self.ser = None
        
        # Bind key events
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)
        self.focus_set()
        
        # Start control thread
        self.control_thread = threading.Thread(target=self.send_movement_commands, daemon=True)
        self.control_thread.start()
    
    def add_key_labels(self):
        """Add labels describing key functions"""
        labels = {
            'w': 'Forward',
            'a': 'Left',
            's': 'Backward',
            'd': 'Right'
        }
        
        for key, text in labels.items():
            label = tk.Label(self.keys_frame, text=text,
                           font=("Helvetica", 10),
                           fg=self.colors['text'],
                           bg=self.colors['bg'])
            row, col = self.keys[key].grid_info()['row'], self.keys[key].grid_info()['column']
            # Increase vertical spacing and adjust positioning
            if key == 'w':
                label.grid(row=row+2, column=col, pady=(5, 0))
            else:
                label.grid(row=row-1, column=col, pady=(0, 5))
    
    def send_command(self, command):
        """Send a command character to the Arduino."""
        if self.ser:
            try:
                self.ser.write(command.encode())
            except Exception as e:
                self.connection_status.config(text=f"Communication Error: {str(e)}",
                                            fg=self.colors['status_error'])
    
    def get_movement_command(self):
        """Determine movement command based on currently pressed keys."""
        w = self.key_states['w']
        s = self.key_states['s']
        a = self.key_states['a']
        d = self.key_states['d']
        
        # Ignore opposing keys
        if (w and s) or (a and d):
            return None
            
        # Diagonal movements
        if w and a: return 'q'  # forward-left
        if w and d: return 'e'  # forward-right
        if s and a: return 'z'  # backward-left
        if s and d: return 'c'  # backward-right
        
        # Single direction movements
        if w: return 'w'
        if s: return 's'
        if a: return 'a'
        if d: return 'd'
        
        return None

    def send_movement_commands(self):
        """Continuously sends the current movement command while keys are held."""
        while self.running:
            command = self.get_movement_command()
            if command:
                self.send_command(command)
            else:
                self.send_command('x')  # stop if no valid command
            time.sleep(0.1)
    
    def on_key_press(self, event):
        """Handle key press events with smooth animation."""
        key = event.keysym.lower()
        if key in self.keys and not self.key_states[key]:
            self.key_states[key] = True
            self.keys[key].configure(bg=self.colors['key_active'])
            
            # Get combined movement command
            command = self.get_movement_command()
            if command:
                # Update movement status
                status_text = {
                    'w': 'Moving Forward',
                    's': 'Moving Backward',
                    'a': 'Turning Left',
                    'd': 'Turning Right',
                    'q': 'Moving Forward-Left',
                    'e': 'Moving Forward-Right',
                    'z': 'Moving Backward-Left',
                    'c': 'Moving Backward-Right'
                }.get(command, 'Unknown')
                self.movement_status.config(text=status_text)
    
    def on_key_release(self, event):
        """Handle key release events with smooth animation."""
        key = event.keysym.lower()
        if key in self.keys:
            self.key_states[key] = False
            self.keys[key].configure(bg=self.colors['key_bg'])
            
            # Get new movement command after key release
            command = self.get_movement_command()
            if not command:
                self.movement_status.config(text="Stopped")
            else:
                # Update status for remaining active keys
                status_text = {
                    'w': 'Moving Forward',
                    's': 'Moving Backward',
                    'a': 'Turning Left',
                    'd': 'Turning Right',
                    'q': 'Moving Forward-Left',
                    'e': 'Moving Forward-Right',
                    'z': 'Moving Backward-Left',
                    'c': 'Moving Backward-Right'
                }.get(command, 'Unknown')
                self.movement_status.config(text=status_text)
    
    def on_close(self):
        """Clean up resources on window close."""
        self.running = False
        if self.ser:
            self.ser.close()
        self.destroy()

if __name__ == "__main__":
    app = WASDKeyboardVisualization()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
