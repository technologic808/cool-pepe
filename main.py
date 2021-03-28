import discord
import os
import random
from replit import db
import pepe_server
import io
import asyncio
import asyncpraw
import aiohttp
import sys

# Gets Discord Client
discord_client = discord.Client()

# Gets Reddit API wrapper
reddit = asyncpraw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="dank meme by technologic",
)


# Gets the meme url from reddit
async def get_meme_url(subreddit, _time):
    subreddit = await reddit.subreddit(subreddit)
    memes = []
    async for submission in subreddit.top(_time):
        url = submission.url
        if url.endswith(('.jpg', '.png', '.jpeg')):
            memes.append(url)
    return random.choice(memes)


# Posts the meme on the channel passed
async def post_dank_meme(channel, subreddit, _time):
    url = await get_meme_url(subreddit, _time)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await channel.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            try:
                await channel.send(file=discord.File(data, 'cool_image.png'))
            except:
                print("Exception: ", sys.exc_info()[0])


# Posts a meme every interval specified
async def auto_post(channel,  subreddit, _time, interval_in_seconds):
    while True:
        await post_dank_meme(channel,  subreddit, _time)
        await asyncio.sleep(interval_in_seconds)


# Prints a message on initialization
@discord_client.event
async def on_ready():
    print("We have logged in as {0.user}\n".format(discord_client))


# Processes all messages posted on the discord
@discord_client.event
async def on_message(message):
    # Ignores its own messages
    if message.author == discord_client.user:
        return

    # Posts a meme
    if message.content.startswith("-meme"):
        await post_dank_meme(message.channel, "dankmemes", "day")


# Keeps the server alive somehow?
pepe_server.keep_alive()

# Runs the discord client
discord_client.run(os.getenv("DISCORD_TOKEN"))
