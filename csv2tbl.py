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


from dataclasses import dataclass
from typing import TextIO
import docopt  # type: ignore


VERSION = 0.01


class Globals:
    debug: bool
    has_header: bool


@dataclass
class Col:
    num: int = 0
    _type: str = ''
    name: str = ''


@dataclass
class Defn:
    table_name: str
    primary_key: str
    cols: list[Col]


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
    if g.debug:
        print('create table:', defn_file)
    with open(defn_file, 'r') as f:
        defn = parse_defn_file(f)
        print(defn)


def load_table(defn_file: str, csv_file: str) -> None:
    if g.debug:
        print('load table:', defn_file, csv_file)


def parse_defn_file(defn_file: TextIO) -> Defn:
    defn = Defn('', '', [])
    cols: list[Col] = []
    for line in defn_file:
        line = line.strip()
        if line.startswith('#'):
            continue
        f = line.split()
        if len(f) == 0:
            continue
        if f[0] == 'table':
            defn.table_name = f[1]
        elif f[0] == 'primary_key':
            defn.primary_key = f[1]
        elif f[0] == 'col':
            col = Col()
            col.num = int(f[1])
            col._type = f[2]
            col.name = f[3]
            cols.append(col)
        else:
            assert False
    defn.cols = cols
    return defn


if __name__ == '__main__':
    main()
