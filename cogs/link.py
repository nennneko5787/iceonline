import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class AccountLinkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @app_commands.command(
        name="link", description=app_commands.locale_str("アカウントをリンクします。")
    )
    @app_commands.rename(
        memberId=app_commands.locale_str("会員番号"),
        nickname=app_commands.locale_str("ニックネーム"),
    )
    @app_commands.describe(
        memberId=app_commands.locale_str(
            "リンクしたいプレイヤーの会員番号(設定から確認できます)"
        ),
        nickname=app_commands.locale_str("リンクしたいプレイヤーのニックネーム"),
    )
    async def linkCommand(
        self, interaction: discord.Interaction, memberId: int, nickname: str
    ):
        await interaction.response.defer(ephemeral=True)
        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/GetUserInfo",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"nickname": nickname, "season": "-1"},
        )
        if response.status_code != 200:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("サーバーとの通信に失敗しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        jsonData: dict = response.json()
        if jsonData.get("msg", "NG") != "OK":
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("会員番号かニックネームが間違っています。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        userData: dict = jsonData["userData"]
        if userData.get("user_index", None) != memberId:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("会員番号かニックネームが間違っています。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        await Database.pool.execute(
            """
                INSERT INTO members (id, member_id, nickname)
                VALUES ($1, $2, $3)
                ON CONFLICT (id)
                DO UPDATE SET
                    member_id = EXCLUDED.member_id,
                    nickname = EXCLUDED.nickname
            """,
            interaction.user.id,
            memberId,
            nickname,
        )

        embed = discord.Embed(
            title=await self.bot.tree.translator.translate(
                app_commands.locale_str("アカウントをリンクしました！"),
                locale=interaction.locale,
            ),
            colour=discord.Colour.green(),
        )
        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AccountLinkCog(bot))
