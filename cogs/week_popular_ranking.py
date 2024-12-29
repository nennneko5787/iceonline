import math
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands


class WeekPopularRankingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            customId = interaction.data["custom_id"]
            customField = customId.split(",")
            if customField[0] == "wpranking":
                if interaction.user.id != int(customField[1]):
                    embed = discord.Embed(
                        title=await self.bot.tree.translator.translate(
                            app_commands.locale_str(
                                "これはあなたが表示させたランキングではありません！"
                            ),
                            interaction.locale,
                        ),
                        colour=discord.Colour.red(),
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                await self.responseGameRanking(
                    interaction,
                    int(customField[2]),
                    editInteraction=True,
                )

    @app_commands.command(
        name="wpranking",
        description=app_commands.locale_str("週間人気度ランキングを確認します。"),
    )
    @app_commands.rename(
        country=app_commands.locale_str("サーバー"),
    )
    @app_commands.choices(
        country=[
            app_commands.Choice(name=app_commands.locale_str("日本"), value="1100"),
            app_commands.Choice(name=app_commands.locale_str("韓国"), value="1000"),
        ],
    )
    async def weekPopularRankingCommand(
        self, interaction: discord.Interaction, country: str
    ):
        await self.responseGameRanking(interaction, country)

    async def responseGameRanking(
        self,
        interaction: discord.Interaction,
        mode: str,
        page: int = 3,
        *,
        editInteraction: bool = False,
    ):
        await interaction.response.defer()
        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/GetRankerCostumes",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"ranker_page": str(page), "ranker_type": mode},
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
        if jsonData.get("user_data", None) is None:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("サーバーとの通信に失敗しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        users: list[str] = jsonData.get("user_data", None)

        embeds = []

        for index, user in enumerate(users, start=1):
            # ランキング内のユーザーデータは少し特殊
            # "\xe3\x83\x96\xe3\x83\xad\xe3\x83\xb3\xe3\x82\xba/164,59,-1,0,0,-1,-1,502,681,-1,-1,-1,112,-1,-1,-1,-1,-1,-1,-1/000002/20235/-1"
            # / で区切ることができる
            # 1番目はニックネーム、2番目はコスチュームデータ、3番目は背景色、4番目はスコア、5番目は何に使うかよくわからないフラグ
            nickname, costumeData, backgroundColor, score, flag = user.split("/")
            embeds.append(
                discord.Embed(
                    title=await self.bot.tree.translator.translate(
                        app_commands.locale_str(
                            "{rank}位", fmt_arg={"rank": (page - 3) + index}
                        ),
                        interaction.locale,
                    ),
                    description=nickname,
                    colour=discord.Colour.from_str(f"#{backgroundColor}"),
                ).add_field(
                    name=await self.bot.tree.translator.translate(
                        app_commands.locale_str("スコア"),
                        interaction.locale,
                    ),
                    value=score,
                )
            )

        view = discord.ui.View(timeout=None)
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.primary,
                emoji="⏪",
                custom_id=f"wpranking,{interaction.user.id},{page - 3}",
                disabled=(page <= 3),
            )
        )
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                label=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "ページ {page} / {mode}",
                        fmt_arg={
                            "page": (page // 3),
                            "mode": self.bot.tree.translator.translate(
                                app_commands.locale_str("週間人気度")
                            ),
                        },
                    ),
                    interaction.locale,
                ),
                disabled=True,
            )
        )
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.primary,
                emoji="⏩",
                custom_id=f"wpranking,{interaction.user.id},{page + 3}",
            )
        )

        if editInteraction:
            await interaction.edit_original_response(embeds=embeds, view=view)
        else:
            await interaction.followup.send(embeds=embeds, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(WeekPopularRankingCog(bot))
