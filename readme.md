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

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

## Usage

1. Start the application
2. Click "Start" to begin gesture detection
3. Rotate your hand clockwise to increase volume, anticlockwise to decrease
4. Use calibration and sensitivity controls as needed

## Tech Stack

- Python
- OpenCV
- MediaPipe Hands
- Pycaw
- CustomTkinter
