#!/usr/bin/env python3
from PngFile import PngFile
import argparse
import sys


def return_args():
    parser = argparse.ArgumentParser('Key parser')
    parser.add_argument('--headers', action='store_true')
    parser.add_argument('--data', action='store_true')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--filename', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = return_args()
    if args.filename is not None:
        try:
            file = PngFile(args.filename)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(-1)
        if args.all:
            file.print_headers_and_data()
        elif args.headers:
            file.print_headers()
        elif args.data:
            file.print_data()
        else:
            print('No keys given')
    else:
        print('No file given')
