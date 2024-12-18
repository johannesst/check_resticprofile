#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" nagios plugin for checking resticprofile status files """

import argparse
import json
import sys
import traceback
from datetime import datetime
from dateutil import parser

def check_file(file,command,profile,warning,critical):
    ''' Check status file '''
    warning=int(warning) * 60 * 60
    critical=int(critical) * 60 * 60

    with  open(file, 'r',encoding='utf-8') as status_file:
        status=json.load(status_file)
    status_file.close()
    status_data=status['profiles'][profile][command]
    #error=status['error']
    #stderr=status_data['stderr']
    duration=status_data['duration']
    timefmt=parser.parse(status_data['time']).replace(tzinfo=None)
    last=datetime.now()-timefmt
    last=int(last.total_seconds())
    perf_data=f"'Last {command}'={last}s;{warning};{critical};; 'Duration'={duration}s;;;"
    status_lines=f'Last {command} {int(last/60/60)} hours ago took {duration} sec | {perf_data}'
    if not status_data['success']:
        print(f'CRITICAL: Last {command} failed | {perf_data} ')
        for i in status_data['stderr'].splitlines():
            print(i)
        sys.exit(2)

    else:
        if last > critical:
            print(f'CRITICAL: {status_lines} ')
            sys.exit(2)
        elif last > warning:
            print(f'WARNING: {status_lines}')
            sys.exit(1)
        elif last < warning:
            print(f'OK: {status_lines}')
            sys.exit(0)
        else:
            print('UNKNOWN')
            sys.exit(3)


# runtime environment and data evaluation
def main():
    ''' main method nothing to see'''
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument('-w', '--warning', metavar='HOURS', default='24',
                      help='return warning if last successfull COMMAND job is older than HOURS')
    argp.add_argument('-c', '--critical', metavar='HOURS', default='48',
                      help='return critical if last successfull COMMAND job is older than HOURS')
    argp.add_argument('-C', '--command', default = 'backup',
                      help='COMMAND to check for, Default: backup')
    argp.add_argument('-p', '--profile', default = 'default',
                      help='profile to use, Default: default')
    argp.add_argument('-f', '--file',required=True,
                      help='Path to resticprofile status file')
    args = argp.parse_args()
    try:
        check_file(args.file,args.command,args.profile,args.warning,args.critical)
    except Exception as err:
        print(f"UNKNOWN: Unexpected {err=}, {type(err)=})")
        print("Trace: "  + traceback.format_exc())
        sys.exit(3)


if __name__ == '__main__':
    main()
