import sqlite3
import config


def fetch_user_stats(user, user2=''):
    con = sqlite3.connect(config.db_path)
    cursor = con.cursor()
    stats = {
        'title_xpath': {},
        'pubdate_xpath': {},
        'author_xpath': {},
        'body_xpath': {},
    }
    cursor.execute("SELECT title_xpath, pubdate_xpath, author_xpath, body_xpath FROM log WHERE user=? OR user=?", (user, user2))
    results = cursor.fetchall()
    for entry in results:
        if entry[0] and entry[0] in stats['title_xpath']:
            stats['title_xpath'][entry[0]] += 1
        else:
            stats['title_xpath'][entry[0]] = 1

        if entry[1] and entry[1] in stats['pubdate_xpath']:
            stats['pubdate_xpath'][entry[1]] += 1
        else:
            stats['pubdate_xpath'][entry[1]] = 1

        if entry[2] and entry[2] in stats['author_xpath']:
            stats['author_xpath'][entry[2]] += 1
        else:
            stats['author_xpath'][entry[2]] = 1

        if entry[3] and entry[3] in stats['body_xpath']:
            stats['body_xpath'][entry[3]] += 1
        else:
            stats['body_xpath'][entry[3]] = 1

    for key in stats.keys():
        stats[key] = sorted(stats[key].items(), key=lambda x: x[1], reverse=True)[:20]

    lines = [f'\n{user}\n']
    for key in stats.keys():
        lines.append(f'\n{key}:\n')
        for xpath in stats[key]:
            lines.append(f'{xpath[0]}: {xpath[1]}\n')

    with open('stats.txt', 'a') as file:
        file.writelines(lines)
        file.close()

    with open('stats.txt', 'w') as f:
        f.close()


if __name__ == "__main__":
    fetch_user_stats(user="Daniel")
    fetch_user_stats(user="Simeon")
    fetch_user_stats(user="Hristo", user2="Bat Icho")
