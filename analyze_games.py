#!/bin/env python

"""
analyze_games.py: Run analysis over all games

Usage:
    analyze_games.py <analysis>

Options:
    -h  --help         Show this screen.
    --version          Show version.

<analysis> can be one of:
    count-games         Count games in database.
    run-clumpiness      Show how often N runs occur in an inning.
    home-advantage      Show percentage of games home team won.
    runs-by-inning      Show how many runs occur in inning N.
"""

from collections import defaultdict

import psycopg2  # type: ignore
import docopt  # type: ignore

import util

VERSION = "0.0.1"


# class Globals():
#    runs: defaultdict[int, int]


# g = Globals()
# g.runs = defaultdict(lambda: 0)


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
            elif s == 'run-clumpiness':
                run_clumpiness(cur)
            elif s == 'home-advantage':
                home_advantage(cur)
            elif s == 'runs-by-inning':
                runs_by_inning(cur)
            else:
                print('ERROR: bad analysis specified')


def count_games(cur: psycopg2.extensions.cursor) -> None:
    "Show total number of games in the database."
    cur.execute('select count(*) from gamelogs')
    n = cur.fetchone()[0]
    print(f'Total games played: {n}')


def run_clumpiness(cur: psycopg2.extensions.cursor) -> None:
    "Show distribution of runs scored in an inning."
    runs: defaultdict[int, int] = defaultdict(lambda: 0)
    cur.execute("select v_line_score, h_line_score from gamelogs")
    for row in cur:
        for i in util.line_score_to_ints(row[0]):
            runs[i] += 1
        for i in util.line_score_to_ints(row[1]):
            runs[i] += 1
    total = sum([runs[i] for i in runs])
    print('Total innings:', total)
    for r in sorted(runs.keys()):
        pct = float(runs[r]) / total * 100.0
        print(r, '->', runs[r], f'{pct:4.2f}%')


def runs_by_inning(cur: psycopg2.extensions.cursor) -> None:
    runs: defaultdict[int, tuple[int, int]] = defaultdict(lambda: (0, 0))
    # runs[n] = (count, runs_scored)
    cur.execute("select v_line_score, h_line_score from gamelogs")
    for row in cur:
        print(row[0])
        print(row[1])
        for i, scored in enumerate(util.line_score_to_ints(row[0])):
            inning = i + 1
            count, total = runs[inning]
            runs[inning] = (count + 1, total + scored)
        for i, scored in enumerate(util.line_score_to_ints(row[1])):
            inning = i + 1
            count, total = runs[inning]
            runs[inning] = (count + 1, total + scored)
        # break
    for key in runs:
        n = runs[key][0]
        r = runs[key][1]
        print(key, runs[key], f'  {r / n: 4.2f}')


def home_advantage(cur: psycopg2.extensions.cursor) -> None:
    "Show percentage of games won by the home team."
    games = 0
    visitor_wins = 0
    home_wins = 0
    cur.execute("select v_score, h_score from gamelogs")
    for row in cur:
        games += 1
        if row[0] > row[1]:
            visitor_wins += 1
        else:
            home_wins += 1
    pct = float(home_wins) / games * 100.0
    print(f'Home winning percentage: {pct:4.2f}')


if __name__ == '__main__':
    main()
