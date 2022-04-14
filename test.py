
import psycopg2  # type: ignore


def main():
    conn_string = "host='localhost' dbname='baseball'" + \
                  "  user='tgphelps' password='524835'"
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            print("connected")

            cur.execute("select * from pg_database")
            # data = cur.fetchall()
            # pprint.pprint(data, indent=2)
            for row in cur:
                print(row)

    print("connection closed")


if __name__ == '__main__':
    main()
