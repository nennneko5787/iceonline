import httpx
import discord
from discord import app_commands
from discord.ext import commands

from .database import Database


class EditProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = httpx.AsyncClient()

    # /User/ManageUserIntroduce
    # {"user_index":"<ユーザーID>","manage_type":"50","detail":"\\u64AE\\u5F71\\u30E2\\u30FC\\u30C9\\u5E38\\u99D0\\u3055\\u305B\\u308D"}
    # manage_type の対応表
    # 一言: 50
    # 上から順に
    # 1: 11
    # 2: 12
    # 3: 13
    # 4: 14
    # 5: 15
    # 6: 16
    # 7: 17
    # 8: 18
    # 誕生日の表示 / 非表示切り替え: 101 detailは空欄(not null)

    # いつも思うんだけどuser_indexだけで変えられるとか欠陥かよ...

    @app_commands.command(name="edit", description="プロフィールを編集します。")
    @app_commands.rename(
        introduction=app_commands.locale_str("一言紹介"),
        showbirthday=app_commands.locale_str("誕生日の表示を切り替える"),
        field1=app_commands.locale_str("情報1"),
        field2=app_commands.locale_str("情報2"),
        field3=app_commands.locale_str("情報3"),
        field4=app_commands.locale_str("情報4"),
        field5=app_commands.locale_str("情報5"),
        field6=app_commands.locale_str("情報6"),
        field7=app_commands.locale_str("情報7"),
        field8=app_commands.locale_str("情報8"),
        field1value=app_commands.locale_str("情報1の内容"),
        field2value=app_commands.locale_str("情報2の内容"),
        field3value=app_commands.locale_str("情報3の内容"),
        field4value=app_commands.locale_str("情報4の内容"),
        field5value=app_commands.locale_str("情報5の内容"),
        field6value=app_commands.locale_str("情報6の内容"),
        field7value=app_commands.locale_str("情報7の内容"),
        field8value=app_commands.locale_str("情報8の内容"),
    )
    @app_commands.describe(
        introduction=app_commands.locale_str("一言紹介"),
        showbirthday=app_commands.locale_str("誕生日の表示を切り替えるかどうか"),
        field1=app_commands.locale_str("情報1"),
        field2=app_commands.locale_str("情報2"),
        field3=app_commands.locale_str("情報3"),
        field4=app_commands.locale_str("情報4"),
        field5=app_commands.locale_str("情報5"),
        field6=app_commands.locale_str("情報6"),
        field7=app_commands.locale_str("情報7"),
        field8=app_commands.locale_str("情報8"),
        field1value=app_commands.locale_str("情報1の内容"),
        field2value=app_commands.locale_str("情報2の内容"),
        field3value=app_commands.locale_str("情報3の内容"),
        field4value=app_commands.locale_str("情報4の内容"),
        field5value=app_commands.locale_str("情報5の内容"),
        field6value=app_commands.locale_str("情報6の内容"),
        field7value=app_commands.locale_str("情報7の内容"),
        field8value=app_commands.locale_str("情報8の内容"),
    )
    @app_commands.choices(
        showbirthday=[
            app_commands.Choice(name=app_commands.locale_str("はい"), value=True),
            app_commands.Choice(name=app_commands.locale_str("いいえ"), value=False),
        ]
    )
    async def edit(
        self,
        interaction: discord.Interaction,
        introduction: str = None,
        showbirthday: app_commands.Choice[int] = None,
        field1: str = None,
        field2: str = None,
        field3: str = None,
        field4: str = None,
        field5: str = None,
        field6: str = None,
        field7: str = None,
        field8: str = None,
        field1value: str = None,
        field2value: str = None,
        field3value: str = None,
        field4value: str = None,
        field5value: str = None,
        field6value: str = None,
        field7value: str = None,
        field8value: str = None,
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
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        updated = False

        if introduction:
            response = await self.client.post(
                "https://iceonline.azurewebsites.net/User/ManageUserIntroduce",
                headers={"content-type": "application/json; charset=utf-8"},
                json={
                    "user_index": row["member_id"],
                    "manage_type": "50",
                    "detail": introduction,
                },
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
            updated = True

        if showbirthday:
            response = await self.client.post(
                "https://iceonline.azurewebsites.net/User/ManageUserIntroduce",
                headers={"content-type": "application/json; charset=utf-8"},
                json={
                    "user_index": row["member_id"],
                    "manage_type": "101",
                    "detail": "",
                },
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
            updated = True

        localVars = locals()

        for index in range(1, 9):
            field = localVars.get(f"field{index}")
            if field:
                response = await self.client.post(
                    "https://iceonline.azurewebsites.net/User/ManageUserIntroduce",
                    headers={"content-type": "application/json; charset=utf-8"},
                    json={
                        "user_index": row["member_id"],
                        "manage_type": f"{index}",
                        "detail": field,
                    },
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
                updated = True

        for index in range(1, 9):
            fieldValue = localVars.get(f"field{index}values")
            if fieldValue:
                response = await self.client.post(
                    "https://iceonline.azurewebsites.net/User/ManageUserIntroduce",
                    headers={"content-type": "application/json; charset=utf-8"},
                    json={
                        "user_index": row["member_id"],
                        "manage_type": f"1{index}",
                        "detail": fieldValue,
                    },
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
                updated = True

        if updated:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str("プロフィールを編集しました。"),
                    interaction.locale,
                ),
                colour=discord.Colour.green(),
            )
        else:
            embed = discord.Embed(
                title=await self.bot.tree.translator.translate(
                    app_commands.locale_str(
                        "プロフィールは何一つ編集されませんでした。"
                    ),
                    interaction.locale,
                ),
                colour=discord.Colour.red(),
            )
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(EditProfileCog(bot))
