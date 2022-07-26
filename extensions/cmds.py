from cv2 import add
from twitchio.ext import commands
import json

from utils import resume_track, search, now_playing, prev_track, skip_track, _volume, pause_track, add_track, add_queue


with open("data.json", "r", encoding="utf-8") as f:
    spotify_data = json.load(f)


class spotify_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add", aliases=["add_track", "add_song", "play"])
    async def play_track(self, ctx, track: str):
        try:
            add_track(playlist_id=spotify_data["spotify"]["playlist_id"], track_id=track)
            await ctx.send(f"{ctx.author.name}, Added your track ( {search(track)} ) to playlist")
            await ctx.author.send(f"{ctx.author.name}, track '{track}' added to playlist for {ctx.author.channel.name}")
        except Exception as e:
            err = str(e)
            if "Premium required" in err:
                await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
            else:
                print(e)

    @commands.command(name="search", aliases=["s"])
    async def search(self, ctx, *, query):
        items = search(query)
        await ctx.send(f"Search results for '{query}': {items}")

    @commands.command(name="song", aliases=["nowplaying", "np"])
    async def now_playing(self, ctx):
        await ctx.send(f"Now playing: {''.join(now_playing())}")

    @commands.command(name="add_queue", aliases=["add_to_queue"])
    async def add_queue(self, ctx, track: str):
        try:
            add_queue(url=track)
            await ctx.send(f"{ctx.author.name}, Added your track to queue")
        except Exception as e:
            err = str(e)
            if "Premium required" in err:
                await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
            else:
                print(e)

    # ! SPOTIFY PREMIUM REQUIRED
    @commands.command(name="prev_track", aliases=["prev", "previous"])
    async def prev_track(self, ctx):
        if ctx.author.is_mod:
            try:
                prev_track()
                await ctx.send(f"{ctx.author.name}, Previous track")
            except Exception as e:
                err = str(e)
                if "Premium required" in err:
                    await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
                else:
                    print(e)
        else:
            await ctx.send("You are not a mod")

    # ! SPOTIFY PREMIUM REQUIRED
    @commands.command(name="skip", aliases=["next", "skip_track"])
    async def skip_track(self, ctx):
        if ctx.author.is_mod:
            try:
                skip_track()
                await ctx.send(f"{ctx.author.name} Next track is now playing")
            except Exception as e:
                err = str(e)
                if "Premium required" in err:
                    await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
                else:
                    print(e)
        else:
            await ctx.send("You are not a mod")

    # ! SPOTIFY PREMIUM REQUIRED
    @commands.command(name="volume", aliases=["vol"])
    async def change_volume(self, ctx, volume: int):
        if ctx.author.is_mod:
            try:
                _volume(volume)
                await ctx.send(f"{ctx.author.name}, Volume set to {volume}")
            except Exception as e:
                err = str(e)
                if "Premium required" in err:
                    await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
                else:
                    print(e)
        else:
            await ctx.send("You are not a mod")

    # ! SPOTIFY PREMIUM REQUIRED
    @commands.command(name="pause", aliases=["pause_track"])
    async def pause_track(self, ctx):
        if ctx.author.is_mod:
            try:
                pause_track()
                await ctx.send(f"{ctx.author.name} Paused track")
            except Exception as e:
                err = str(e)
                if "Premium required" in err:
                    await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
                else:
                    print(e)
        else:
            await ctx.send("You are not a mod")

    @commands.command(name="resume", aliases=["resume_track"])
    async def resume_track(self, ctx):
        if ctx.author.is_mod:
            try:
                resume_track(spotify_data["spotify"]["playlist_id"])
                await ctx.send(f"{ctx.author.name} Resumed track")
            except Exception as e:
                err = str(e)
                if "Premium required" in err:
                    await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
                else:
                    print(e)
        else:
            await ctx.send("You are not a mod")


def prepare(bot):
    bot.add_cog(spotify_commands(bot))
