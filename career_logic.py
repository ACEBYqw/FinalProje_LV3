# career_logic.py
"""
CareerSensei - Kariyer Öneri Motoru
models.py + database.py uyumlu
"""

from typing import List, Dict
from models import CareerPath, UserProfile
from database import load_careers


# -----------------------------
# PUANLAMA MOTORU
# -----------------------------

def calculate_score(user: UserProfile, career: CareerPath) -> int:
    score = 0

    # İlgi alanı eşleşmesi
    score += len(set(user.interests) & set(career.interests)) * 3

    # Beceri eşleşmesi
    score += len(set(user.skills) & set(career.skills)) * 4

    # Eğitim seviyesi
    if career.education_level.lower() == "fark etmez":
        score += 2
    elif user.education_level.lower() == career.education_level.lower():
        score += 3

    # Uzaktan çalışma
    if user.wants_remote and career.remote_possible:
        score += 2

    # Risk uyumu
    risk_diff = abs(user.risk_tolerance - career.risk_level)
    score += max(0, 3 - risk_diff)

    return score


# -----------------------------
# AÇIKLAMA ÜRETİCİ
# -----------------------------

def generate_reason(user: UserProfile, career: CareerPath) -> str:
    reasons = []

    if set(user.interests) & set(career.interests):
        reasons.append("ilgi alanlarınla örtüşüyor")

    if set(user.skills) & set(career.skills):
        reasons.append("becerilerinle uyumlu")

    if user.wants_remote and career.remote_possible:
        reasons.append("uzaktan çalışmaya uygun")

    if abs(user.risk_tolerance - career.risk_level) <= 1:
        reasons.append("risk tercihinle uyumlu")

    if not reasons:
        return "genel profil uyumu yüksek"

    return "Bu kariyer önerildi çünkü " + ", ".join(reasons) + "."


# -----------------------------
# ANA ÖNERİ FONKSİYONU
# -----------------------------

def recommend_careers(user: UserProfile, top_n: int = 3) -> List[Dict]:
    careers = load_careers()

    scored = []
    for career in careers:
        scored.append((career, calculate_score(user, career)))

    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    for career, score in scored[:top_n]:
        results.append({
            "career": career.name,
            "score": score,
            "description": career.levels[0].description if career.levels else "",
            "reason": generate_reason(user, career),
            "risk_level": career.risk_level,
            "remote_possible": career.remote_possible,
            "tags": career.tags
        })

    return results
