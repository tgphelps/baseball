
from collections import defaultdict
import psycopg2  # type: ignore

import util

runs: defaultdict[int, int] = defaultdict(lambda: 0)


def main():
    conn_string = "host='localhost' dbname='baseball'" + \
                  "  user='tgphelps' password='524835'"
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            print("connected")

            cur.execute("select v_line_score, h_line_score from gamelogs")
            # data = cur.fetchall()
            # pprint.pprint(data, indent=2)
            for row in cur:
                # print(row[0], '->', util.line_score_to_ints(row[0]))
                # print(row[1], '->', util.line_score_to_ints(row[1]))
                # print()
                do_line_score(util.line_score_to_ints(row[0]))
                do_line_score(util.line_score_to_ints(row[1]))

    print("connection closed")
    print_run_stats()


def do_line_score(inning: list[int]) -> None:
    print('do', inning)
    for i in inning:
    #   if i not in runs:
    #     runs[i] = 0
        runs[i] += 1


def print_run_stats() -> None:
    total = sum([runs[i] for i in runs])
    print('Total:', total)
    for r in sorted(runs.keys()):
        pct = float(runs[r]) / total * 100
        print(r, '->', runs[r], f'{pct:4.2f}%')


if __name__ == '__main__':
    main()
