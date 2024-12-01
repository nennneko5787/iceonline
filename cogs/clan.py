from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands


class ClanInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    # {"msg":"OK","getClanInfoData":{"clan_user_data":[{"nickname":"Xx\xe3\x81\xad\xe3\x82\x93\xe3\x81\xad\xe3\x81\x93xX","clan_grade":100},{"nickname":"\xe3\x82\x89\xe3\x81\xa6o","clan_grade":50},{"nickname":"\xe3\x81\xb7\xe3\x81\xa1\xe3\x82\x8d\xe3\x81\xa1\xe5\xa4\xaa\xe9\x83\x8e","clan_grade":0},{"nickname":"\xe3\x81\xbf\xe3\x82\x93\xe3\x81\xa8\xe3\x81\xae\xe3\x82\xb5\xe3\x83\x96\xe5\x9e\xa2","clan_grade":0}],"clan_index":301765,"clan_ranking":7250,"clan_mark_number":9,"clan_mark_number_2":27,"clan_level":1,"clan_score":1000,"clan_name":"\xe9\xbb\x92\xe5\x85\x8e","clan_detail":"\xe3\x82\x88\xe3\x82\x8d\xe3\x81\x97\xe3\x81\x8f","clan_create_date":"11/27/2024 11:06:35 PM","clan_condition_level":1,"clan_condition_vs":true,"clan_condition_join":true,"clan_condition_mode_1":0,"clan_condition_mode_2":0,"clan_condition_mode_3":0,"clan_condition_mode_4":0,"clan_condition_mode_5":0,"clan_condition_mode_6":0,"clan_condition_chat_2":"url"}}

    def rateToString(self, late: int):
        match late:
            case 0:
                return "Bronze"
            case 1:
                return "Silver 4"
            case 2:
                return "Silver 3"
            case 3:
                return "Silver 2"
            case 4:
                return "Silver 1"
            case 5:
                return "Gold 5"
            case 6:
                return "Gold 4"
            case 7:
                return "Gold 3"
            case 8:
                return "Gold 2"
            case 9:
                return "Gold 1"
            case 10:
                return "Platinum 5"
            case 11:
                return "Platinum 4"
            case 12:
                return "Platinum 3"
            case 13:
                return "Platinum 2"
            case 14:
                return "Platinum 1"
            case 15:
                return "Diamond 5"
            case 16:
                return "Diamond 4"
            case 17:
                return "Diamond 3"
            case 18:
                return "Diamond 2"
            case 19:
                return "Diamond 1"
            case 20:
                return "Enter Master"
            case 21:
                return "Semi Master"
            case 22:
                return "Master"
            case 23:
                return "Grand Master"
            case 24:
                return "King Slayer"
            case 25:
                return "King"

    @app_commands.command(
        name="clan",
        description=app_commands.locale_str("クランの情報を確認します。"),
    )
    @app_commands.rename(clanname=app_commands.locale_str("クラン名"))
    @app_commands.describe(clanname=app_commands.locale_str("クランの名前"))
    async def clanCommand(self, interaction: discord.Interaction, clanname: str):
        await interaction.response.defer()
        response = await self.client.post(
            "https://iceonline.azurewebsites.net/Clan/GetClanInfo_2",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"clan_name": clanname},
        )
        jsonData: dict = response.json()
        if jsonData.get("msg", "NG") != "OK":
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("その名前のクランは存在しません。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        clanData: dict = jsonData["getClanInfoData"]

        members: list[dict] = clanData.get("clan_user_data", [])
        rank = clanData.get("clan_ranking", 99999)
        maxMember = 20 + (clanData.get("clan_level", 1) - 1)
        score = clanData.get("clan_score", 0)
        normalizedName = clanData.get("clan_name", clanname)
        detail = clanData.get("clan_detail", "")
        createdAt = datetime.strptime(
            clanData.get("clan_create_date", "1/1/1970 00:00:00 AM"),
            "%m/%d/%Y %I:%M:%S %p",
        ).replace(tzinfo=ZoneInfo("Asia/Seoul"))

        conditionLevel = clanData.get("clan_condition_level", 1)
        conditionVs = clanData.get("clan_condition_vs", False)
        conditionJoin = clanData.get("clan_condition_join", False)

        freezeTagRankLimit = clanData.get("clan_condition_mode_1", False)
        teamBattleRankLimit = clanData.get("clan_condition_mode_2", False)
        oneVsOneRankLimit = clanData.get("clan_condition_mode_3", False)
        stealFlagRankLimit = clanData.get("clan_condition_mode_4", False)
        fallingRankLimit = clanData.get("clan_condition_mode_5", False)
        teamFreezeTagRankLimit = clanData.get("clan_condition_mode_6", False)

        if clanData.get("clan_condition_chat_2", "url") == "url":
            interViewURL = None
        else:
            interViewURL = clanData.get("clan_condition_chat_2", "url")

        embed = (
            discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "{clanname} クランの情報", fmt_arg={"clanname": normalizedName}
                    ),
                    interaction.locale,
                ),
                description=detail,
                colour=discord.Colour.blurple(),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クラン順位"),
                    interaction.locale,
                ),
                value=await self.bot.tree.translator.translate(
                    app_commands.locale_str("{rank}位", fmt_arg={"rank": rank}),
                    interaction.locale,
                ),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クラン人員"), interaction.locale
                ),
                value=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "{member}人 (最大{maxMember}人)",
                        fmt_arg={"member": len(members), "maxMember": maxMember},
                    ),
                    interaction.locale,
                ),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クラン点数"),
                    interaction.locale,
                ),
                value=await self.bot.tree.translator.translate(
                    app_commands.locale_str("{score}点", fmt_arg={"score": score}),
                    interaction.locale,
                ),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クラン作成日"),
                    interaction.locale,
                ),
                value=discord.utils.format_dt(createdAt, "f"),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("レベル条件"),
                    interaction.locale,
                ),
                value=conditionLevel,
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("クランゲーム進行"),
                    interaction.locale,
                ),
                value=":o:" if conditionVs else ":x:",
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("参加可能"),
                    interaction.locale,
                ),
                value=":o:" if conditionJoin else ":x:",
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼モード ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(freezeTagRankLimit),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("チームバトルモード ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(teamBattleRankLimit),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("1対1モード ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(oneVsOneRankLimit),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("旗取りモード ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(stealFlagRankLimit),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("墜落モード ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(fallingRankLimit),
            )
            .add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼(チーム) ランク条件"),
                    interaction.locale,
                ),
                value=self.rateToString(teamFreezeTagRankLimit),
            )
        )

        if interViewURL:
            embed.add_field(
                name=await self.bot.tree.translator.translate(
                    app_commands.locale_str("面接用チャット"), interaction.locale
                ),
                value=interViewURL,
            )

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ClanInfoCog(bot))
