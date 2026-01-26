# main.py
# 🌸 CareerSensei — Advanced Discord Career Advisor

import discord
from discord.ext import commands
from discord.ui import View, Button, Select
from datetime import datetime
from career_logic import recommend_careers
from config import BOT_TOKEN, BOT_NAME, VERSION
from database import init_db, save_user, load_user
from models import UserProfile
from career_logic import recommend_careers

# =============================
# BOT SETUP
# =============================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

init_db()


# =============================
# BOT READY
# =============================

@bot.event
async def on_ready():
    print(f"🌸 {BOT_NAME} v{VERSION} aktif!")
    await bot.change_presence(
        activity=discord.Game(name="Kariyer yollarını inceliyor 🌱")
    )


# =============================
# UI BİLEŞENLERİ
# =============================

class InterestSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Teknoloji", value="teknoloji"),
            discord.SelectOption(label="Tasarım", value="tasarım"),
            discord.SelectOption(label="İletişim", value="iletişim"),
            discord.SelectOption(label="İş & Girişim", value="iş"),
            discord.SelectOption(label="Veri & Analiz", value="veri"),
        ]
        super().__init__(
            placeholder="İlgi alanını seç",
            min_values=1,
            max_values=3,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.user_interests = self.values
        await interaction.response.send_message(
            f"✅ İlgi alanların kaydedildi: {', '.join(self.values)}",
            ephemeral=True
        )


class SkillSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Python", value="python"),
            discord.SelectOption(label="Analitik Düşünme", value="analitik"),
            discord.SelectOption(label="Yaratıcılık", value="yaratıcılık"),
            discord.SelectOption(label="İletişim", value="iletişim"),
            discord.SelectOption(label="Tasarım", value="tasarım"),
        ]
        super().__init__(
            placeholder="Güçlü becerilerini seç",
            min_values=1,
            max_values=3,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.user_skills = self.values
        await interaction.response.send_message(
            f"🧠 Becerilerin kaydedildi: {', '.join(self.values)}",
            ephemeral=True
        )


class ProfileView(View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.user_interests = []
        self.user_skills = []

        self.add_item(InterestSelect())
        self.add_item(SkillSelect())

        self.add_item(
            Button(
                label="🚀 Kariyerimi Öner",
                style=discord.ButtonStyle.success,
                custom_id="recommend"
            )
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    @discord.ui.button(label="🚀 Kariyerimi Öner", style=discord.ButtonStyle.success)
    async def recommend(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        if not self.user_interests or not self.user_skills:
            await interaction.response.send_message(
                "⚠️ Önce ilgi alanı ve beceri seçmelisin.",
                ephemeral=True
            )
            return

        profile = UserProfile(
            user_id=self.user_id,
            interests=list(self.user_interests),
            skills=list(self.user_skills),
            education_level="lise",
            wants_remote=True,
            risk_tolerance=3,
            language="tr",
            created_at=datetime.utcnow()
        )

        save_user(profile)

        results = recommend_careers(profile)

        if not results:
            await interaction.response.send_message(
                "🌑 Sana uygun net bir yol bulamadım.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🌸 Sensei’nin Kariyer Önerileri",
            description="Profiline göre en uyumlu yollar:",
            color=0xffb7c5
        )

        for r in results:
            embed.add_field(
                name=f"🎯 {r['career']} ({r['score']} puan)",
                value=f"{r['description']}\n\n🧠 *{r['reason']}*",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


# =============================
# KOMUTLAR
# =============================

@bot.command()
async def kariyer(ctx):
    existing = load_user(ctx.author.id)

    if existing:
        await ctx.send(
            "🌸 Seni hatırlıyorum.\n"
            "Yeni bir yol mu arıyoruz, yoksa eski profile devam mı?"
        )

    view = ProfileView(ctx.author.id)

    await ctx.send(
        "🧭 **CareerSensei ile Yolculuk Başlıyor**\n\n"
        "Aşağıdan ilgi alanlarını ve güçlü becerilerini seç:",
        view=view
    )


@bot.command()
async def help(ctx):
    await ctx.send(
        "🆘 **CareerSensei Komutları**\n\n"
        "`!kariyer` → Kariyer danışmanı\n"
        "`!help` → Yardım\n\n"
        "🌱 Kendini keşfet, yolunu seç."
    )


@bot.command()
async def tanitim(ctx):
    await ctx.send(
        "🎎 **CareerSensei**\n\n"
        "Kişisel ilgi ve becerilere göre\n"
        "kariyer yolları öneren akıllı bir Discord botudur.\n\n"
        "📌 MVP+++ | Veri tabanlı | UI destekli"
    )


# =============================
# RUN
# =============================

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
