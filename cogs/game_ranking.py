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

    # {'msg': 'OK', 'userData': {'couple_nickname': 'らてo', 'bodycolor': 'ffffff', 'nickname': None, 'clan_name': '黒兎', 'self_intro': '撮影モードやらせろ', 'info_title_1': '誕生日', 'info_title_2': 'X・Discord', 'info_title_3': '俺のリア友(やめた人)', 'info_title_4': '', 'info_title_5': '', 'info_title_6': '好きなキャラクター', 'info_title_7': '好きなゲーム', 'info_title_8': '使ってる端末', 'info_data_1': '2010-05-25', 'info_data_2': 'nennneko5787', 'info_data_3': '2月のライオン', 'info_data_4': 'プログラムを書くこと', 'info_data_5': '撮影モード', 'info_data_6': 'ボーカロイド', 'info_data_7': 'com.eoag.iceonline', 'info_data_8': 'iPhone SE 第2世代', 'birthday_secret': False, 'birthday': '1/23/2020 11:32:57 AM', 'textcolor': '', 'textcolor_2': '', 'play_info_rating_1': 980, 'play_info_rating_2': 1059, 'play_info_rating_3': 958, 'play_info_rating_4': 1000, 'play_info_rating_5': 1129, 'play_info_rating_6': 1000, 'rank_1': 24528, 'rank_2': 612, 'rank_3': 14190, 'rank_4': 4929, 'rank_5': 1758, 'rank_6': 11098, 'score': 838227, 'type_0': 825, 'type_1': 86, 'type_10': 114, 'type_11': 20, 'type_12': 121, 'type_13': -1, 'type_14': 4, 'type_15': 119, 'type_16': 0, 'type_17': -1, 'type_18': -1, 'type_19': -1, 'type_20': -1, 'type_2': 901, 'type_3': 0, 'type_4': 0, 'type_5': -1, 'type_6': 285, 'type_7': 112, 'type_8': 910, 'type_9': 467, 'popularity_week': 1, 'popularity_acc': 30, 'popularity_week_rank': 1860, 'popularity_acc_rank': 11171, 'current_season': 25, 'user_index': <userid>}, 'ccd': []}

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            customId = interaction.data["custom_id"]
            customField = customId.split(",")
            if customField[0] == "profile":
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
    async def gameranking(self, interaction: discord.Interaction):
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
                    custom_id=f"profile,{interaction.user.id},{rankerType - 4}",
                )
            )
        elif rankerType == 107:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏪",
                    custom_id=f"profile,{interaction.user.id},{rankerType - 3}",
                )
            )
        elif rankerType > 101:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏪",
                    custom_id=f"profile,{interaction.user.id},{rankerType - 1}",
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
                    custom_id=f"profile,{interaction.user.id},{rankerType + 3}",
                )
            )
        elif rankerType == 107:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏩",
                    custom_id=f"profile,{interaction.user.id},{rankerType + 4}",
                )
            )
        elif rankerType != 111:
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.primary,
                    emoji="⏩",
                    custom_id=f"profile,{interaction.user.id},{rankerType + 1}",
                )
            )

        if editInteraction:
            await interaction.edit_original_response(embeds=embeds, view=view)
        else:
            await interaction.followup.send(embeds=embeds, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(GameRankingCog(bot))
