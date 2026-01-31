import sqlite3
import json
from typing import List, Optional
from models import CareerPath, CareerLevel

DB_NAME = "careersensei.db"


# -------------------------
# DB CONNECTION
# -------------------------
def get_connection():
    return sqlite3.connect(DB_NAME)


# -------------------------
# DB SETUP
# -------------------------
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        name TEXT PRIMARY KEY,
        interests TEXT,
        skills TEXT,
        education_level TEXT,
        remote_possible INTEGER,
        risk_level TEXT,
        levels TEXT,
        tags TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        interests TEXT,
        skills TEXT,
        recommended_career TEXT
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# CAREER SAVE
# -------------------------
def save_career(career: CareerPath):
    conn = get_connection()
    cursor = conn.cursor()

    levels_json = json.dumps([
        {
            "title": lvl.title,
            "min_experience": lvl.min_experience,
            "description": lvl.description
        }
        for lvl in career.levels
    ])

    cursor.execute("""
        INSERT OR REPLACE INTO careers
        (name, interests, skills, education_level, remote_possible,
         risk_level, levels, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        career.name,
        json.dumps(career.interests),
        json.dumps(career.skills),
        career.education_level,
        int(career.remote_possible),
        career.risk_level,
        levels_json,
        json.dumps(career.tags)
    ))

    conn.commit()
    conn.close()


# -------------------------
# LOAD CAREERS
# -------------------------
def load_careers() -> List[CareerPath]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM careers")
    rows = cursor.fetchall()
    conn.close()

    careers: List[CareerPath] = []

    for row in rows:
        levels_data = json.loads(row[6])
        levels = [
            CareerLevel(
                title=lvl["title"],
                min_experience=lvl["min_experience"],
                description=lvl["description"]
            )
            for lvl in levels_data
        ]

        careers.append(
            CareerPath(
                name=row[0],
                interests=json.loads(row[1]),
                skills=json.loads(row[2]),
                education_level=row[3],
                remote_possible=bool(row[4]),
                risk_level=row[5],
                levels=levels,
                tags=json.loads(row[7])
            )
        )

    return careers


# -------------------------
# USER PROFILE
# -------------------------
def save_user_profile(
    user_id: str,
    interests: List[str],
    skills: List[str],
    recommended_career: Optional[str]
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users
        (user_id, interests, skills, recommended_career)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        json.dumps(interests),
        json.dumps(skills),
        recommended_career
    ))

    conn.commit()
    conn.close()


def get_user_profile(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT interests, skills, recommended_career
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None

    return {
        "interests": json.loads(result[0]),
        "skills": json.loads(result[1]),
        "recommended_career": result[2]
    }
def save_or_update_user(user_id, interests, skills):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, interests, skills, recommended_career)
        VALUES (?, ?, ?, COALESCE(
            (SELECT recommended_career FROM users WHERE user_id=?), NULL)
        )
    """, (
        user_id,
        json.dumps(interests),
        json.dumps(skills),
        user_id
    ))

    conn.commit()
    conn.close()
