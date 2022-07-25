from ast import expr_context
from twitchio.ext import commands
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from utils import resume_track, search, now_playing, prev_track, skip_track, _volume, pause_track, add_track__


with open("data.json", "r", encoding="utf-8") as f:
    spotify_data = json.load(f)


scope = 'playlist-modify-public playlist-modify-private user-read-currently-playing user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=spotify_data["spotify"]["client_id"],
        client_secret=spotify_data["spotify"]["client_secret"],
        redirect_uri=spotify_data["spotify"]["redirect_uri"],
    )
)


class spotify_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ! SPOTIFY PREMIUM REQUIRED
    @commands.command(name="add", aliases=["add_track", "add_song", "play"])
    async def play_track(self, ctx, track_id):
        print(sp.me())
        track = []
        if track_id.startswith("https://open.spotify.com/track/"):
            track = track[34:]
        elif track_id.startswith("spotify:track:"):
            track = track[13:]
        try:
            add_track__(playlist_id=spotify_data["spotify"]["playlist_id"], track_id=track)
            await ctx.send(f"{ctx.author.name}, Added your track to playlist")
        except Exception as e:
            err = str(e)
            if "Premium required" in err:
                await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
            else:
                print(e)

    @commands.command(name="search", aliases=["s"])
    async def search(self, ctx, *, query):
        items = search(query)
        link = items[0]['external_urls']['spotify']
        await ctx.send(f"Search results for {query}: {link}")

    @commands.command(name="song", aliases=["nowplaying", "np"])
    async def now_playing(self, ctx):
        await ctx.send(f"Now playing: {''.join(now_playing())}")

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

    @commands.command()
    async def track_add(self, ctx, track_id):
        track = []
        if track_id.startswith("https://open.spotify.com/track/"):
            track = track[34:]
        elif track_id.startswith("spotify:track:"):
            track = track[13:]
        try:
            result = sp.playlist_add_items(spotify_data["spotify"]["playlist_id"], track)
            print(result)
            await ctx.send(f"{ctx.author.name}, Added your track to playlist")
        except Exception as e:
            err = str(e)
            if "Premium required" in err:
                await ctx.send(f"{ctx.author.name}, Request raised an Error: PREMIUM REQUIRED")
            else:
                print(e)


def prepare(bot):
    bot.add_cog(spotify_commands(bot))
