#!/usr/bin/env python3
from afk_guardian import AFKGuardian
import argparse

def main():
    parser = argparse.ArgumentParser(description='AFK Guardian - Virtual Workspace Supervisor')
    parser.add_argument('--threshold', type=int, default=60,
                        help='Time in seconds before user is considered AFK (default: 60)')
    parser.add_argument('--report', type=str, help='Generate report from log file')
    parser.add_argument('--preview', action='store_true', help='Show camera preview for demonstration')
    parser.add_argument('--heatmap', type=str, help='Generate activity heatmap from log file')
    parser.add_argument('--breaks', type=str, help='Analyze break patterns from log file')
    parser.add_argument('--productivity', type=str, help='Calculate productivity scores from log file')
    
    args = parser.parse_args()
    
    guardian = AFKGuardian(afk_threshold=args.threshold)
    
    if args.report:
        guardian.generate_report(args.report)
    elif args.heatmap:
        guardian.generate_heatmap(args.heatmap)
    elif args.breaks:
        guardian.analyze_breaks(args.breaks)
    elif args.productivity:
        guardian.calculate_productivity_score(args.productivity)
    elif args.preview:
        guardian.show_camera_preview()
    else:
        guardian.start()

if __name__ == "__main__":
    main()