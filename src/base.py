BOT_VERSION = "1.1.0"

from dotenv import load_dotenv
load_dotenv()

from guilded.ext.commands import Bot, when_mentioned_or, Context
from core.embeds import EMBED_STANDARD
from guilded.ext import commands

import guilded
import asyncio
import config

client_features = guilded.ClientFeatures(
    experimental_event_style=True,
    official_markdown=True
)

bot = Bot(
    command_prefix=when_mentioned_or(config.DEFAULT_PREFIX),
    features=client_features
)

async def send_shutdown(ctx):
    link = guilded.utils.link(
        title="this post",
        link="https://www.guilded.gg/server-guard/groups/D57rgP7z/channels/bd1c327a-44e4-4c63-8eda-3c9a5b417c19/announcements/16nGrG1y"
    )
    cg_link = guilded.utils.link(
        title="here",
        link="https://discord.gg/Savkc9RvPw"
    )
    await ctx.reply(embed=EMBED_STANDARD(
        title="Server Guard has shutdown.",
        description=f"Server Guard will not be responding to any commands. Please refer to {link} for more information.\n\nIt has been fun maintaining this bot, goodbye!\n\n- Reapimus"
    ))
    await (isinstance(ctx, guilded.Message) and ctx.channel.send or ctx.send)(embed=EMBED_STANDARD(
        title="Alternative chatting app",
        description=f"I am also now working on an alternative chatting app with some other developers! anyone interested can find an invite to its Discord server {cg_link}!"
    ))

@bot.event
async def on_ready():
    await bot.set_status(
        emote=guilded.Object(90002078),
        content="Server Guard has shutdown."
    )

@bot.event
async def on_message(event: guilded.MessageEvent):
    await bot.process_commands(event.message)
    if event.message.content.strip() == bot.user.mention:
        await send_shutdown(event.message)

@bot.event
async def on_command(ctx: Context):
    await send_shutdown(ctx)

@bot.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, commands.CommandNotFound):
        await send_shutdown(ctx)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.run(config.TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())