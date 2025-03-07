#!/usr/bin/env python3
from afk_guardian import AFKGuardian
import argparse

def main():
    parser = argparse.ArgumentParser(description='AFK Guardian - Virtual Workspace Supervisor')
    parser.add_argument('--threshold', type=int, default=60,
                        help='Time in seconds before user is considered AFK (default: 60)')
    parser.add_argument('--report', type=str, help='Generate report from log file')
    
    args = parser.parse_args()
    
    guardian = AFKGuardian(afk_threshold=args.threshold)
    
    if args.report:
        guardian.generate_report(args.report)
    else:
        guardian.start()

if __name__ == "__main__":
    main()