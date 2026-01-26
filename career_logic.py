# career_logic.py
"""
Kariyer öneri motoru
- Puanlama sistemi
- Açıklama üretimi
- Genişletilebilir mimari
"""

from dataclasses import dataclass
from typing import List, Dict


# -----------------------------
# DATA MODELLERİ
# -----------------------------

@dataclass
class Career:
    name: str
    interests: List[str]
    skills: List[str]
    education_level: str
    remote_possible: bool
    risk_level: int  # 1 = düşük, 5 = yüksek
    description: str


@dataclass
class UserProfile:
    interests: List[str]
    skills: List[str]
    education_level: str
    wants_remote: bool
    risk_tolerance: int  # 1–5 arası


# -----------------------------
# KARİYER VERİ SETİ (DEMO)
# -----------------------------

CAREERS: List[Career] = [
    Career(
        name="Yazılım Geliştirici",
        interests=["teknoloji", "problem çözme", "mantık"],
        skills=["python", "algoritma", "debug"],
        education_level="lise",
        remote_possible=True,
        risk_level=2,
        description="Uygulama ve sistem geliştirir."
    ),
    Career(
        name="Veri Analisti",
        interests=["veri", "istatistik", "analiz"],
        skills=["python", "sql", "excel"],
        education_level="üniversite",
        remote_possible=True,
        risk_level=2,
        description="Verilerden anlamlı sonuçlar çıkarır."
    ),
    Career(
        name="Girişimci",
        interests=["iş", "liderlik", "yenilik"],
        skills=["iletişim", "strateji", "satış"],
        education_level="fark etmez",
        remote_possible=False,
        risk_level=5,
        description="Kendi işini kurar ve yönetir."
    ),
    Career(
        name="UI/UX Tasarımcı",
        interests=["tasarım", "yaratıcılık", "kullanıcı deneyimi"],
        skills=["figma", "tasarım", "empati"],
        education_level="lise",
        remote_possible=True,
        risk_level=3,
        description="Kullanıcı dostu arayüzler tasarlar."
    ),
]


# -----------------------------
# PUANLAMA MOTORU
# -----------------------------

def calculate_score(user: UserProfile, career: Career) -> int:
    score = 0

    # İlgi alanı eşleşmesi
    score += len(set(user.interests) & set(career.interests)) * 3

    # Beceri eşleşmesi
    score += len(set(user.skills) & set(career.skills)) * 4

    # Eğitim seviyesi uyumu
    if career.education_level == "fark etmez":
        score += 2
    elif user.education_level == career.education_level:
        score += 3

    # Uzaktan çalışma tercihi
    if user.wants_remote and career.remote_possible:
        score += 2

    # Risk uyumu
    risk_diff = abs(user.risk_tolerance - career.risk_level)
    score += max(0, 3 - risk_diff)

    return score


# -----------------------------
# AÇIKLAMA ÜRETİCİ
# -----------------------------

def generate_reason(user: UserProfile, career: Career) -> str:
    reasons = []

    common_interests = set(user.interests) & set(career.interests)
    if common_interests:
        reasons.append(
            f"ilgi alanların ({', '.join(common_interests)}) bu meslekle uyumlu"
        )

    common_skills = set(user.skills) & set(career.skills)
    if common_skills:
        reasons.append(
            f"sahip olduğun beceriler ({', '.join(common_skills)}) avantaj sağlıyor"
        )

    if user.wants_remote and career.remote_possible:
        reasons.append("uzaktan çalışma isteğine uygun")

    if abs(user.risk_tolerance - career.risk_level) <= 1:
        reasons.append("risk alma seviyenle uyumlu")

    if not reasons:
        return "profilinle genel olarak uyumlu bir kariyer"

    return "Bu meslek önerildi çünkü " + ", ".join(reasons) + "."


# -----------------------------
# ANA ÖNERİ FONKSİYONU
# -----------------------------

def recommend_careers(user: UserProfile, top_n: int = 3) -> List[Dict]:
    scored = []

    for career in CAREERS:
        score = calculate_score(user, career)
        scored.append((career, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    recommendations = []
    for career, score in scored[:top_n]:
        recommendations.append({
            "career": career.name,
            "score": score,
            "description": career.description,
            "reason": generate_reason(user, career)
        })

    return recommendations
