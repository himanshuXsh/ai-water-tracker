import sqlite3
from datetime import datetime, timedelta

DB_NAME = "water.db"


# -------------------------------
# Create Tables
# -------------------------------

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        daily_goal INTEGER
    )
    """)

    # Water intake table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_intake (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# -------------------------------
# User Functions
# -------------------------------

def create_user(username: str, daily_goal: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, daily_goal) VALUES (?, ?)",
        (username, daily_goal)
    )

    conn.commit()
    conn.close()


def get_user(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, daily_goal FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    return user  # (id, daily_goal)


def update_user_goal(username: str, new_goal: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET daily_goal = ? WHERE username = ?",
        (new_goal, username)
    )

    conn.commit()
    conn.close()


# -------------------------------
# Intake Functions
# -------------------------------

def log_intake(username: str, amount: int, date: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get user ID
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return False

    user_id = user[0]

    cursor.execute(
        "INSERT INTO water_intake (user_id, amount, date) VALUES (?, ?, ?)",
        (user_id, amount, date)
    )

    conn.commit()
    conn.close()

    return True


def get_history(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, date
        FROM water_intake
        JOIN users ON water_intake.user_id = users.id
        WHERE users.username = ?
        ORDER BY date DESC
    """, (username,))

    records = cursor.fetchall()
    conn.close()

    return records


# -------------------------------
# Daily / Weekly / Monthly Analytics
# -------------------------------

def get_today_total(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT SUM(amount)
        FROM water_intake
        JOIN users ON water_intake.user_id = users.id
        WHERE users.username = ?
        AND date LIKE ?
    """, (username, f"{today}%"))

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0


def get_weekly_total(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT SUM(amount)
        FROM water_intake
        JOIN users ON water_intake.user_id = users.id
        WHERE users.username = ?
        AND date >= ?
    """, (username, seven_days_ago))

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0


def get_monthly_total(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    first_day_of_month = datetime.now().strftime("%Y-%m-01")

    cursor.execute("""
        SELECT SUM(amount)
        FROM water_intake
        JOIN users ON water_intake.user_id = users.id
        WHERE users.username = ?
        AND date >= ?
    """, (username, first_day_of_month))

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0


def get_weekly_chart_data(username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT substr(date, 1, 10) as day, SUM(amount)
        FROM water_intake
        JOIN users ON water_intake.user_id = users.id
        WHERE users.username = ?
        AND date >= ?
        GROUP BY day
        ORDER BY day
    """, (username, seven_days_ago))

    rows = cursor.fetchall()
    conn.close()

    data = [
        {"date": row[0], "total_ml": row[1]}
        for row in rows
    ]

    return data
