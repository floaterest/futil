import os
import argparse

from utils.writer import Writer, MODES
from utils.common import is_image

RED = '\033[1;31m'
RESET = '\033[0;0m'


def main():
    parser = argparse.ArgumentParser(description='generate a image viewer in HTML')
    parser.add_argument('path', type=str,
                        help='directory path (use double quote if needed)')
    parser.add_argument('mode', type=str, nargs='?', default=next(iter(MODES)),
                        help=f'display mode, available modes are {list(MODES.keys())}')
    # note: wrapping is based on global page number
    # not page number inside each chapter
    parser.add_argument('wrap', type=int, nargs='?', default=0,
                        help='wrap option: '
                             '0 to wrap after each page, '
                             '1 to wrap after page with odd page numbers (1-indexed), '
                             '2 to wrap after page with even page numbers (1-indexed)')
    args = parser.parse_args()
    assert args.mode in MODES, f'"{args.mode}" is not a valid mode!'
    assert os.path.exists(args.path), f'"{args.path}" is not a valid path!'

    for r, ds, fs in os.walk(os.path.abspath(args.path)):
        if fs := [f for f in os.listdir(r) if is_image(f.lower())]:
            print(r, args.mode, args.wrap)
            os.chdir(r)
            Writer(args.mode, args.wrap, sorted(fs)).write('index')
        else:
            print(RED + f'no images in "{r}"' + RESET)


if __name__ == '__main__':
    main()
