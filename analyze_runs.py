
"""
analyze_runs.py: Shows run production stats

Usage:
    analyze_runs.py [--innings-by-runs]

Options:
    -h  --help         Show this screen.
    --version          Show version.
    --innings-by-runs  Show in how many innings teams scored N runs
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
            print_reports(args, cur)

    print("connection closed")


def print_reports(args: dict[str, str],
                  cur: psycopg2.extensions.cursor) -> None:
    if args['--innings-by-runs']:
        print_innings_by_runs(cur)


def print_innings_by_runs(cur: psycopg2.extensions.cursor) -> None:
    cur.execute("select v_line_score, h_line_score from gamelogs")
    for row in cur:
        do_line_score(util.line_score_to_ints(row[0]))
        do_line_score(util.line_score_to_ints(row[1]))
    print_run_stats()  # XXX


def do_line_score(inning: list[int]) -> None:
    # print('do', inning)
    for i in inning:
        g.runs[i] += 1


def print_run_stats() -> None:
    total = sum([g.runs[i] for i in g.runs])
    print('Total:', total)
    for r in sorted(g.runs.keys()):
        pct = float(g.runs[r]) / total * 100
        print(r, '->', g.runs[r], f'{pct:4.2f}%')


if __name__ == '__main__':
    main()
