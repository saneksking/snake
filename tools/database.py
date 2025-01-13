import sqlite3

conn = sqlite3.connect('snake_game.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL,
        score INTEGER NOT NULL
    )
''')
conn.commit()


def save_score(nickname, score):
    c.execute('SELECT score FROM scores WHERE nickname = ?', (nickname,))
    result = c.fetchone()

    if result:
        existing_score = result[0]
        if score > existing_score:
            c.execute('UPDATE scores SET score = ? WHERE nickname = ?', (score, nickname))
    else:
        c.execute('INSERT INTO scores (nickname, score) VALUES (?, ?)', (nickname, score))

    conn.commit()


def get_leaderboard_records(limit=5):
    c.execute('SELECT nickname, score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    return c.fetchall()

