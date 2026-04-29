import psycopg2
from config import DB_CONFIG


def connect():
    return psycopg2.connect(**DB_CONFIG)


def get_player_id(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM players WHERE username = %s",
        (username,)
    )

    player = cur.fetchone()

    if player:
        player_id = player[0]

    else:
        cur.execute(
            """
            INSERT INTO players(username)
            VALUES(%s)
            RETURNING id
            """,
            (username,)
        )

        player_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return player_id


def save_result(username, score, level):
    player_id = get_player_id(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES(%s, %s, %s)
        """,
        (player_id, score, level)
    )

    conn.commit()

    cur.close()
    conn.close()


def get_leaderboard():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            p.username,
            g.score,
            g.level_reached,
            g.played_at
        FROM game_sessions g
        JOIN players p
        ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
        """
    )

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


def get_personal_best(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p
        ON g.player_id = p.id
        WHERE p.username = %s
        """,
        (username,)
    )

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result:
        return result

    return 0