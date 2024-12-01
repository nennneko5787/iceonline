from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class Discord2UserCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @app_commands.command(
        name="user",
        description=app_commands.locale_str(
            "Discordのユーザーがアカウントをリンクしている場合、プロフィールを表示します。"
        ),
    )
    @app_commands.rename(user=app_commands.locale_str("ユーザー"))
    @app_commands.describe(user=app_commands.locale_str("確認したいユーザー。"))
    async def userCommand(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        row = await Database.pool.fetchrow(
            "SELECT * FROM members WHERE id = $1", user.id
        )
        if not row:
            commands = await self.bot.tree.fetch_commands()
            for cmd in commands:
                if cmd.name == "link":
                    commandId = cmd.id
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "その人はこおり鬼 Online!のアカウントをリンクしていません\nその人がこおり鬼 Online!をやっているのであれば「{command} を使って！」と言ってあげてください。",
                        fmt_arg={"command": f"</link:{commandId}>"},
                    ),
                    interaction.locale,
                ),
                color=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        await self.bot.get_cog("UserInfoCog").responseUserProfile(
            interaction,
            row["nickname"],
            editInteraction=False,
            ephemeral=False,
            isResponsed=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Discord2UserCog(bot))
