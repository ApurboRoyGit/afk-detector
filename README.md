# AFK Guardian

A virtual workspace supervisor that monitors your activity and provides insights about your work patterns.

## Features

- Detects when you're away from keyboard (AFK) using:
  - Keyboard and mouse activity monitoring
  - Webcam-based face detection
- Generates detailed activity reports
- Creates activity heatmaps to visualize your work patterns
- Analyzes break patterns and provides recommendations
- Calculates productivity scores
- Modern web interface for real-time monitoring and analytics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/afk-guardian.git
cd afk-guardian
```
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Start monitoring

```bash
python src/run_afk_guardian.py