# AirVolume

A desktop application that uses hand gesture recognition to control system volume via webcam.

## Features

- Real-time hand gesture detection using MediaPipe
- Smooth volume control with clockwise/anticlockwise hand rotation
- Modern dark UI with CustomTkinter
- Live webcam preview with hand landmark overlay
- Volume meter and FPS counter
- Sensitivity adjustment and calibration

## Requirements

- Python 3.8+
- Windows 10/11 (for Pycaw volume control)
- Webcam

## Installation

1. **Install Python 3.8 or higher**
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Clone or download the repository**
   ```bash
   git clone https://github.com/thakursudhanshu/airvolume.git
   cd airvolume
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Usage

1. Launch the application
2. Click "Start Detection" to begin gesture recognition
3. Position your hand in front of the webcam
4. Rotate your hand clockwise to increase volume, counterclockwise to decrease
5. Use the sensitivity slider to adjust gesture responsiveness
6. Click "Calibrate" if the gesture detection needs resetting
7. Use "Mute" to toggle audio on/off

## Troubleshooting

- **Camera not accessible**: Ensure no other applications are using the webcam
- **Volume control not working**: Pycaw requires Windows audio APIs (works on Windows 10/11)
- **Import errors**: Make sure all dependencies are installed correctly
- **Performance issues**: Close other resource-intensive applications

## Tech Stack

- Python
- OpenCV
- MediaPipe Hands
- Pycaw
- CustomTkinter
