# AFK Guardian - Virtual Workspace Supervisor

A simple application that monitors your presence at the computer and tracks productivity.

## Features

- Face detection using webcam
- Keyboard and mouse activity monitoring
- AFK alerts when you're away for too long
- Productivity analytics (time spent active vs. inactive)

## Requirements

- Python 3.6+
- OpenCV
- NumPy
- pynput
- plyer
- matplotlib

## Installation

1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Start monitoring

```bash
python src/run_afk_guardian.py