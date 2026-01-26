# database.py
"""
CareerSensei - Database Katmanı

Bu dosya şunları yapar:
- SQLite veritabanını oluşturur
- Kullanıcı profillerini kaydeder / yükler
- Kariyer ağaçlarını (CareerPath) saklar
- Uygulamanın hafızasını yönetir
"""

import sqlite3
import json
from typing import Optional, List

from models import UserProfile, CareerPath, CareerLevel

DB_NAME = "careersensei.db"


# =============================
# DB BAĞLANTISI
# =============================

def get_connection():
    return sqlite3.connect(DB_NAME)


# =============================
# DB OLUŞTURMA
# =============================

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Kullanıcı Profilleri
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        interests TEXT,
        skills TEXT,
        education_level TEXT,
        wants_remote INTEGER,
        risk_tolerance INTEGER,
        language TEXT,
        created_at TEXT
    )
    """)

    # Kariyer Ağaçları
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        name TEXT PRIMARY KEY,
        interests TEXT,
        skills TEXT,
        education_level TEXT,
        remote_possible INTEGER,
        risk_level INTEGER,
        levels TEXT,
        tags TEXT
    )
    """)

    conn.commit()
    conn.close()


# =============================
# USER PROFİLİ
# =============================

def save_user(profile: UserProfile):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users
    (user_id, interests, skills, education_level, wants_remote,
     risk_tolerance, language, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile.user_id,
        json.dumps(profile.interests),
        json.dumps(profile.skills),
        profile.education_level,
        int(profile.wants_remote),
        profile.risk_tolerance,
        profile.language,
        profile.created_at.isoformat()
    ))

    conn.commit()
    conn.close()


def load_user(user_id: int) -> Optional[UserProfile]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return UserProfile(
        user_id=row[0],
        interests=json.loads(row[1]),
        skills=json.loads(row[2]),
        education_level=row[3],
        wants_remote=bool(row[4]),
        risk_tolerance=row[5],
        language=row[6],
    )


# =============================
# KARİYER AĞAÇLARI
# =============================

def save_career(career: CareerPath):
    conn = get_connection()
    cursor = conn.cursor()

    levels_json = json.dumps([
        {
            "title": lvl.title,
            "min_experience": lvl.min_experience,
            "description": lvl.description
        } for lvl in career.levels
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
