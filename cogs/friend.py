from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class FriendsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.data.get("component_type") == 3:
                customId = interaction.data["custom_id"]
                customField = customId.split(",")
                if customField[0] == "friend":
                    await self.bot.get_cog("UserInfoCog").responseUserProfile(
                        interaction,
                        interaction.data["values"][0],
                        editInteraction=False,
                        ephemeral=True,
                    )

    # {'msg': 'OK3', 'getFriendData': {'friend_data': [{'nickname': '白猫さん', 'user_index': 2758412, 'lastdate': '2'}, {'nickname': 'らてo', 'user_index': 4063528, 'lastdate': '139'}, {'nickname': 'イタリア人マーク', 'user_index': 3322819, 'lastdate': '269'}, {'nickname': '탕후루주세요', 'user_index': 3840634, 'lastdate': '2415'}, {'nickname': '玲華', 'user_index': 2280008, 'lastdate': '14267'}], 'block_data': [{'nickname': '米ありません', 'user_index': 3819425}], 'my_index': 0, 'friend_action': 1}}
    @app_commands.command(
        name="friends",
        description=app_commands.locale_str("フレンド一覧を確認します。"),
    )
    @app_commands.rename(type=app_commands.locale_str("リスト"))
    @app_commands.describe(type=app_commands.locale_str("確認したいリスト。"))
    @app_commands.choices(
        type=[
            app_commands.Choice(name=app_commands.locale_str("友達リスト"), value="1"),
            app_commands.Choice(name=app_commands.locale_str("受信リスト"), value="2"),
            app_commands.Choice(name=app_commands.locale_str("送信リスト"), value="3"),
        ]
    )
    async def friendsCommand(
        self, interaction: discord.Interaction, type: app_commands.Choice[str]
    ):
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
            "https://iceonline.azurewebsites.net/Play/GetFriendAndBlock",
            headers={"content-type": "application/json; charset=utf-8"},
            json={"my_index": row["member_id"], "friend_action": type.value},
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
                    app_commands.locale_str("フレンドがいません。"),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
            await interaction.followup.send(embed=embed)
            return

        friends: list[dict] = jsonData.get("getFriendData", {"friend_data": []}).get(
            "friend_data"
        )

        view = discord.ui.View(timeout=None)
        options = []
        for friend in friends:
            nickname = friend.get("nickname")
            lastdate = friend.get("lastdate", None)  # 分単位

            if lastdate:
                lastConnectedDate = datetime.now(ZoneInfo("Asia/Seoul")) - timedelta(
                    minutes=int(lastdate)
                )
            else:
                lastConnectedDate = None

            options.append(
                discord.SelectOption(
                    label=nickname,
                    value=nickname,
                    description=(
                        await self.bot.tree.translator.translate(
                            app_commands.locale_str(
                                "最終接続: {datetime}",
                                fmt_arg={
                                    "datetime": lastConnectedDate.strftime(
                                        "%Y/%m/%d %H:%M:%S"
                                    )
                                },
                            ),
                            interaction.locale,
                        )
                        if lastConnectedDate
                        else ""
                    ),
                )
            )

        view.add_item(discord.ui.Select(custom_id="friend", options=options))

        embed = discord.Embed(
            title=await self.bot.tree.translator.translate(
                app_commands.locale_str("フレンドを選択してください"),
                interaction.locale,
            ),
            colour=discord.Colour.purple(),
        )

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(FriendsCog(bot))
