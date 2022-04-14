#!/usr/bin/env python
"""
csv2tbl.py: Deduplicating utility for backup/restore

Usage:
    csv2tbl.py [--debug] create DEFNFILE
    csv2tbl.py [--debug] [-H] load DEFNFILE CSFILE
    csv2tbl.py --version
    csv2tbl.py --help

Options:
    --debug -d         Print debug information to stdout.
    -H                 CSV file has a header line
    --version          Show version and exit.
    -h --help          Show this message and exit.
"""


import docopt  # type: ignore


VERSION = 0.01


class Globals:
    debug: bool


g = Globals()


def main():
    args = docopt.docopt(__doc__, version=VERSION)
    g.debug = args['--debug']
    if g.debug:
        print(args)


if __name__ == '__main__':
    main()
