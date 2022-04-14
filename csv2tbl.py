#!/usr/bin/env python
"""
csv2tbl.py: Deduplicating utility for backup/restore

Usage:
    csv2tbl.py [--debug] create DEFNFILE
    csv2tbl.py [--debug] [-H] load DEFNFILE CSVFILE
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
    has_header: bool


g = Globals()


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    g.debug = args['--debug']
    g.has_header = args['-H']
    if g.debug:
        print(args)
    if args['create']:
        create_table(args['DEFNFILE'])
    elif args['load']:
        load_table(args['DEFNFILE'], args['CSVFILE'])
    else:
        assert False


def create_table(defn_file: str) -> None:
    print('create table:', defn_file)


def load_table(defn_file: str, csv_file: str) -> None:
    print('load table:', defn_file, csv_file)


if __name__ == '__main__':
    main()
