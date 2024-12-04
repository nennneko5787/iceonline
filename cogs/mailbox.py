from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class MailBoxCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    async def detectBosang(self, index: int, locale: discord.Locale):
        match (index):
            case 0:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("ゴールド"), locale
                )
            case 1:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("アイス"), locale
                )
            case 2:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("マイレージ"), locale
                )
            case 3:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("キューブ"), locale
                )
            case 50:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("高級箱"), locale
                )
            case _:
                return await self.bot.tree.translator.translate(
                    app_commands.locale_str("不明"), locale
                )

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.data.get("component_type") == 3:
                customId = interaction.data["custom_id"]
                customField = customId.split(",")
                if customField[0] == "mailbox":
                    selectField = interaction.data["values"][0].split(",")
                    mailIndex: int = int(selectField[0])
                    _bosangType: int = int(selectField[1])

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
                                app_commands.locale_str(
                                    "アカウントがリンクされていません！"
                                ),
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
                        "https://iceonline.azurewebsites.net/User/GetMailBosang",
                        headers={"content-type": "application/json; charset=utf-8"},
                        json={"user_index": row["member_id"], "mail_index": mailIndex},
                    )
                    if response.status_code != 200:
                        embed = discord.Embed(
                            title=await self.bot.tree.translator.translate(
                                app_commands.locale_str(
                                    "サーバーとの通信に失敗しました。"
                                ),
                                interaction.locale,
                            ),
                            colour=discord.Colour.red(),
                        )
                        await interaction.followup.send(embed=embed)
                        return

                    jsonData: dict = response.json()
                    if not "OK" in jsonData.get("msg", "NG"):
                        embed = discord.Embed(
                            title=await self.bot.tree.translator.translate(
                                app_commands.locale_str(
                                    "サーバーとの通信に失敗しました。"
                                ),
                                interaction.locale,
                            ),
                            colour=discord.Colour.red(),
                        )
                        await interaction.followup.send(embed=embed)
                        return

                    bosangType: int = jsonData.get("bosang_type")
                    bosangValue: int = jsonData.get("bosang_value")

                    embed = discord.Embed(
                        title=await self.bot.tree.translator.translate(
                            app_commands.locale_str(
                                "{bosang} を受け取りました！",
                                fmt_arg={
                                    "bosang": f"{self.detectBosang(_bosangType, interaction.locale)} ({_bosangType})"
                                },
                            ),
                            interaction.locale,
                        ),
                        description=await self.bot.tree.translator.translate(
                            app_commands.locale_str(
                                "獲得したアイテムはゲーム内で確認してください。",
                            ),
                            interaction.locale,
                        ),
                        colour=discord.Colour.red(),
                    )
                    await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="mailbox",
        description=app_commands.locale_str("届いているメールの一覧を確認します。"),
    )
    async def mailBoxCommand(self, interaction: discord.Interaction):
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
            "https://iceonline.azurewebsites.net/User/GetMailList",
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
        if not "OK" in jsonData.get("msg", "NG"):
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("サーバーとの通信に失敗しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        mailbox: list[dict] = jsonData.get(
            "getMailResultData", {"mail_list_data": []}
        ).get("mail_list_data")

        if len(mailbox) <= 0:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("届いているメールはありません。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        view = discord.ui.View(timeout=None)
        options = []
        for mail in mailbox:
            mailIndex = mail.get("mail_index")
            bosangType = mail.get("bosang_type")
            bosangValue = mail.get("bosang_value")
            bosangText = mail.get("bosang_text")
            endDate = datetime.strptime(
                mail.get("end_date", "Jan  1 1970  0:00AM"), "%b  %d %Y  %I:%M%p"
            ).replace(tzinfo=ZoneInfo("Asia/Seoul"))

            options.append(
                discord.SelectOption(
                    label=bosangText,
                    value=f"{mailIndex},{bosangType}",
                    description=(
                        await self.bot.tree.translator.translate(
                            app_commands.locale_str(
                                "受け取り期限: {datetime}",
                                fmt_arg={
                                    "datetime": endDate.strftime("%Y/%m/%d %H:%M:%S")
                                },
                            ),
                            interaction.locale,
                        )
                    ),
                )
            )

        view.add_item(discord.ui.Select(custom_id="mailbox", options=options))

        embed = discord.Embed(
            title=await self.bot.tree.translator.translate(
                app_commands.locale_str("メールボックス"),
                interaction.locale,
            ),
            colour=discord.Colour.purple(),
        )

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MailBoxCog(bot))
