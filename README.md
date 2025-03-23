# WASD Robot Controller 🤖

A modern interface for controlling a two-wheeled robot using WASD keyboard controls. This project combines a Python-based GUI with Arduino-powered motor control for an intuitive robot control experience.

## Features ✨

- Modern, intuitive graphical interface
- Real-time visual feedback of key presses
- 8-directional movement control
- Smooth motor control with Arduino
- Status indicators for connection and movement
- Fail-safe timeout mechanism

## Hardware Requirements 🔧

- Arduino board (e.g., Arduino Uno)
- Two DC motors
- Motor driver (compatible with 4 control pins)
- USB cable for Arduino connection
- Robot chassis with two wheels

## Pin Configuration 📌

| Motor Control | Arduino Pin |
|--------------|-------------|
| Right Forward| 5           |
| Right Backward| 4          |
| Left Forward | 6           |
| Left Backward| 7           |

## Software Setup 🛠️

### Prerequisites

- Python 3.x
- Arduino IDE
- Required Python packages:
  ```bash
  pip install pyserial tkinter
  ```

### Installation

1. Upload the `main.ino` sketch to your Arduino board using the Arduino IDE
2. Connect your Arduino to your computer via USB
3. Run the Python interface:
   ```bash
   python main.py
   ```

## Controls 🎮

| Key Combination | Movement Direction |
|-----------------|-------------------|
| W               | Forward           |
| S               | Backward          |
| A               | Turn Left         |
| D               | Turn Right        |
| W + A           | Forward-Left      |
| W + D           | Forward-Right     |
| S + A           | Backward-Left     |
| S + D           | Backward-Right    |

## Features in Detail 🔍

### GUI Interface
- Real-time status display
- Visual key press feedback
- Connection status indicator
- Movement direction display

### Arduino Control
- PWM motor speed control
- Automatic motor stop on communication timeout
- Smooth diagonal movement support
- Fail-safe mechanisms

## Troubleshooting 🔧

1. **Connection Issues**
   - Verify the correct COM port is selected (default: COM3)
   - Check USB cable connection
   - Ensure Arduino is properly powered

2. **Movement Problems**
   - Verify motor connections
   - Check motor driver power supply
   - Ensure correct pin configuration


## License 📄

This project is open source and available under the MIT License.
