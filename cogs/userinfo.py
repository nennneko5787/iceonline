import math

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .translator import FreezeTranslator


class UserInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    # {'msg': 'OK', 'userData': {'couple_nickname': 'らてo', 'bodycolor': 'ffffff', 'nickname': None, 'clan_name': '黒兎', 'self_intro': '撮影モードやらせろ', 'info_title_1': '誕生日', 'info_title_2': 'X・Discord', 'info_title_3': '俺のリア友(やめた人)', 'info_title_4': '', 'info_title_5': '', 'info_title_6': '好きなキャラクター', 'info_title_7': '好きなゲーム', 'info_title_8': '使ってる端末', 'info_data_1': '2010-05-25', 'info_data_2': 'nennneko5787', 'info_data_3': '2月のライオン', 'info_data_4': 'プログラムを書くこと', 'info_data_5': '撮影モード', 'info_data_6': 'ボーカロイド', 'info_data_7': 'com.eoag.iceonline', 'info_data_8': 'iPhone SE 第2世代', 'birthday_secret': False, 'birthday': '1/23/2020 11:32:57 AM', 'textcolor': '', 'textcolor_2': '', 'play_info_rating_1': 980, 'play_info_rating_2': 1059, 'play_info_rating_3': 958, 'play_info_rating_4': 1000, 'play_info_rating_5': 1129, 'play_info_rating_6': 1000, 'rank_1': 24528, 'rank_2': 612, 'rank_3': 14190, 'rank_4': 4929, 'rank_5': 1758, 'rank_6': 11098, 'score': 838227, 'type_0': 825, 'type_1': 86, 'type_10': 114, 'type_11': 20, 'type_12': 121, 'type_13': -1, 'type_14': 4, 'type_15': 119, 'type_16': 0, 'type_17': -1, 'type_18': -1, 'type_19': -1, 'type_20': -1, 'type_2': 901, 'type_3': 0, 'type_4': 0, 'type_5': -1, 'type_6': 285, 'type_7': 112, 'type_8': 910, 'type_9': 467, 'popularity_week': 1, 'popularity_acc': 30, 'popularity_week_rank': 1860, 'popularity_acc_rank': 11171, 'current_season': 25, 'user_index': 1955121}, 'ccd': []}

    @app_commands.command(
        name="profile",
        description=app_commands.locale_str(
            "ニックネームからユーザーのプロフィールを取得します。"
        ),
    )
    async def profile(self, interaction: discord.Interaction, nickname: str):
        await interaction.response.defer()
        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/GetUserInfo",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"nickname": nickname, "season": "-1"},
        )
        if response.status_code != 200:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("ユーザーの取得に失敗しました。"),
                    interaction.locale,
                )
            )
            await interaction.followup.send(embed=embed)
            return
        jsonData: dict = response.json()
        if jsonData.get("msg", "NG") != "OK":
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "そのニックネームのユーザーは存在しません。"
                    ),
                    interaction.locale,
                )
            )
            await interaction.followup.send(embed=embed)
            return
        userData: dict = jsonData["userData"]
        embed = (
            discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "{nickname} のプロフィール", fmt_arg={"nickname": nickname}
                    ),
                    interaction.locale,
                ),
                description=userData.get("self_intro", ""),
                colour=discord.Colour.from_str(f'#{userData.get("bodycolor", "")}'),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("レベル"),
                    interaction.locale,
                ),
                value=math.ceil(userData.get("score", 0) / 1000),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("カップル"),
                    interaction.locale,
                ),
                value=userData.get("couple_nickname", ""),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クラン"),
                    interaction.locale,
                ),
                value=userData.get("clan_name", ""),
            )
        )

        infoLocale = await self.bot.tree.translator.translate(
            app_commands.locale_str("情報"),
            interaction.locale,
        )

        if not userData.get("birthday_secret", False):
            embed.add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("誕生日"),
                    interaction.locale,
                ),
                value=userData.get("birthday", ""),
            )

        for i in range(1, 8):
            if (userData.get(f"info_title_{i}", "") == "") and (
                userData.get(f"info_data_{i}", "") == ""
            ):
                continue

            if userData.get(f"info_title_{i}", "") == "":
                info = f"{infoLocale}{i}"
            else:
                info = userData.get(f"info_title_{i}", "")

            embed.add_field(
                name=info,
                value=userData.get(f"info_data_{i}", ""),
            )

        embed.add_field(name="こおり鬼モード", value=f'{userData.get("play_info_rating_1", 1000)} ({userData.get("rank_1", 1000)}位)').add_field(name="チームバトルモード", value=f'{userData.get("play_info_rating_2", 1000)} ({userData.get("rank_2", 1000)}位)').add_field(name="1対1モード", value=f'{userData.get("play_info_rating_3", 1000)} ({userData.get("rank_3", 1000)}位)').add_field(name="旗取りモード", value=f'{userData.get("play_info_rating_4", 1000)} ({userData.get("rank_4", 1000)}位)').add_field(name="墜落モード", value=f'{userData.get("play_info_rating_5", 1000)} ({userData.get("rank_5", 1000)}位)').add_field(name="こおり鬼(チーム)", value=f'{userData.get("play_info_rating_6", 1000)} ({userData.get("rank_6", 1000)}位)')
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfoCog(bot))
