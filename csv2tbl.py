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


import csv
from dataclasses import dataclass
from typing import TextIO

import docopt  # type: ignore


VERSION = 0.01
COMMIT_INTVL = 50


class Globals:
    debug: bool


@dataclass
class Col:
    num: int = 0
    _type: str = ''
    name: str = ''


@dataclass
class Defn:
    table_name: str
    primary_key: list[str]
    cols: list[Col]


g = Globals()


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    g.debug = args['--debug']
    has_header = args['-H']
    if g.debug:
        print(args)
    if args['create']:
        create_table(args['DEFNFILE'])
    elif args['load']:
        load_table(args['DEFNFILE'], args['CSVFILE'], has_header)
    else:
        assert False


def create_table(defn_file: str) -> None:
    if g.debug:
        print('create table:', defn_file)
    with open(defn_file, 'r') as f:
        defn = parse_defn_file(f)
        if g.debug:
            print(defn)
        print_create_stmt(defn)


def load_table(defn_file: str, csv_file: str, has_header: bool) -> None:
    if g.debug:
        print('load table:', defn_file, csv_file)
    with open(defn_file, 'r') as f1, open(csv_file, 'r') as f2:
        defn = parse_defn_file(f1)
        print_insert_statements(defn, f2, has_header)


def parse_defn_file(defn_file: TextIO) -> Defn:
    defn = Defn('', [''], [])
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
            defn.primary_key = f[1:]
        elif f[0] == 'col':
            col = Col()
            col.num = int(f[1])
            col._type = f[2]
            col.name = f[3]
            cols.append(col)
        else:
            assert False
    assert defn.table_name != ''
    assert defn.primary_key != ''
    defn.cols = cols
    assert len(defn.cols) > 0
    return defn


def print_create_stmt(defn: Defn) -> None:
    c_str = f'create table {defn.table_name} (\n'
    keycols = ', '.join(defn.primary_key)
    key = f',\n  primary key ({keycols})\n'
    cols = []
    if keycols == 'id_serial':   # special case: make an auto-increment column
        cols.append('  id serial')
        key = f',\n  primary key (id)\n'
    for col in defn.cols:
        s = f'  {col.name} {col._type}'
        cols.append(s)
    col_str = ',\n'.join(cols)
    stmt = c_str + col_str + key + ');'
    print(stmt)


def print_insert_statements(defn: Defn, f: TextIO, has_header: bool) -> None:
    s1 = f'insert into {defn.table_name}\n'
    names = [x.name for x in defn.cols]
    s1 += '(' + ', '.join(names) + ')\nvalues\n'
    reader = csv.reader(f)
    in_xaction = False
    for num, line in enumerate(reader):
        if has_header:
            has_header = False
            continue  # skip the first row
        values = '(' + get_values_list(defn, line) + ');\n'
        stmt = s1 + values
        if not in_xaction:
            print('begin transaction;')
            in_xaction = True
        print(stmt)
        if num % COMMIT_INTVL == 0:
            print('commit;')
            in_xaction = False
    if in_xaction:
        print('commit')

def get_values_list(defn: Defn, line: list[str]) -> str:
    vals: list[str] = []
    for col in defn.cols:
        vals.append(format_col(col, line))
    return ', '.join(vals)


def format_col(col: Col, line: list[str]) -> str:
    val = line[col.num - 1]
    if "'" in val:
        val = val.replace("'", "''")
    if col._type == 'text':
        val = "'" + val + "'"
    if col._type in ('smallint', 'integer') and val == '':
        val = '0'
    return val


if __name__ == '__main__':
    main()
