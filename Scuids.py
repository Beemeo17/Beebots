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
import traceback
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
  
async def image_dcuid(charactert):
    async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
        async with aiohttp.ClientSession() as session: 
              uid = global_data.get("uid")
              data = global_data.get("data")
              weapon = charactert.weapon     
              urls_to_download = [
                  charactert.costume.icon.gacha if charactert.costume is not None else charactert.icon.gacha,
                  charactert.weapon.icon,            
                  charactert.talents[0].icon,
                  charactert.talents[1].icon,
                  charactert.talents[2].icon,
                  "https://cdn.discordapp.com/emojis/1210395337139683328.png",
                  "https://media.discordapp.net/attachments/1107978903294853140/1210397607147602001/AFB13433-D899-4DA5-9761-16D69195636C.png?ex=65ea699d&is=65d7f49d&hm=df95ff8fb259fd4854c9e043ac5b9529d29ead1e94fc37cb8df25b07b646fcd1&a",
              ]
              responses = await download_images(urls_to_download)
              image_app = Image.open(BytesIO(await ntscuid(charactert.element.value))).resize((1455, 885))
              font = ImageFont.truetype("zh-cn.ttf", 27)
              draw = ImageDraw.Draw(image_app)
              #char)           
              image_schar0 = Image.open(BytesIO(responses[0]))
              x_pos = 83 if charactert.costume is not None else -342
              image_app.paste(image_schar0, (x_pos, 0), mask=image_schar0)
              image_main = Image.open(BytesIO(responses[6])).convert("RGBA")
              image_app.paste(image_main, (0, 0), mask=image_main)
              draw.text((325, 4), (f"{charactert.name}  \nBFF.{charactert.friendship_level}  \nlv.{charactert.level}/{charactert.max_level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255))  #level0
              draw.text((1128, 812), f"{data.player.nickname} \nUID:{uid}  AR:{data.player.level}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255)) #player name ,level player
              # Chèn thông tin vũ khí
              image_vk0 = Image.open(BytesIO(responses[1])).convert("RGBA").resize((144, 124))
              image_app.paste(image_vk0, (958, 19), mask=image_vk0)
              draw.text((1121, 16), weapon.name if len(weapon.name) < 23 else weapon.name + "...", font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255)) #name
              draw.text((1121, 108), (f"R{weapon.refinement}"), font=font, fill=(255, 255, 255)) #tinh luyện
              draw.text((1264, 108), (f"{weapon.level}/{weapon.max_level}"), font=font, fill=(255, 255, 255)) #level
              draw.text(((973, 114)) if weapon.rarity == 5 else (986, 114), (f"{'★'*weapon.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 0))#rate
              draw.text((1190, 60), (f"{round(weapon.stats[0].value)}"), font=font, fill=(255, 255, 255))#atk#dòng chính
              icon_st = await licon(weapon.stats[1].type.value)
              image_vk0 = Image.open(BytesIO(icon_st)).convert("RGBA").resize((44, 41))
              image_app.paste(image_vk0, (1290, 57), mask=image_vk0)
              draw.text((1350, 60), f"{weapon.stats[1].formatted_value}", font=font, fill=(255, 255, 255)) 
              #stats
              dmg_bonut = charactert.highest_dmg_bonus_stat
              stat_infos = [
                  (("HP: ", FightPropType.FIGHT_PROP_MAX_HP), (970, 220-30), (40, 40)),
                  (("Tấn Công: ", FightPropType.FIGHT_PROP_CUR_ATTACK), (970, 255-30), (40, 40)),
                  (("Phòng Ngự: ", FightPropType.FIGHT_PROP_CUR_DEFENSE), (970, 295-30), (40, 40)),
                  (("Tinh Thông Nguyên Tố: ", FightPropType.FIGHT_PROP_ELEMENT_MASTERY), (970, 335-30), (40, 40)),
                  (("Tỉ Lệ Bạo: ", FightPropType.FIGHT_PROP_CRITICAL), (970, 375-30), (40, 40)),
                  (("Sát Thương Bạo: ", FightPropType.FIGHT_PROP_CRITICAL_HURT), (970, 415-30), (40, 40)),
                  (("Hiệu Quả Nạp: ", FightPropType.FIGHT_PROP_CHARGE_EFFICIENCY), (970, 455-30), (40, 40)),
                  (("Trị Liệu: ", FightPropType.FIGHT_PROP_HEAL_ADD), (970, 495-30), (40, 40)),
                  ((f"{dmg_bonut.name}.", dmg_bonut.type), (970, 535-30), (40, 40)),
              ]                
              current_position = (1016, 190)
              txtx = 0
              for o, stat_info in enumerate(stat_infos[:9]):
                stat_value = charactert.stats[stat_info[0][1]]
                draw.text(current_position, (f"{stat_info[0][0]}{stat_value.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 25), fill=(255, 255, 255))                         
                icon_image = Image.open(BytesIO(await licon(stat_value.type.name))).convert("RGBA").resize(stat_info[2])
                image_app.paste(icon_image, stat_info[1], mask=icon_image)
                current_position = (current_position[0], current_position[1] + 40)
                txtx += 1
              #tdv
              artifact_counts = {}
              for artifact in charactert.artifacts[:5]:
                  artifact_name_set = artifact.set_name
                  artifact_counts[artifact_name_set] = artifact_counts.get(artifact_name_set, 0) + 1
              sorted_counts = dict(sorted(artifact_counts.items(), key=lambda item: item[1], reverse=True))
              y_position, y_offset = 1011, 589
              for set_name, count in sorted_counts.items():
                  if count >= 2 and count < 4:
                      draw.text((1014, y_position), f"{set_name} x{count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(0, 205, 102))
                      y_position += y_offset
                  elif count >= 4:
                      draw.text((1011, 599), f"{set_name} x{count}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(0, 205, 102))
              y_cv1, y_tdv_levels = 12, 30             
              x_tdv, x_tdv_icon, x_tdv_level = 177, 27, 40
              x_tdv_rate, x_tdv_stats = 140, 4
              y_tdv_stats2 = 30
              count_tdv = 0
              for artifact in charactert.artifacts[:5]:
                  response = await fetch_image(session, artifact.icon)
                  image_tdv0 = Image.open(BytesIO(response)).resize((165, 165))
                  image_app.paste(image_tdv0, (3, x_tdv_icon), mask=image_tdv0)               
                  response = await licon(artifact.main_stat.type.value)
                  image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((50, 50))
                  image_app.paste(image_tdv0, (269, x_tdv_stats), mask=image_tdv0)                              
                  draw.text((14, x_tdv_rate), (f"{'★'*artifact.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 0))
                  draw.text((112, x_tdv_stats), (f"{artifact.main_stat.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 28), fill=(255, 255, 250))
                  x_tdv_icon += x_tdv
                  x_tdv_rate += x_tdv
                  crit_dmg, crit_rate = 0, 0
                  for substate in artifact.sub_stats[:4]:
                      response = await licon(substate.type.value)
                      image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((40, 40))
                      image_app.paste(image_tdv0, (142, x_tdv_stats+36), mask=image_tdv0)                      
                      occurrence = await count_occurrences(float(substate.formatted_value.replace('%', '')), substate.type.value)
                      draw.text((142+42, x_tdv_stats+44), (f"+{substate.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=((255, 255, 255) if occurrence >= 2 else (170, 170, 170)))
                      draw.text((142+125, x_tdv_stats+48), (f"{'*'*occurrence}"), font=ImageFont.truetype("zh-cn.ttf", 21), fill=((255, 255, 255) if occurrence >= 2 else (170, 170, 170)))     
                      x_tdv_stats += y_tdv_stats2   
                      count_tdv += 1
                      if count_tdv % 4 == 0: 
                          x_tdv_level += 177
                          x_tdv_stats = x_tdv_level - 36                  
                      crit_rate = substate.value if substate.name == "Tỷ Lệ Bạo Kích" else crit_rate
                      crit_dmg = substate.value if substate.name == "ST Bạo Kích" else crit_dmg
                  cv0 = crit_rate * 2 + crit_dmg
                  color = (
                      (208, 59, 84) if cv0 >= 50
                      else (203, 208, 59) if 42 <= cv0 <= 49
                      else (208, 59, 208) if 32 <= cv0 <= 41
                      else (59, 123, 208) if 18 <= cv0 <= 31
                      else (210, 221, 236)
                  )
                  fills = (0, 0, 0) if color in [(210, 221, 236), (203, 208, 59)] else (255, 255, 255)
                  draw.rounded_rectangle([19 - 5, y_cv1 - 5, 19 + 68 + 5, y_cv1 + 18 + 5], 10, fill=color)
                  draw.text((19, y_tdv_levels), f"+{artifact.level}", font=ImageFont.truetype("zh-cn.ttf", 23), fill=(255, 255, 255))
                  draw.text((17 + 1, y_cv1 + 1), f"{cv0:.1f}CV", font=ImageFont.truetype("zh-cn.ttf", 17), fill=fills)
                  y_tdv_levels += 177
                  y_cv1 += 177
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
              image_url = base64.b64encode(buffer.getvalue()).decode()
              file_url = await upload_img(image_url, session)
              return file_urlurl

class Select(discord.ui.Select):
    def __init__(self, *args, **kwargs):
        self.data = global_data.get("data")
        self.channel = inset_message.get('channelt')
        super().__init__(*args, **kwargs)
        options = [
            discord.SelectOption(label=char.name, value=f"char{i+1}") for i, char in enumerate(self.data.characters)
        ]
        super().__init__(placeholder="showcare", max_values=1, min_values=1, options=options)
    async def callback(self, Interaction: discord.Interaction):
        async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
            char_index = int(self.values[0][-1]) - 1
            charactert = self.data.characters[char_index]
            messagea = inset_message.get("message")
            now = datetime.datetime.now()
            embed_loading = discord.Embed(title="<a:aloading:1152869299942338591> **Đang tạo thông tin..__Hãy kiên nhẫn__** <a:ganyurollst:1118761352064946258>", color=discord.Color.yellow())
            await Interaction.response.edit_message(content=None, embed=embed_loading)
            embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.datetime.now())
            reload_time = now + datetime.timedelta(seconds=self.data.ttl)
            embed.add_field(name=f"Name.{charactert.name}", value=f"Level.{charactert.level} \nnguyên tố.{charactert.element} C.{len(charactert.constellations)} \nLàm mới: <t:{int(reload_time.timestamp())}:R>", inline=False) 
            embed.set_thumbnail(url=f"{charactert.icon.front}")
            embed.set_footer(text="", icon_url=f"{Interaction.user.avatar}")
            file_url = await image_dcuid(charactert)
            embed.set_image(url=file_url)
            await messagea.edit(content=None, embed=embed)
 
class SelectView(discord.ui.View):
    def __init__(self, *, timeout=300):
        super().__init__(timeout=timeout)
        self.add_item(Select())
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
        urlgoc = await fetch_image(session, 'https://media.discordapp.net/attachments/1107978903294853140/1206074586098176010/F7C59933-6074-48A1-8422-A66E5B12B81F.png?ex=65daaf7d&is=65c83a7d&hm=bf8a3b1baedfa274063937d09302701f079f5691e37a88261013e7e44067f11a&')
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
            if char.costume is not None:
              m = char.costume.icon.circle
            else:
              m = char.icon.circle
            char_icon_data = await fetch_image(session, m)
            char_icon = Image.open(BytesIO(char_icon_data)).convert("RGBA").resize((80, 80))
            char_icon_datak = await fetch_image(session, char.namecard.full)
            char_imaget = Image.open(BytesIO(char_icon_datak)).convert("RGBA").resize((279, 104))
            url_goc = await fetch_image(session, 'https://media.discordapp.net/attachments/1107978903294853140/1205793445000511488/Khong_Co_Tieu_e137_20240210152124-removebg-preview.png?ex=65d9a9a7&is=65c734a7&hm=2442e609a8b315270789d41b02fc316c4e412cdb1782035ce2736c2b67f2aade&')
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
        image_url = base64.b64encode(buffer.getvalue()).decode()
        file_url = await upload_img(image_url, session)
        return file_url

class buttons(discord.ui.View):
  def __init__ (self, *, timeout=300):
    super().__init__(timeout=timeout) 

  @discord.ui.button(label="showcare", style=discord.ButtonStyle.gray)
  async def my_button(self, Interaction: discord.Interaction, button: discord.ui.button):
   await Interaction.response.send_message("tesr")

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
        user_id = str(Interaction.user.id)
        if uid is not None:
          uid = uid
        elif user is not None:
              uid = data[str(user.id)]["uid"] if str(user.id) in data else 831335714
        else:
              uid = data[user_id]["uid"] if str(user_id) in data else 831335714
        data = await api.fetch_showcase(uid)
        global_data["data"] = data
        global_data["uid"] = uid
        embed = discord.Embed()
        embed.add_field(name="vui lòng đợi thông tin được sử lý", value="", inline=False)
        await Interaction.response.send_message(embed=embed, ephemeral=True)
        if data.characters is not None and len(data.characters) > 0:
          file_url= await generate_image(data)
          message = await Interaction.channel.send(file_url, view=SelectView())
          inset_message["message"] = message
        else:
          embed1 = discord.Embed(color=0xed0202)
          embed1.add_field(name="lỗi", value="Không tìm thấy dữ liệu cho người dùng này.", inline=False)
          embed1.add_field(name="Chuyện gì đã xảy ra?", value="Vấn đề thường gặp nhất với lỗi này đó là tài khoản bạn đang tìm kiếm chưa công khai Hồ sơ. Để sửa lỗi này, hãy bật tùy chọn ``Hiển thị chi tiết nhân vật`` trong giao diện Hồ sơ Genshin của bạn. Hãy tham khảo hình ảnh bên dưới \n\n```Hoặc bạn đang sửa dụng Biến User Hoặc không sửa dụng biến khi Bạn hoặc User không có dữ liệu UID```", inline=False)
          embed1.set_image(url="https://cdn.discordapp.com/attachments/969461764704059392/1000843651863285810/unknown.png")
          await Interaction.followup.send(embed=embed1, ephemeral=True)
     except Exception as s:
        await channel.send(f"Error: {s}")

async def setup(bot):
  await bot.add_cog(scuids(bot))