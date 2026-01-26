# models.py
"""
CareerSensei - Veri Modelleri

Bu dosya:
- Kullanıcı profili
- Kariyer tanımı
- Kariyer ağaçları (Junior → Senior → Lead)
için temel veri yapılarını içerir.

Bu yapı sayesinde:
- Recommendation engine sade kalır
- Database katmanı temiz olur
- UI tarafı karmaşıklaşmaz
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


# =============================
# KULLANICI PROFİLİ
# =============================

@dataclass
class UserProfile:
    user_id: int
    interests: List[str]
    skills: List[str]
    education_level: str
    wants_remote: bool
    risk_tolerance: int  # 1 (düşük) - 5 (yüksek)
    language: str = "tr"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def summary(self) -> str:
        """
        Kullanıcı profilini özetleyen kısa metin
        (UI ve loglama için kullanılır)
        """
        return (
            f"İlgi alanları: {', '.join(self.interests)} | "
            f"Beceriler: {', '.join(self.skills)} | "
            f"Risk: {self.risk_tolerance}/5"
        )


# =============================
# KARİYER SEVİYESİ
# =============================

@dataclass
class CareerLevel:
    title: str              # Junior Developer, Senior Designer vb.
    min_experience: int     # yıl
    description: str


# =============================
# KARİYER AĞACI
# =============================

@dataclass
class CareerPath:
    name: str                              # Yazılım Geliştirici
    interests: List[str]
    skills: List[str]
    education_level: str
    remote_possible: bool
    risk_level: int                        # 1–5
    levels: List[CareerLevel]              # Junior → Senior → Lead
    tags: List[str] = field(default_factory=list)

    def current_level(self, experience_years: int) -> CareerLevel:
        """
        Kullanıcının tecrübesine göre hangi seviyede olduğunu bulur
        """
        eligible_levels = [
            lvl for lvl in self.levels
            if experience_years >= lvl.min_experience
        ]
        return eligible_levels[-1] if eligible_levels else self.levels[0]

    def future_levels(self, experience_years: int) -> List[CareerLevel]:
        """
        Kullanıcının ileride ulaşabileceği seviyeleri verir
        """
        return [
            lvl for lvl in self.levels
            if lvl.min_experience > experience_years
        ]


# =============================
# ÖNERİ SONUCU (UI İÇİN)
# =============================

@dataclass
class RecommendationResult:
    career_name: str
    score: int
    reason: str
    description: str
    current_level: Optional[str] = None
    next_steps: List[str] = field(default_factory=list)
