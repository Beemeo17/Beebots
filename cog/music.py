import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import urllib.parse, urllib.request, re
from concurrent.futures import ThreadPoolExecutor
import aiohttp

loop_song = False
def fetch_title(url):
    yt = YouTube(url)
    return yt.title
class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.current_volume = 0.5
        self.current_speed = 1.0
        self.queue = {}
        self.current_song = {}
        self.yt_dl_options = {"format": "bestaudio/best"}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
        self.youtube_base_url = 'https://www.youtube.com/'
        self.youtube_results_url = self.youtube_base_url + 'results?'
        self.youtube_watch_url = self.youtube_base_url + 'watch?v='
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id='bb031d0c49744f12b281e5d41e10c966', 
            client_secret='5bc0091d7b4347798a0e79377d367819'
        )
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
    
    def ffmpeg_options(self, volume, speed):
        return {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': f'-vn -filter:a "volume={volume},atempo={speed}"'
        }


    async def play_next(self, ctx):
        global loop_song
        if loop_song and self.current_song[ctx.guild.id]:
            loop = asyncio.get_event_loop()
            
            data = await asyncio.to_thread(self.ytdl.extract_info, self.current_song[ctx.guild.id], download=False)
            song = data['url']
            
            player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options(self.current_volume, self.current_speed))
            self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
        elif self.queue[ctx.guild.id]:
            next_url = self.queue[ctx.guild.id].pop(0)
            self.current_song[ctx.guild.id] = next_url

            loop = asyncio.get_event_loop()
            
            data = await asyncio.to_thread(self.ytdl.extract_info, next_url, download=False)
            song = data['url']

            player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options(self.current_volume, self.current_speed))
            self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

            yt = YouTube(next_url)
            title = yt.title
            author = yt.author
            length = yt.length
            tl = yt.thumbnail_url

            hours = length // 3600
            minutes = (length % 3600) // 60
            remaining_seconds = length % 60
            result = []
            if hours > 0:
                result.append(f"{hours}:")
            if minutes > 0:
                result.append(f"{minutes}:")
            if remaining_seconds > 0:
                result.append(f"{remaining_seconds}")

            now = datetime.datetime.now()
            new_time = now + datetime.timedelta(seconds=length)

            voice_client = ctx.guild.voice_client
            if voice_client and voice_client.is_connected():
                channel = voice_client.channel
                embed = discord.Embed()
                embed.set_author(name=title, url=next_url, icon_url="https://cdn.discordapp.com/emojis/1153748335337938994.gif?size=96&quality=lossless")
                embed.add_field(name=f"{ctx.user.mention}✦``{''.join(result)}``<t:{int(new_time.timestamp())}:R>\n **``channel:``**:<#{channel.id}>", value="", inline=False)
                embed.set_thumbnail(url=tl)
                embed.set_footer(text=f"Lệnh Hỗ Trợ /help | Tác giả: {author}", icon_url="https://cdn.discordapp.com/emojis/1153569595714707456.gif")
                await ctx.channel.send(embed=embed, view=ButtonView())
        
        else:
            embed = discord.Embed(title="Hàng chờ nhạc trống. Đến giờ bot đi ngủ rồi")
            await ctx.channel.send(embed=embed)
            await ctx.guild.voice_client.disconnect()

    async def fetch_yt_url(self, session, url):
        query_string = urllib.parse.urlencode({'search_query': url})
        async with session.get(self.youtube_results_url + query_string) as response:
            content = await response.text()
            search_results = re.findall(r'/watch\?v=(.{11})', content)
            if search_results:
                return self.youtube_watch_url + search_results[0]
            return None

    async def spo_to_yt(self, url):
        async with aiohttp.ClientSession() as session:
            return await self.fetch_yt_url(session, url)

    async def music(self, I, url):
        if "http" not in url:
            url_ = await self.spo_to_yt(url)
            self.queue[I.guild.id].append(url_)
            return url_
        else:
            if "youtu.be" in url or "youtube.com" in url:
                self.queue[I.guild.id].append(url)
                return url

            def song(url):
                if "spotify.com/track" in url:
                    track = self.sp.track(url)
                    if track:
                        return track['name'], track['artists'][0]['name'], track['external_urls']['spotify'], track['id'], track['album']['images'][0]['url']
                    else:
                        return None

                if "spotify.com/album" in url:
                    album = self.sp.album(url)
                    if album:
                        return album['name'], album['artists'][0]['name'], album['external_urls']['spotify'], album['id'], album['images'][0]['url']
                    else:
                        return None

                if "spotify.com/playlist" in url:
                    playlist = self.sp.playlist(url)
                    if playlist:
                        return playlist['name'], playlist['external_urls']['spotify'], playlist['id'], playlist['images'][0]['url']
                    else:
                        return None

                results = self.sp.search(q=url, type='album', limit=1)
                if results['albums']['items']:
                    album = results['albums']['items'][0]
                    return album['name'], album['artists'][0]['name'], album['external_urls']['spotify'], album['id'], album['images'][0]['url']
                else:
                    return None

            def get_all_tracks_in_album(album_id):
                tracks = self.sp.album_tracks(album_id)['items']
                return [(track['name'], track['artists'][0]['name'], track['external_urls']['spotify']) for track in tracks]

            def get_all_tracks_in_playlist(playlist_id):
                tracks = self.sp.playlist_tracks(playlist_id)['items']
                return [(track['track']['name'], track['track']['artists'][0]['name'], track['track']['external_urls']['spotify']) for track in tracks]

            async def fetch_spotify_info(url):
                return song(url)

            async def fetch_youtube_url(query):
                return await self.spo_to_yt(query)

            async def handle_spotify_url(I, url):
                result = await fetch_spotify_info(url)
                if "spotify.com/track" in url:
                    track_name, artist_name, _, _, cover_image = result
                    _url = await fetch_youtube_url(f"{track_name} {artist_name}")
                    self.queue[I.guild.id].append(_url)
                elif "spotify.com/album" in url:
                    album_name, _, _, album_id, cover_image = result
                    _url = await fetch_youtube_url(album_name)
                    self.queue[I.guild.id].append(_url)

                    tracks_info = get_all_tracks_in_album(album_id)
                    if tracks_info:
                        async with aiohttp.ClientSession() as session:
                            tasks = [self.fetch_yt_url(session, f"{track_name} {artist_name}") for track_name, artist_name, _ in tracks_info]
                            yt_urls = await asyncio.gather(*tasks)
                            self.queue[I.guild.id].extend(yt_urls)
                elif "spotify.com/playlist" in url:
                    playlist_name, _, playlist_id, cover_image = result
                    tracks_info = get_all_tracks_in_playlist(playlist_id)
                    if tracks_info:
                        async with aiohttp.ClientSession() as session:
                            tasks = [self.fetch_yt_url(session, f"{track_name} {artist_name}") for track_name, artist_name, _ in tracks_info]
                            yt_urls = await asyncio.gather(*tasks)
                            self.queue[I.guild.id].extend(yt_urls)

            if "spotify.com" in url:
                await handle_spotify_url(I, url)
            elif "youtu.be" in url or "youtube.com" in url:
                return

    async def remove_list_parameter(self, url):
        list_index = url.find('&list=')
        if list_index != -1:
            next_ampersand = url.find('&', list_index + len('&list='))
            if next_ampersand != -1:
                return url[:list_index] + url[next_ampersand:]
            else:
                return url[:list_index]
        return url

    async def create_queue_embed(self, I, page):
        embed = discord.Embed(title="Hàng chờ nhạc", color=discord.Color.dark_gold())
        start = (page - 1) * 6
        end = start + 6
        queue_slice = self.queue[I.guild.id][start:end]
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            titles = await asyncio.gather(*[loop.run_in_executor(pool, fetch_title, url) for url in queue_slice])

        for i, (url, title) in enumerate(zip(queue_slice, titles), start=start + 1):
            embed.add_field(name=f"{i}. {title}", value=url, inline=False)
        
        embed.set_footer(text=f"page {page}/{(len(self.queue[I.guild.id]) + 5) // 6}")
        return embed

    @app_commands.command(name='play', description="Phát nhạc theo mong muốn của bạn")
    async def play(self, Interaction, *, searchs: str):
        search = await self.remove_list_parameter(searchs)
        if Interaction.guild.id not in self.queue:
            self.queue[Interaction.guild.id] = []

        if Interaction.user.voice:
            try:
                voice_client = await Interaction.user.voice.channel.connect()
                self.voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)
        else:
            return await Interaction.response.send_message("❌ Bạn không ở trong một voice nào cả!!")
        
        await Interaction.response.send_message("Đang tải nội dung!")
        OutSong = await self.music(Interaction, search)
        try:
            url = self.queue[Interaction.guild.id][0]
            if "spotify.com/album" in search:
                album = self.sp.album(search)
                if album:
                    cover_image = album['images'][0]['url']
                    embed = discord.Embed()
                    embed.add_field(name=f"**Đã thêm vào hàng chờ**\n{album['name']}\n{album['external_urls']['spotify']}", value="", inline=False)
                    embed.set_thumbnail(url=cover_image)
                    await Interaction.channel.send(embed=embed)
            elif "spotify.com/track" in search:
                track = self.sp.track(search)
                if track:
                    cover_image = track['album']['images'][0]['url']
                    embed = discord.Embed()
                    embed.add_field(name=f"**Đã thêm vào hàng chờ**\n{track['name']} - {track['artists'][0]['name']}\n{track['external_urls']['spotify']}", value="", inline=False)
                    embed.set_thumbnail(url=cover_image)
                    await Interaction.channel.send(embed=embed)
            elif "spotify.com/playlist" in search:
                playlist = self.sp.playlist(search)
                if playlist:
                    cover_image = playlist['images'][0]['url']
                    embed = discord.Embed()
                    embed.add_field(name=f"**Đã thêm vào hàng chờ**\n{playlist['name']}\n{playlist['external_urls']['spotify']}", value="", inline=False)
                    embed.set_thumbnail(url=cover_image)
                    await Interaction.channel.send(embed=embed)
            else:
                if self.queue[Interaction.guild.id]:
                    embed = discord.Embed()
                    embed.add_field(name=f"**Đã thêm vào hàng chờ**\n{YouTube(OutSong).title}\n{OutSong}", value="", inline=False)
                    embed.set_thumbnail(url=YouTube(OutSong).thumbnail_url)
                    await Interaction.channel.send(embed=embed)

            if not Interaction.guild.voice_client.is_playing():
                await self.play_next(Interaction)
        except Exception as e:
            print(e)

    @app_commands.command(name='stop', description="Dùng nhạc đang phát")
    async def stop(self, Interaction):
        global loop_song
        self.queue[Interaction.guild.id].clear()
        loop_song = False
        self.current_song[Interaction.guild.id] = None
        Interaction.guild.voice_client.stop()
        await Interaction.response.send_message("Đã dừng phát nhạc")

    @app_commands.command(name='skip', description="Chuyển tới bài hát bạn mong muốn")
    async def skip(self, Interaction, index: int=None):
        try:
            if index is not None:
                if 1 <= index <= len(self.queue[Interaction.guild.id]):
                    if len(self.queue[Interaction.guild.id]) <= 1:
                        pass
                    else:
                        selected_song = self.queue[Interaction.guild.id].pop(index - 1)
                        self.queue[Interaction.guild.id].insert(0, selected_song)
                else:
                    await Interaction.response.send_message('Chỉ số không hợp lệ.')
                    return
            
            if Interaction.guild.voice_client and self.queue[Interaction.guild.id] != []:
                Interaction.guild.voice_client.pause()
                await Interaction.response.send_message('Đã bỏ qua bài hát.')
                await self.play_next(Interaction)
            else:
                await Interaction.response.send_message('Không có bài hát nào đang phát.')
        except Exception as e:
            await Interaction.response.send_message(f'Đã xảy ra lỗi: {str(e)}')

    @app_commands.command(name='loop', description="Lặp bài hát đang được phát")
    async def loop(self, Interaction):
        global loop_song
        loop_song = not loop_song
        await Interaction.response.send_message('Chế độ lặp lại: ' + ('Bật' if loop_song else 'Tắt'))

    @app_commands.command(name='queue', description="Hiển thị hàng chờ nhạc hiện tại")
    async def show_queue(self, Interaction: discord.Interaction):
        if Interaction.guild.id not in self.queue or not self.queue[Interaction.guild.id]:
            await Interaction.response.send_message("Hàng chờ trống.")
            return

        embed = await self.create_queue_embed(Interaction, 1)
        message = await Interaction.response.send_message(embed=embed, view=QueueView(self, self.queue))

    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        if 0 <= volume <= 100:
            self.current_volume = volume / 100
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                ctx.voice_client.resume()
            await ctx.send(f"Volume set to {volume}%")
        else:
            await ctx.send("Volume must be between 0 and 100")

    @commands.command(name='speed')
    async def speed(self, ctx, speed: float):
        if 0.5 <= speed <= 2.0:
            self.current_speed = speed
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                ctx.voice_client.resume()
            await ctx.send(f"Playback speed set to {speed}x")
        else:
            await ctx.send("Speed must be between 0.5 and 2.0")



class QueueView(discord.ui.View):
    def __init__(self, music_cog, queue, timeout=180):
        super().__init__(timeout=timeout)
        self.music_cog = music_cog
        self.page = 1
        self.queue = queue

    @discord.ui.button(label="", emoji="◀️", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.next_page.disabled = False
            self.page -= 1
            embed = await self.music_cog.create_queue_embed(interaction, self.page)
            if self.page <= 1:
                button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="", emoji="▶️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (len(self.queue[interaction.guild.id]) + 5) // 6 <= 1:
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.response.send_message("Chuyển trang không hợp lệ!")
        if self.page < (len(self.music_cog.queue[interaction.guild.id]) + 5) // 6:
            self.previous_page.disabled = False
            self.page += 1
            embed = await self.music_cog.create_queue_embed(interaction, self.page)
            if self.page == (len(self.queue[interaction.guild.id]) + 5) // 6:
                button.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            print("="*50)
        

class ButtonView(discord.ui.View):
    def __init__(self, timeout=300):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="", emoji="▶️")
    async def button_pause(self, interaction, button: discord.ui.Button):
        button.disabled = True
        self.button_resume.disabled = False
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="", emoji="⏸️", disabled=True)
    async def button_resume(self, interaction, button: discord.ui.Button):
        button.disabled = True
        self.button_pause.disabled = False
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="", emoji="🔁")
    async def button_loop(self, interaction, button: discord.ui.Button):
        global loop_song
        loop_song = not loop_song
        await interaction.response.send_message('Chế độ lặp lại: ' + ('Bật' if loop_song else 'Tắt'))

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
