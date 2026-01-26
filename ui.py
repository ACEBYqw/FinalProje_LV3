
import discord
from discord.ui import View, Select

class ProfileView(View):
    def __init__(self):
        super().__init__(timeout=300)
        self.user_data = {
            "interests": [],
            "skills": []
        }

        self.add_item(InterestSelect(self))
        self.add_item(SkillSelect(self))


class InterestSelect(Select):
    def __init__(self, parent: ProfileView):
        self.parent = parent
        options = [
            discord.SelectOption(label="Yazılım", value="teknoloji"),
            discord.SelectOption(label="Tasarım", value="tasarım"),
            discord.SelectOption(label="Veri / Analiz", value="veri"),
            discord.SelectOption(label="İş & Girişim", value="iş"),
        ]

        super().__init__(
            placeholder="🧭 İlgi alanını seç",
            min_values=1,
            max_values=2,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.parent.user_data["interests"] = self.values
        await interaction.response.send_message(
            f"✅ İlgi alanı kaydedildi: {', '.join(self.values)}",
            ephemeral=True
        )


class SkillSelect(Select):
    def __init__(self, parent: ProfileView):
        self.parent = parent
        options = [
            discord.SelectOption(label="Analitik Düşünme", value="analiz"),
            discord.SelectOption(label="Yaratıcılık", value="yaratıcılık"),
            discord.SelectOption(label="İletişim", value="iletişim"),
            discord.SelectOption(label="Problem Çözme", value="problem"),
        ]

        super().__init__(
            placeholder="⚔️ Güçlü yönlerini seç",
            min_values=1,
            max_values=2,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.parent.user_data["skills"] = self.values
        await interaction.response.send_message(
            f"✅ Güçlü yönler kaydedildi: {', '.join(self.values)}",
            ephemeral=True
        )
