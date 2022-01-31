import sqlite3


def sync(db_from_path, db_to_path):
    db_from = sqlite3.connect(db_from_path)
    cur_from = db_from.cursor()

    db_to = sqlite3.connect(db_to_path)
    cur_to = db_to.cursor()

    ids_from = [item_id[0] for item_id in cur_from.execute("SELECT id FROM log").fetchall()]
    print(len(ids_from))

    ids_to = [item_id[0] for item_id in cur_to.execute("SELECT id FROM log").fetchall()]
    print(len(ids_to))

    ids_to_ad = []
    for item_id in ids_from:
        if item_id not in ids_to:
            ids_to_ad.append(item_id)
    print(len(ids_to_ad))

    if not ids_to_ad:
        return

    full_items_to_add = []
    for item_id in ids_to_ad:
        full_items_to_add.append(cur_from.execute("SELECT * FROM log WHERE id=?", (item_id,)).fetchone())
    print(full_items_to_add)
    for full_item in full_items_to_add:
        cur_to.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", full_item)

    db_to.commit()
    db_to.close()
    db_from.close()


if __name__ == "__main__":
    db1 = input("Database to pull from:")
    db2 = input("Database to insert into:")
    sync(db_from_path=db1, db_to_path=db2)
