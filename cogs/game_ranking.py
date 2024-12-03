import math
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands


class GameRankingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            customId = interaction.data["custom_id"]
            customField = customId.split(",")
            if customField[0] == "gameranking":
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

    async def rankerTypeToString(self, rankerType: int, locale: discord.Locale):
        match rankerType:
            case 101:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼モード"), locale
                )
            case 102:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("チームバトルモード"), locale
                )
            case 103:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("1対1モード"), locale
                )
            case 104:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("旗取りモード"), locale
                )
            case 107:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("墜落モード"), locale
                )
            case 111:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼(チーム)"), locale
                )
            case _:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("不明"), locale
                )

    @app_commands.command(
        name="gameranking",
        description=app_commands.locale_str("各モードのランキングを確認します。"),
    )
    async def gameRankingCommand(self, interaction: discord.Interaction):
        await self.responseGameRanking(interaction)

    async def responseGameRanking(
        self,
        interaction: discord.Interaction,
        rankerType: int = 101,
        *,
        editInteraction: bool = False,
    ):
        await interaction.response.defer()
        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/GetRankerCostumes",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"ranker_page": "3", "ranker_type": f"{rankerType}"},
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
                        app_commands.locale_str("{rank}位", fmt_arg={"rank": index}),
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
        if rankerType == 111:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏪",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType - 4}",
                )
            )
        elif rankerType == 107:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏪",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType - 3}",
                )
            )
        elif rankerType > 101:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏪",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType - 1}",
                )
            )
        view.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                label=await self.rankerTypeToString(rankerType, interaction.locale),
                disabled=True,
            )
        )
        if rankerType == 104:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏩",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType + 3}",
                )
            )
        elif rankerType == 107:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏩",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType + 4}",
                )
            )
        elif rankerType != 111:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏩",
                    custom_id=f"gameranking,{interaction.user.id},{rankerType + 1}",
                )
            )

        if editInteraction:
            await interaction.edit_original_response(embeds=embeds, view=view)
        else:
            await interaction.followup.send(embeds=embeds, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(GameRankingCog(bot))