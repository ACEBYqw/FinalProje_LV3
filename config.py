# config.py
# Kariyer Danışmanı Botu - MVP++ Konfigürasyonu

# Discord entegrasyonu MVP++ kapsamında planlıdır
# Token final sürümde eklenecektir
BOT_TOKEN = ''

# Uygulama durumu
APP_STAGE = "mvp"   # mvp / production

# Bot bilgileri
BOT_NAME = "CareerAdvisorBot"
VERSION = "MVP++"

# Özellik bayrakları
FEATURE_FLAGS = {
    "career_recommendation": True,
    "user_profiling": True,
    "discord_integration": False  # MVP++’ta planlı ama aktif değil
}

# Veri kaynağı
DATA_SOURCE = "in_memory"  # json / database (ileride)