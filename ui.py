# ui.py
import discord
from discord.ui import View, Select
from database import save_user_profile

class ProfileView(View):
    def __init__(self, user):
        super().__init__(timeout=300)
        self.user = user
        self.user_data = {"interests": [], "skills": []}
        self.add_item(InterestSelect(self))

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if hasattr(self, "message"):
            await self.message.edit(view=self)

class InterestSelect(Select):
    def __init__(self, parent: ProfileView):
        options = [
            discord.SelectOption(label="Yazılım", value="teknoloji"),
            discord.SelectOption(label="Tasarım", value="tasarım"),
            discord.SelectOption(label="Veri / Analiz", value="veri"),
            discord.SelectOption(label="İş & Girişim", value="iş")
        ]
        super().__init__(placeholder="🧭 İlgi alanını seç", min_values=1, max_values=2, options=options)
        self.parent_view = parent

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.user_data["interests"] = self.values
        self.parent_view.clear_items()
        self.parent_view.add_item(SkillSelect(self.parent_view))
        self.parent_view.message = interaction.message
        await interaction.response.edit_message(
            content=f"✅ İlgi alanların: {', '.join(self.values)}\n🧠 Şimdi becerilerini seç",
            view=self.parent_view
        )

class SkillSelect(Select):
    def __init__(self, parent: ProfileView):
        options = [
            discord.SelectOption(label="Analitik Düşünme", value="analiz"),
            discord.SelectOption(label="Yaratıcılık", value="yaratıcılık"),
            discord.SelectOption(label="İletişim", value="iletişim"),
            discord.SelectOption(label="Problem Çözme", value="problem")
        ]
        super().__init__(placeholder="⚡ Güçlü yönlerini seç", min_values=1, max_values=2, options=options)
        self.parent_view = parent

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.user_data["skills"] = self.values
        save_user_profile(
            str(self.parent_view.user.id),
            self.parent_view.user_data["interests"],
            self.parent_view.user_data["skills"],
            recommended_career=None
        )
        self.parent_view.stop()
        await interaction.response.edit_message(
            content=f"✅ Becerilerin: {', '.join(self.values)}\n🚀 Hazırsın! Artık `!oner` komutunu kullanabilirsin.",
            view=None
        )
