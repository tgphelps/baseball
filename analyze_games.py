#!/bin/env python

"""
analyze_games.py: Run analysis over all games

Usage:
    analyze_games.py <analysis>

Options:
    -h  --help         Show this screen.
    --version          Show version.

<analysis> can be one of:
    count-games         Count games in database
    innings-by-runs     Show how often N runs occur in an inning
"""

from collections import defaultdict

import psycopg2  # type: ignore
import docopt  # type: ignore

import util

VERSION = "0.0.1"


class Globals():
    runs: defaultdict[int, int]


g = Globals()
g.runs = defaultdict(lambda: 0)


def main():
    args = docopt.docopt(__doc__, version=VERSION)
    conn_string = "host='localhost' dbname='baseball'" + \
                  "  user='tgphelps' password='524835'"
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            # print("connected")
            # print(args)
            s = args['<analysis>']
            if s == 'count-games':
                count_games(cur)
            elif s == 'innings-by-runs':
                innings_by_runs(cur)
            else:
                print('ERROR: bad analysis specified')


def count_games(cur: psycopg2.extensions.cursor) -> None:
    cur.execute('select count(*) from gamelogs')
    n = cur.fetchone()[0]
    print(f'Total games played: {n}')


def innings_by_runs(cur: psycopg2.extensions.cursor) -> None:
    cur.execute("select v_line_score, h_line_score from gamelogs")
    for row in cur:
        for i in util.line_score_to_ints(row[0]):
            g.runs[i] += 1
        for i in util.line_score_to_ints(row[1]):
            g.runs[i] += 1
    total = sum([g.runs[i] for i in g.runs])
    print('Total:', total)
    for r in sorted(g.runs.keys()):
        pct = float(g.runs[r]) / total * 100
        print(r, '->', g.runs[r], f'{pct:4.2f}%')


if __name__ == '__main__':
    main()
