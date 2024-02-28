import discord
from discord.ext import commands
from discord import app_commands
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import aiohttp
import datetime
import enka
import asyncio
from enka.enums import FightPropType, Language
import operator
import json
import base64

files = "test.json"
def load_data():
    try:
        with open(files, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data
def save_data(data):
    with open(files, 'w') as file:
        json.dump(data, file, indent=4)

global_data = {
    "data": None,
    "uid": None
}
inset_message = {'message' :None, "channelt": None}
emoji_list = []

async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def download_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def upload_img(url: str, session: aiohttp.ClientSession) -> str:
    payload = {
        "key": "6d207e02198a847aa98d0a2a901485a5",
        "source": url,
    }
    async with session.post("https://freeimage.host/api/1/upload", data=payload) as resp:
        data = await resp.json()
    return data["image"]["url"]

async def count_occurrences(value1, value2):
    variab = {
        "FIGHT_PROP_CRITICAL_HURT": (5.4, 7.9),
        "FIGHT_PROP_CRITICAL": (2.7, 4.0),
        "FIGHT_PROP_CHARGE_EFFICIENCY": (4.5, 6.6),
        "FIGHT_PROP_ELEMENT_MASTERY": (16, 24),
        "FIGHT_PROP_HP_PERCENT": (4.1, 5.9),
        "FIGHT_PROP_HP": (209, 300),
        "FIGHT_PROP_DEFENSE_PERCENT": (5.1, 7.4),
        "FIGHT_PROP_DEFENSE": (16, 24),
        "FIGHT_PROP_ATTACK_PERCENT": (4.1, 5.9),
        "FIGHT_PROP_ATTACK": (14, 20),
    }
    value = variab[value2]
    count = 1
    for l in range(1, 7):
        if value[0] <= (value1 / l) <= value[1]:
            return count
        count += 1

async def ntscuid(nntsl):
    url_nt = [
        "https://media.discordapp.net/attachments/1107978903294853140/1210263381962002462/IMG_4166.png?ex=65e9ec9b&is=65d7779b&hm=6e86ac07014a8f612985e79b50cdc50585254bf62a160a4393d01aa33d9068dc&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263382364528650/IMG_4170.png?ex=65e9ec9b&is=65d7779b&hm=7fb29f3027956cef58cabbe66bbf5b2fff1396641ddad0503e56647a306dc927&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263382700331069/IMG_4165.png?ex=65e9ec9c&is=65d7779c&hm=329305b4fc51cd10069c46e691fc0ec4d445d9d9bc538b833226c27bf2af8c83&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263383111245854/IMG_4164.png?ex=65e9ec9c&is=65d7779c&hm=08ade5d58d33ed3c1536eb2c57e72e9fe1b6080909f43ec44add3ee63bc73de2&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263383472078928/IMG_4168.png?ex=65e9ec9c&is=65d7779c&hm=5b334d4be866ef2eff894760e2c56af596a019b312ac16cf45b850110ba339ee&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263383803437166/IMG_4169.png?ex=65e9ec9c&is=65d7779c&hm=e334ea9a40d68aa347f321c0c78a61b64d8ed6131e8d037d3294bb77d49eb3ec&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1210263384159686686/IMG_4167.png?ex=65e9ec9c&is=65d7779c&hm=f53c9c8e48994daa1334bf0f7c9bd1cafb5217a92cd9c0e9b6cba428d2bfd013&a",
    ]
    urrl_nt = await download_images(url_nt)
    index = {
        "Wind": 0,
        "Rock": 1,
        "Electric": 2,
        "Grass": 3,
        "Water": 4,
        "Fire": 5,
        "Ice": 6
    }
    return urrl_nt[index[nntsl]]

async def licon(vlue):
  async with aiohttp.ClientSession() as session: 
    icon_inp ={
  "FIGHT_PROP_MAX_HP": "https://cdn.discordapp.com/emojis/1118937196418842734.png",
  "FIGHT_PROP_CUR_ATTACK": "https://cdn.discordapp.com/emojis/1118942800516485160.png",
  "FIGHT_PROP_CUR_DEFENSE": 'https://cdn.discordapp.com/emojis/1118944853015924758.png',
  "FIGHT_PROP_HP": "https://cdn.discordapp.com/emojis/1118937196418842734.png",
  "FIGHT_PROP_ATTACK": "https://cdn.discordapp.com/emojis/1118942800516485160.png",
  "FIGHT_PROP_DEFENSE": 'https://cdn.discordapp.com/emojis/1118944853015924758.png',
  "FIGHT_PROP_HP_PERCENT": "https://cdn.discordapp.com/emojis/1210381440639041597.png",
  "FIGHT_PROP_ATTACK_PERCENT": "https://cdn.discordapp.com/emojis/1210381514471120977.png",
  "FIGHT_PROP_DEFENSE_PERCENT": "https://cdn.discordapp.com/emojis/1210381625066782750.png",
  "FIGHT_PROP_CRITICAL": "https://cdn.discordapp.com/emojis/1118954424459599943.png",
  "FIGHT_PROP_CRITICAL_HURT": "https://cdn.discordapp.com/emojis/1118954407099371601.png",
  "FIGHT_PROP_CHARGE_EFFICIENCY": 'https://cdn.discordapp.com/emojis/1118961754190385282.png',
  "FIGHT_PROP_HEAL_ADD": 'https://cdn.discordapp.com/emojis/1118969739918708756.png',
  "FIGHT_PROP_ELEMENT_MASTERY": "https://cdn.discordapp.com/emojis/1118957536507351080.png",
  "FIGHT_PROP_PHYSICAL_ADD_HURT": 'https://cdn.discordapp.com/emojis/1210381516551757845.png',
  "FIGHT_PROP_WIND_ADD_HURT": 'https://cdn.discordapp.com/emojis/882253026021228544.webp?size=96&quality=lossless',
  "FIGHT_PROP_ROCK_ADD_HURT": 'https://cdn.discordapp.com/emojis/882253025895399504.webp?size=96&quality=lossless',
  "FIGHT_PROP_ELEC_ADD_HURT": 'https://cdn.discordapp.com/emojis/882254148584759317.webp?size=96&quality=lossless',
  "FIGHT_PROP_GRASS_ADD_HURT": 'https://cdn.discordapp.com/emojis/882253026113507349.webp?size=96&quality=lossless',
  "FIGHT_PROP_WATER_ADD_HURT": 'https://cdn.discordapp.com/emojis/882254676916068393.webp?size=96&quality=lossless',
  "FIGHT_PROP_FIRE_ADD_HURT": 'https://cdn.discordapp.com/emojis/882254077361262592.webp?size=96&quality=lossless',
  "FIGHT_PROP_ICE_ADD_HURT": 'https://cdn.discordapp.com/emojis/882253026046390292.webp?size=96&quality=lossless',
 }
    icus = await fetch_image(session, icon_inp[vlue])
    return icus

async def process_artifact(session, artifact, image_app, draw, artifact_counts, x_tdv_icon, x_tdv_rate, x_tdv_stats, y_tdv_stats2, y_cv1, count_tdv):
    #main_stat_TDV
    response = await fetch_image(session, artifact.icon)
    image_tdv0 = Image.open(BytesIO(response)).resize((165, 165))
    image_tdv0 = ImageEnhance.Brightness(image_tdv0).enhance(0.8)
    image_app.paste(image_tdv0, (3, x_tdv_icon), mask=image_tdv0)               

    response = await licon(artifact.main_stat.type.value)
    image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((50, 50))
    image_app.paste(image_tdv0, (17, x_tdv_stats+60), mask=image_tdv0)                              

    draw.text((14, x_tdv_rate), (f"{'★'*artifact.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 0))
    draw.text((14, x_tdv_stats+112), (f"{artifact.main_stat.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 28), fill=(255, 255, 250))

    artifact_counts[artifact.set_name] = artifact_counts.get(artifact.set_name, 0) + 1
    #sub_stats_TDV
    crit_dmg, crit_rate = 0, 0
    for substate in artifact.sub_stats[:4]:
        crit_rate = substate.value if substate.type.value == "FIGHT_PROP_CRITICAL" else crit_rate
        crit_dmg = substate.value if substate.type.value == "FIGHT_PROP_CRITICAL_HURT" else crit_dmg
    #Tdv_CV
    cv0 = crit_rate * 2 + crit_dmg
    color = ((113, 48, 53) if int(cv0) >= 50
        else (134, 123, 50) if 42 <= int(cv0) <= 49
        else (108, 42, 113) if 32 <= int(cv0) <= 41
        else (48, 68, 124) if 18 <= int(cv0) <= 31
        else (77, 77, 77))
    draw.rounded_rectangle([19 - 5, y_cv1 - 5, 19 + 68 + 5, y_cv1 + 18 + 5], 8, fill=color)
    draw.text((19, y_cv1+22), f"+{artifact.level}", font=ImageFont.truetype("zh-cn.ttf", 23), fill=(255, 255, 255))
    draw.text((18 + 1, y_cv1 + 1), f"{cv0:.1f}CV", font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))

async def process_substate(substate, image_app, draw, artifact_counts, x_tdv_stats, y_tdv_stats2, count_tdv):
    response = await licon(substate.type.value)
    image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((40, 40))
    image_app.paste(image_tdv0, (142, x_tdv_stats+2), mask=image_tdv0)                      

    occurrence = await count_occurrences(float(substate.formatted_value.replace('%', '')), substate.type.value)
    text_fill = (255, 255, 255) if occurrence >= 2 else (170, 170, 170)
    draw.text((142+42, x_tdv_stats+10), (f"+{substate.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=text_fill)
    draw.text((142+125, x_tdv_stats+14), (f"{'*'*occurrence}"), font=ImageFont.truetype("zh-cn.ttf", 21), fill=text_fill)     

async def image_dcuid(charactert):
    async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
        async with aiohttp.ClientSession() as session: 
              uid = global_data.get("uid")
              data = global_data.get("data")
              weapon = charactert.weapon     
              urls_to_download = [charactert.costume.icon.gacha if charactert.costume is not None else charactert.icon.gacha,
                  charactert.weapon.icon,            
                  charactert.talents[0].icon,
                  charactert.talents[1].icon,
                  charactert.talents[2].icon,
                  "https://cdn.discordapp.com/emojis/1210395337139683328.png",
                  "https://media.discordapp.net/attachments/1107978903294853140/1210964500166082570/233149C0-7EA6-4CC6-A333-C6E3EE916190.png?ex=65ec7993&is=65da0493&hm=e08c7e5d514db42f1614e4291775a417cf46a2d5bfa53a9ce75c73c8d987bf1e&a",]
              responses = await download_images(urls_to_download)
              image_app = Image.open(BytesIO(await ntscuid(charactert.element.value))).resize((1455, 885))
              font = ImageFont.truetype("zh-cn.ttf", 27)
              draw = ImageDraw.Draw(image_app)
              #char
              image_schar0 = Image.open(BytesIO(responses[0]))
              char_icon = [
                (image_schar0, (((image_app.width - image_schar0.width) // 2)-25, (image_app.height - image_schar0.height) // 2)),
                (Image.open(BytesIO(responses[6])).convert("RGBA"), (0, 0)),
                (Image.open(BytesIO(responses[1])).convert("RGBA").resize((144, 124)), (958, 19)),
                (Image.open(BytesIO(await licon(weapon.stats[1].type.value))).convert("RGBA").resize((44, 41)), (1290, 57)),
              ]
              for char_ios in char_icon[:4]:
                image_app.paste(char_ios[0], char_ios[1], mask=char_ios[0])
              char_info = [
                (f"{charactert.name}  \nBFF.{charactert.friendship_level}  \nlv.{charactert.level}/{charactert.max_level}", ImageFont.truetype("zh-cn.ttf", 24), (325, 4), (255, 255, 255)),
                (f"{data.player.nickname} \nUID:{uid}  AR:{data.player.level}", ImageFont.truetype("zh-cn.ttf", 24), (1128, 812), (255, 255, 255)),
                (weapon.name if len(weapon.name) < 23 else weapon.name + "...", ImageFont.truetype("zh-cn.ttf", 22), (1121, 16), (255, 255, 255)),
                (f"R{weapon.refinement}", ImageFont.truetype("zh-cn.ttf", 27), (1121, 108), (255, 255, 255)),
                (f"{weapon.level}/{weapon.max_level}", ImageFont.truetype("zh-cn.ttf", 27), (1264, 108), (255, 255, 255)),
                (f"{'★'*weapon.rarity}", ImageFont.truetype("zh-cn.ttf", 24), ((973, 114) if weapon.rarity == 5 else (986, 114)), (255, 255, 0)),
                ((f"{round(weapon.stats[0].value)}"), ImageFont.truetype("zh-cn.ttf", 27), (1190, 60), (255, 255, 255)),
                ((f"{weapon.stats[1].formatted_value}"), ImageFont.truetype("zh-cn.ttf", 27), (1350, 60), (255, 255, 255)),
              ]
              for char_ip in char_info[:8]:
                draw.text(char_ip[2], char_ip[0], font=char_ip[1], fill=char_ip[3])
              #stats
              dmg_bonut = charactert.highest_dmg_bonus_stat
              stat_infos = [
                  (("HP", FightPropType.FIGHT_PROP_MAX_HP), (967, 220-30), (40, 40)),
                  (("Tấn Công", FightPropType.FIGHT_PROP_CUR_ATTACK), (967, 255-30), (40, 40)),
                  (("Phòng Ngự", FightPropType.FIGHT_PROP_CUR_DEFENSE), (967, 295-30), (40, 40)),
                  (("Tinh Thông Nguyên Tố", FightPropType.FIGHT_PROP_ELEMENT_MASTERY), (967, 335-30), (40, 40)),
                  (("Tỉ Lệ Bạo", FightPropType.FIGHT_PROP_CRITICAL), (967, 375-30), (40, 40)),
                  (("Sát Thương Bạo", FightPropType.FIGHT_PROP_CRITICAL_HURT), (967, 415-30), (40, 40)),
                  (("Hiệu Quả Nạp", FightPropType.FIGHT_PROP_CHARGE_EFFICIENCY), (967, 455-30), (40, 40)),
                  (("Trị Liệu", FightPropType.FIGHT_PROP_HEAL_ADD), (967, 495-30), (40, 40)),
                  ((f"{dmg_bonut.name[5:]}", dmg_bonut.type), (967, 535-30), (40, 40)),]                
              for stat_info in stat_infos[:9]:
                stat_value = charactert.stats[stat_info[0][1]]
                draw.text((stat_info[1][0] + 43, stat_info[1][1] + 3), (f"{stat_value.formatted_value} -> {stat_info[0][0]}"), font=ImageFont.truetype("zh-cn.ttf", 25), fill=(255, 255, 255))                         
                icon_image = Image.open(BytesIO(await licon(stat_value.type.name))).convert("RGBA").resize(stat_info[2])
                image_app.paste(icon_image, stat_info[1], mask=icon_image)
              #TDV
              artifact_counts = {}
              x_tdv_icon, x_tdv_rate, x_tdv_stats = 4, 140, 4
              y_tdv_stats2, y_cv1 = 40, 9
              count_tdv = 0
              tasks = []
              substate_tasks = []
              for artifact in charactert.artifacts[:5]:
                  tasks.append(process_artifact(session, artifact, image_app, draw, artifact_counts, x_tdv_icon, x_tdv_rate, x_tdv_stats, y_tdv_stats2, y_cv1, count_tdv))
                  x_tdv_icon += 177
                  x_tdv_rate += 177
                  y_cv1 += 177
                  for substate in artifact.sub_stats[:4]:
                    substate_tasks.append(process_substate(substate, image_app, draw, artifact_counts, x_tdv_stats, y_tdv_stats2, count_tdv))
                    x_tdv_stats += 40   
                    count_tdv += 1
                    if count_tdv % 4 == 0:
                        x_tdv_stats = x_tdv_stats - 160 + 177
              await asyncio.gather(*tasks, *substate_tasks)
              #Set_tdv
              sorted_counts = dict(sorted(artifact_counts.items(), key=operator.itemgetter(1), reverse=True))
              y_position = 585
              for set_name, count in sorted_counts.items():
                  if count >= 2 and count < 4:
                      draw.text((1011, y_position), f"{set_name} x{count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(0, 205, 102))
                      y_position += 32
                  elif count >= 4:
                      draw.text((1011, 599), f"x{count} {set_name}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(0, 205, 102))
              #thiên phú
              skill_positions = [(338, 636), (338, 719), (338, 802)]                
              for i in range(3):
                  image_skill = Image.open(BytesIO(responses[i + 2])).convert("RGBA").resize((60, 60))
                  image_app.paste(image_skill, skill_positions[i], mask=image_skill)
                  draw.text((393 if charactert.talents[i].level > 9 else 400, 664 + i * 83), f"{charactert.talents[i].level}", font=font, fill=(255, 255, 255))                                
              #cm
              Locks = len(charactert.constellations)
              x_lock = 903
              for _ in range(6 - Locks):
                  image_skill00 = Image.open(BytesIO(responses[5])).convert("RGBA").resize((43, 43))
                  image_app.paste(image_skill00, (x_lock, 802), mask=image_skill00)
                  x_lock -= 86
              inseta = 465
              for constellation in charactert.constellations:
                  response = await fetch_image(session, constellation.icon)
                  image_skill00 = Image.open(BytesIO(response)).convert("RGBA").resize((60, 60))
                  image_app.paste(image_skill00, (inseta, 798), mask=image_skill00)
                  inseta += 86
              buffer = BytesIO()
              image_app.save(buffer, format='png')
              buffer.seek(0)
              file = discord.File(buffer, filename="showcase.png")
              channel = inset_message.get("channelt")
              messaget = await channel.send(file=file)
              file_url = messaget.attachments[0]
              return file_url

outputz = {}
class Select(discord.ui.Select):
    def __init__(self, *args, **kwargs):
        self.data = global_data.get("data")
        self.channel = inset_message.get('channelt')
        super().__init__(*args, **kwargs)
        options = [
            discord.SelectOption(label=char.name, value=f"char{i+1}") for i, char in enumerate(self.data.characters)
        ]
        super().__init__(placeholder="showcare", max_values=1, min_values=1, options=options)
    async def callback(self, I: discord.Interaction):
        async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
            char = self.data.characters[int(self.values[0][-1]) - 1]
            now = datetime.datetime.now()
            embed_loading = discord.Embed(title="<a:aloading:1152869299942338591> **Đang tạo thông tin..__Hãy kiên nhẫn__** <a:ganyurollst:1118761352064946258>", color=discord.Color.yellow())
            await I.response.edit_message(content=None, embed=embed_loading)
            embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.datetime.now())
            reload_time = now + datetime.timedelta(seconds=self.data.ttl)
            embed.add_field(name=f"Name.{char.name}", value=f"Level.{char.level} \nnguyên tố.{char.element} C.{len(char.constellations)} \nLàm mới: <t:{int(reload_time.timestamp())}:R>", inline=False) 
            embed.set_thumbnail(url=f"{char.icon.front}")
            embed.set_footer(text="", icon_url=f"{I.user.avatar}")
            if char.name in outputz:
              file_url = outputz[char.name]
            else:
              file_url = await image_dcuid(char)
              outputz[char.name] = file_url
            embed.set_image(url=file_url)
            message = inset_message.get("message")
            await message.edit(content=None, embed=embed)
 
class SelectView(discord.ui.View):
    def __init__(self, *, timeout=300):
        super().__init__(timeout=timeout)
        self.select = Select()
        self.add_item(self.select)
    async def on_timeout(self):
      message = inset_message.get("message")
      options = [
          discord.SelectOption(label="Tùy chọn 1", value="option1"),
      ]
      select = discord.ui.Select(placeholder="Timeout!!", options=options, disabled=True)
      embed = discord.Embed(color=discord.Color.red())
      embed.add_field(name="Timeout!", value="Nếu bạn muốn xem lại, hãy sử dụng lệnh ``/scuid``")
      views = discord.ui.View()
      views.add_item(select)
      await message.edit(embed=embed, view=views)

async def generate_image(data):
    async with aiohttp.ClientSession() as session:
        uid = global_data.get("uid")
        urlgoc = await fetch_image(session, 'https://media.discordapp.net/attachments/1107978903294853140/1206074586098176010/F7C59933-6074-48A1-8422-A66E5B12B81F.png?ex=65e3e9fd&is=65d174fd&hm=292f17eaab0fb457ca1e98f3821dd7cfd222491f73dbedc63d371c8310a4b78b&a')
        image_appt = Image.open(BytesIO(urlgoc)).convert("RGBA").resize((600, 850))
        draw = ImageDraw.Draw(image_appt)
        player_icon_data = await fetch_image(session, data.player.profile_picture_icon.circle)
        player_icon = Image.open(BytesIO(player_icon_data)).resize((141, 141)).convert("RGBA")
        image_appt.paste(player_icon, (77, 62), player_icon)
        draw.text((238, 60), data.player.nickname, font=ImageFont.truetype("zh-cn.ttf", 16), fill=(0, 0, 0))
        draw.text((238, 104), data.player.signature, font=ImageFont.truetype("zh-cn.ttf", 14), fill=(0, 0, 0))
        draw.text((476, 171), f"{data.player.level}", font=ImageFont.truetype("zh-cn.ttf", 16), fill=(0, 0, 0))
        draw.text((480, 208), f"{data.player.world_level}", font=ImageFont.truetype("zh-cn.ttf", 16), fill=(0, 0, 0))
        draw.text((78, 208), f"UID:{uid}", font=ImageFont.truetype("zh-cn.ttf", 18), fill=(255, 255, 255))
        draw.text((138, 266), f"{data.player.achievements}", font=ImageFont.truetype("zh-cn.ttf", 23), fill=(255, 255, 255))
        draw.text((322, 266), f"{data.player.abyss_floor}-{data.player.abyss_level}", font=ImageFont.truetype("zh-cn.ttf", 23), fill=(255, 255, 255))
        x, y = 15, 380
        for i, char in enumerate(data.characters[:8]):
            char_icon_data = await fetch_image(session, char.costume.icon.circle if char.costume is not None else char.icon.circle)
            char_icon = Image.open(BytesIO(char_icon_data)).convert("RGBA").resize((80, 80))
            char_icon_datak = await fetch_image(session, char.namecard.full)
            char_imaget = Image.open(BytesIO(char_icon_datak)).convert("RGBA").resize((279, 104))
            url_goc = await fetch_image(session, 'https://media.discordapp.net/attachments/1107978903294853140/1210886413302763520/Khong_Co_Tieu_e164.png?ex=65ec30da&is=65d9bbda&hm=bbbc2697264af7c9bf80fc56eb7b4db70a17526197d7fbbb226859e5d3229ae9&a')
            char_iconk = Image.open(BytesIO(url_goc)).convert("RGBA").resize((279, 104))
            enhancer = ImageEnhance.Brightness(char_imaget)
            char_image = enhancer.enhance(0.8)
            char_draw = ImageDraw.Draw(char_image)
            char_image.paste(char_iconk, (0, 0), char_iconk)
            char_image.paste(char_icon, (10, 12), char_icon)
            char_draw.text((101, 4), char.name, font=ImageFont.truetype("zh-cn.ttf", 15), fill=(255, 255, 255))
            char_draw.text((102, 33), f"Lv.{char.level}/{char.max_level}", font=ImageFont.truetype("zh-cn.ttf", 14), fill=(255, 255, 255))
            char_draw.text((180, 34), f"C{len(char.constellations)}", font=ImageFont.truetype("zh-cn.ttf", 14), fill=(255, 255, 255))
            char_draw.text((102, 59), f"Friendship {char.friendship_level}", font=ImageFont.truetype("zh-cn.ttf", 12), fill=(255, 255, 255))
            crit_dmg = 0
            crit_rate = 0
            x_skill = 105
            for artifact in char.artifacts:
                for substate in artifact.sub_stats:
                    if substate.name == "Tỷ Lệ Bạo Kích":
                        crit_rate += substate.value
                    elif substate.name == "ST Bạo Kích":
                        crit_dmg += substate.value
            cv0 = (crit_rate) * 2 + crit_dmg
            char_draw.text((193, 59), f"{cv0:.1f}CV", font=ImageFont.truetype("zh-cn.ttf", 12), fill=(255, 255, 255))
            for j, talent in enumerate(char.talents[:3]):
                talent_icon_url = talent.icon
                talent_icon_data = await fetch_image(session, talent_icon_url)
                talent_icon = Image.open(BytesIO(talent_icon_data)).resize((20, 20)).convert('RGBA')
                char_image.paste(talent_icon, (105 + j * 47, 80), talent_icon)
                char_draw.text((x_skill+23, 82), f"{talent.level}", font=ImageFont.truetype("zh-cn.ttf", 14), fill=(255, 255, 255))
                x_skill += 47
                char_draw.text((102, 59), f"Friendship {char.friendship_level}", font=ImageFont.truetype("zh-cn.ttf", 12), fill=(255, 255, 255))
            image_appt.paste(char_image, (x, y))
            x += 294
            if (i + 1) % 2 == 0:
                x = 15
                y += 115
        buffer = BytesIO()
        image_appt.save(buffer, format='png')
        buffer.seek(0)
        file = discord.File(buffer, filename="output.png")
        return file

class scuids(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)
    
  @app_commands.command(name="scuid", description="check dữ liệu uid genshin")
  async def scuid(self, Interaction, uid: int = None , user: discord.Member = None):
    async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
     channel = self.bot.get_channel(1118977913392476210)
     inset_message["channelt"] = channel
     try:
        data = load_data()
        user_id = str(Interaction.user.id) if user is None else str(user.id)
        if uid is not None:
          uid = uid
        else: 
          if user_id in data:
             uid = data[user_id]["uid"] if "uid" in data[user_id] else await Interaction.response.send_message("Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")
          else:
             await Interaction.response.send_message("Bạn chưa đăng kí hãy sửa dụng ``/login`` để tiếp tục")
        data = await api.fetch_showcase(uid)
        global_data["data"] = data
        global_data["uid"] = uid
        embed = discord.Embed()
        embed.add_field(name="vui lòng đợi thông tin được sử lý", value="", inline=False)
        await Interaction.response.send_message(embed=embed, ephemeral=True)
        if data.characters is not None and len(data.characters) > 0:
          file = await generate_image(data)
          message = await Interaction.channel.send(file=file, view=SelectView())
          inset_message["message"] = message
        else:
          embed1 = discord.Embed(color=0xed0202)
          embed1.add_field(name="lỗi", value="Không tìm thấy dữ liệu cho người dùng này.", inline=False)
          embed1.add_field(name="Chuyện gì đã xảy ra?", value="Vấn đề thường gặp nhất với lỗi này đó là tài khoản bạn đang tìm kiếm chưa công khai Hồ sơ. Để sửa lỗi này, hãy bật tùy chọn ``Hiển thị chi tiết nhân vật`` trong giao diện Hồ sơ Genshin của bạn. Hãy tham khảo hình ảnh bên dưới", inline=False)
          embed1.set_image(url="https://media.discordapp.net/attachments/1107978903294853140/1210882152842006538/Khong_Co_Tieu_e162_20240224163313.png?ex=65ec2ce2&is=65d9b7e2&hm=d99f4a97b54aad9c632adafbf19de28986fe0f5436b22ca469a9c1c64520457f&a")
          await Interaction.followup.send(embed=embed1, ephemeral=True)
          
     except Exception as s:
        await channel.send(f"Error: {s}")

async def setup(bot):
  await bot.add_cog(scuids(bot))