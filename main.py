# main.py
import discord
from discord.ext import commands
from datetime import date
import random

# -----------------------------
# CONFIG
# -----------------------------
BOT_TOKEN = ""
BOT_NAME = "CareerSensei"
VERSION = "1.0"

# -----------------------------
# INTENTS
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# -----------------------------
# XP / LEVEL / BADGE
# -----------------------------
USER_XP = {}
USER_LEVEL = {}
DAILY_USED = {}
USER_PROFILES = {}  # Kullanıcı profilleri hafızada
USER_PREVIOUS = {}  # Önceki kariyer önerileri

BADGES = {
    5: "Rising Star 🌟",
    10: "Career Master 🏆",
    15: "Legendary Mentor 👑"
}

def add_xp(user_id, amount):
    USER_XP[user_id] = USER_XP.get(user_id, 0) + amount
    USER_LEVEL[user_id] = USER_XP[user_id] // 100 + 1
    return USER_LEVEL[user_id], USER_XP[user_id]

def get_level(user_id):
    return USER_LEVEL.get(user_id, 1), USER_XP.get(user_id, 0)

def get_badge(user_id):
    lvl = USER_LEVEL.get(user_id, 1)
    badge = ""
    for threshold, name in sorted(BADGES.items()):
        if lvl >= threshold:
            badge = name
    return badge

# -----------------------------
# READY
# -----------------------------
@bot.event
async def on_ready():
    print(f"{BOT_NAME} v{VERSION} aktif!")
    await bot.change_presence(activity=discord.Game(name="Kariyer yollarını keşfet 🌱"))

# -----------------------------
# HELP KOMUTU
# -----------------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🆘 Komutlar",
        description="CareerSensei botunu kullanabileceğin komutlar:",
        color=0xffb7c5
    )
    embed.add_field(name="!kariyer", value="Kariyer testini başlatır ve ilgi/beceri toplar", inline=False)
    embed.add_field(name="!profil", value="Profilini gösterir", inline=False)
    embed.add_field(name="!gunluk", value="Günlük XP alırsın", inline=False)
    embed.add_field(name="!oner", value="Kariyer önerisi alırsın", inline=False)
    embed.add_field(name="!onceki", value="Önceki kariyer önerilerini gör", inline=False)
    embed.add_field(name="!leaderboard", value="XP liderlerini gösterir", inline=False)
    embed.add_field(name="!mini", value="Günlük mini test / challenge ile ekstra XP kazan", inline=False)
    await ctx.send(embed=embed)

# -----------------------------
# GÜNLÜK ÖDÜL
# -----------------------------
@bot.command()
async def gunluk(ctx):
    uid = ctx.author.id
    today = date.today()
    if DAILY_USED.get(uid) == today:
        await ctx.send("⏳ Bugün zaten günlük ödülünü aldın.")
        return
    DAILY_USED[uid] = today
    lvl, xp = add_xp(uid, 50)
    badge = get_badge(uid)
    await ctx.send(f"🎁 +50 XP! Level {lvl} | XP {xp} | {badge}")

# -----------------------------
# PROFİL
# -----------------------------
@bot.command()
async def profil(ctx):
    uid = ctx.author.id
    lvl, xp = get_level(uid)
    badge = get_badge(uid)
    profile = USER_PROFILES.get(uid, {"interests": [], "skills": []})
    interests = ", ".join(profile["interests"]) if profile["interests"] else "Yok"
    skills = ", ".join(profile["skills"]) if profile["skills"] else "Yok"
    embed = discord.Embed(title=f"👤 {ctx.author.name} Profil", color=0xffb7c5)
    embed.add_field(name="🆙 Level / XP / Badge", value=f"{lvl} / {xp} / {badge}", inline=False)
    embed.add_field(name="🎯 İlgi alanları", value=interests, inline=False)
    embed.add_field(name="⚡ Beceriler", value=skills, inline=False)
    await ctx.send(embed=embed)

# -----------------------------
# KARİYER KOMUTU
# -----------------------------
CAREER_INTERESTS = ["Yazılım", "Tasarım", "İletişim", "İş & Girişim", "Analitik Düşünme", "Yaratıcılık"]
CAREER_SKILLS = ["Analiz", "Yaratıcılık", "İletişim", "Problem Çözme", "Tasarım", "Python"]

@bot.command()
async def kariyer(ctx):
    uid = ctx.author.id
    USER_PROFILES[uid] = {"interests": [], "skills": []}

    await ctx.send(f"🧭 {ctx.author.mention}, ilgi alanını seç: {', '.join(CAREER_INTERESTS)}")

    def check_interest(m):
        return m.author == ctx.author and m.content in CAREER_INTERESTS

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check_interest)
        USER_PROFILES[uid]["interests"].append(msg.content)
    except:
        await ctx.send("⏳ Süre doldu, işlem iptal edildi.")
        return

    await ctx.send(f"⚡ Şimdi becerini seç: {', '.join(CAREER_SKILLS)}")

    def check_skill(m):
        return m.author == ctx.author and m.content in CAREER_SKILLS

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check_skill)
        USER_PROFILES[uid]["skills"].append(msg.content)
        await ctx.send("✅ Hazırsın! Kariyer önerisini almak için `!oner` komutunu kullanabilirsin.")
    except:
        await ctx.send("⏳ Süre doldu, işlem iptal edildi.")

# -----------------------------
# KARIYER ÖNERİSİ
# -----------------------------
CAREER_RESULTS = {
    "Yazılım": ["Yazılım Geliştirici", "Oyun Programcısı", "Veri Analisti"],
    "Tasarım": ["UI/UX Tasarımcı", "Grafik Tasarımcı", "Dijital Pazarlama"],
    "İletişim": ["Halkla İlişkiler", "Satış Uzmanı", "Müşteri Deneyimi"],
    "İş & Girişim": ["Girişimci", "İş Analisti", "Pazarlama Uzmanı"],
    "Analitik Düşünme": ["Veri Analisti", "Finans Analisti", "İstatistikçi"],
    "Yaratıcılık": ["Reklamcı", "Sanat Yönetmeni", "Yaratıcı Yazarlık"]
}

@bot.command()
async def oner(ctx):
    uid = ctx.author.id
    profile = USER_PROFILES.get(uid)
    if not profile or not profile["interests"] or not profile["skills"]:
        await ctx.send("❌ Önce `!kariyer` ile profil oluşturmalısın.")
        return

    interests = profile["interests"]
    skills = profile["skills"]

    recommended = []
    for intr in interests:
        recommended.extend(CAREER_RESULTS.get(intr, []))

    recommended = recommended[:3]  # ilk 3 öneri
    USER_PREVIOUS[uid] = recommended

    lvl, xp = add_xp(uid, 50)
    badge = get_badge(uid)

    embed = discord.Embed(title="🌸 Sensei'nin Önerisi", color=0xffb7c5)
    embed.add_field(name="🎯 En Çok Önerilen", value=recommended[0], inline=False)
    if len(recommended) > 1:
        embed.add_field(name="💡 Diğer Öneriler", value=", ".join(recommended[1:]), inline=False)
    embed.add_field(name="🆙 Level / XP / Badge", value=f"{lvl} / {xp} / {badge}", inline=False)
    await ctx.send(embed=embed)

# -----------------------------
# ÖNCEKİ ÖNERİLER
# -----------------------------
@bot.command()
async def onceki(ctx):
    uid = ctx.author.id
    prev = USER_PREVIOUS.get(uid)
    if not prev:
        await ctx.send("❌ Önceki önerin bulunamadı.")
        return
    await ctx.send(f"📝 Önceki Önerin: {', '.join(prev)}")

# -----------------------------
# LEADERBOARD
# -----------------------------
@bot.command()
async def leaderboard(ctx):
    if not USER_XP:
        await ctx.send("Henüz kimse yok.")
        return
    sorted_users = sorted(USER_XP.items(), key=lambda x: x[1], reverse=True)[:5]
    msg = "🏆 Liderlik Tablosu\n"
    for i, (uid, xp) in enumerate(sorted_users, start=1):
        user = await bot.fetch_user(uid)
        lvl = USER_LEVEL.get(uid, 1)
        badge = get_badge(uid)
        msg += f"{i}. {user.name} — XP {xp} | Level {lvl} | {badge}\n"
    await ctx.send(msg)

# -----------------------------
# MINI TEST
# -----------------------------
MINI_QUESTS = [
    {"question": "Python dilinde değişken ataması için hangi sembol kullanılır?", "answer": "="},
    {"question": "HTML’de başlık etiketi hangisidir?", "answer": "h1"},
    {"question": "Veri analizinde yaygın kullanılan Python kütüphanesi?", "answer": "pandas"}
]

@bot.command()
async def mini(ctx):
    quest = random.choice(MINI_QUESTS)
    await ctx.send(f"🧩 Günlük Challenge: {quest['question']} (cevabını yaz)")

    def check(m):
        return m.author == ctx.author

    try:
        msg = await bot.wait_for("message", timeout=30.0, check=check)
        if msg.content.strip().lower() == quest["answer"].lower():
            lvl, xp = add_xp(ctx.author.id, 20)
            badge = get_badge(ctx.author.id)
            await ctx.send(f"✅ Doğru! +20 XP | Level {lvl} | XP {xp} | {badge}")
        else:
            await ctx.send(f"❌ Yanlış! Doğru cevap: {quest['answer']}")
    except:
        await ctx.send("⏳ Süre doldu!")

# -----------------------------
# RUN
# -----------------------------
bot.run(BOT_TOKEN)
