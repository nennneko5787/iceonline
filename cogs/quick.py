from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class AccountLinkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    async def detectMode(self, index: int, locale: discord.Locale):
        match (index):
            case 0:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼モード")
                )
            case 1:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("チームバトルモード")
                )
            case 2:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("(古い)1対1モード")
                )
            case 3:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("1対1モード")
                )
            case 5:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("旗取りモード")
                )
            case 7:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("墜落モード")
                )
            case 8:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("こおり鬼(チーム)")
                )
            case 9:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("巨人モード")
                )
            case 10:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("マラソンモード")
                )
            case 11:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("不明")
                )
            case 12:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("撮影モード")
                )
            case 13:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("占領モード")
                )
            case 14:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("警察と泥棒モード")
                )
            case 15:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("墜落モード(1vs1)")
                )
            case 16:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("マフィアモード")
                )
            case 17:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("爆弾モード")
                )
            case 19:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("墜落モード(個展)")
                )
            case 21:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("かくれんぼモード")
                )
            case 22:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("迷路モード")
                )
            case 23:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("不明")
                )
            case 24:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("崩壊モード")
                )
            case 25:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("ひっくり返しモード")
                )
            case 29:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("だるまさんがころんだモード")
                )
            case 30:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("薄氷モード")
                )
            case 31:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("宝探しモード")
                )
            case 32:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("迷路エスケープモード")
                )
            case 33:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("クイズモード")
                )
            case 35:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("チームデスマッチモード")
                )
            case 38:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("雪玉を避けるモード")
                )
            case 40:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("雪合戦モード")
                )
            case 41:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("超能力こおり鬼モード")
                )
            case 42:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("フリーズボールモード")
                )
            case 44:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("王騎士モード")
                )
            case 45:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("変身かくれんぼモード")
                )
            case _:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("不明")
                )

    # {"current_mode_index":13,"left_sec":148,"msg":"OK"}
    @app_commands.command(
        name="quickmatch",
        description=app_commands.locale_str(
            "クイックマッチの現在の情報を取得します。アカウントをリンクする必要があります。"
        ),
    )
    async def quickMatchCommand(self, interaction: discord.Interaction):
        await interaction.response.defer()
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
            )
            await interaction.followup.send(embed=embed)
            return

        response = await self.client.post(
            "https://iceonline.azurewebsites.net/User/GetUserInfo",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"user_index": row["member_id"]},
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
                    app_commands.locale_str("サーバーとの通信に失敗しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        modeIndex = jsonData.get("current_mode_index", 0)
        leftSec = jsonData.get("left_sec", 0)

        mode = f"{await self.detectMode(modeIndex, interaction.locale)} ({modeIndex})"

        switchTime = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(seconds=leftSec)

        embed = discord.Embed(
            title=await self.bot.tree.translator.translate(
                app_commands.locale_str("現在のクイックマッチの情報")
            ),
            description=await self.bot.tree.translator.translate(
                app_commands.locale_str(
                    "現在のモード: {mode}\n次のモード切り替えの時間: {switchTime}",
                    fmt_arg={
                        "mode": mode,
                        "switchTime": discord.utils.format_dt(switchTime, style="R"),
                    },
                )
            ),
            colour=discord.Colour.blurple(),
        )

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(AccountLinkCog(bot))
