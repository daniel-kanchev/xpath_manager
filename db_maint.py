import sqlite3
import config


def find_bad_items():
    con = sqlite3.connect(config.db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    bad_items = cur.execute("SELECT id, user, date FROM log WHERE status='Running' AND body_xpath=''").fetchall()
    if bad_items:
        print(f'Items with no body:')
        for item in bad_items:
            print("ID: ", item['id'])
            print("User: ", item['user'])
            print("Date: ", item['date'])
            print("____________________________________________")

    bad_items = cur.execute("SELECT id, user, date FROM log WHERE start_urls=''").fetchall()

    if bad_items:
        print(f'Items with no URL:')
        for item in bad_items:
            print("ID: ", item['id'])
            print("User: ", item['user'])
            print("Date: ", item['date'])
            print("____________________________________________")

    bad_items = cur.execute("SELECT id, user, date FROM log WHERE botname='siteshtml' AND articles_xpath=''").fetchall()

    if bad_items:
        print(f'Siteshtml items with no Articles_xpath:')
        for item in bad_items:
            print("ID: ", item['id'])
            print("User: ", item['user'])
            print("Date: ", item['date'])
            print("____________________________________________")

    bad_items = cur.execute("SELECT id, user, date FROM log WHERE botname='siteshtml' AND title_xpath=''").fetchall()

    if bad_items:
        print(f'Siteshtml items with no title_xpath:')
        for item in bad_items:
            print("ID: ", item['id'])
            print("User: ", item['user'])
            print("Date: ", item['date'])
            print("____________________________________________")


if __name__ == '__main__':
    find_bad_items()
