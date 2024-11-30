import asyncio
import os
from contextlib import asynccontextmanager

import discord
import dotenv
from discord.ext import commands, tasks
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from cogs.translator import FreezeTranslator
from cogs.database import Database

dotenv.load_dotenv()

discord.utils.setup_logging()

bot = commands.Bot("iceonline#", intents=discord.Intents.default())


@tasks.loop(seconds=20)
async def precenseLoop():
    appInfo = await bot.application_info()
    game = discord.Game(
        f"/help | {len(bot.guilds)} servers | {appInfo.approximate_user_install_count} users"
    )
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.event
async def on_ready():
    precenseLoop.start()


@bot.event
async def setup_hook():
    await bot.tree.set_translator(FreezeTranslator())
    await bot.load_extension("cogs.userinfo")
    await bot.load_extension("cogs.link")
    await bot.load_extension("cogs.quick")
    await bot.load_extension("cogs.clan")
    await bot.load_extension("cogs.edit")
    await bot.load_extension("cogs.admin")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    asyncio.create_task(bot.start(os.getenv("discord")))
    yield
    async with asyncio.timeout(60):
        await Database.pool.close()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
