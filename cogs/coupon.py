from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class CouponCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @app_commands.command(
        name="coupon",
        description=app_commands.locale_str("クーポンを使用します。"),
    )
    @app_commands.rename(coupon="クーポン")
    @app_commands.describe(coupon="使用するクーポン。")
    async def couponCommand(self, interaction: discord.Interaction, coupon: str):
        await interaction.response.defer(ephemeral=True)
        row = await Database.pool.fetchrow(
            "SELECT * FROM members WHERE id = $1", interaction.user.id
        )
        if not row:
            commands = await self.bot.tree.fetch_commands()
            for cmd in commands:
                if cmd.name == "link":
                    commandId = cmd.id
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("アカウントがリンクされていません！"),
                    interaction.locale,
                ),
                description=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "{cmd}を使用して、アカウントをリンクしてください。",
                        fmt_arg={"cmd": f"</link:{commandId}>"},
                    ),
                    interaction.locale,
                ),
                color=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/UseCoupon_2",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"user_index": "1955121", "coupon_name": coupon},
        )
        if response.status_code != 200:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("サーバーとの通信に失敗しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        result = response.text
        if "NO" in result:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "既に使用されているか、クーポンがありません。"
                    ),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title=await self.bot.tree.translator.translate(
                app_commands.locale_str("クーポンを使用しました。"),
                interaction.locale,
            ),
            colour=discord.Colour.blurple(),
        )

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CouponCog(bot))
