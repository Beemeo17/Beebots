import discord
from discord.ext import commands, tasks
from discord import app_commands, PartialEmoji
import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, time
import aiohttp
import enka
import asyncio
import traceback
from enka.enums import FightPropType, Language
import operator

global_data = {
    "data": None,
    "uid": None
}
inset_message = {'message' :None, "channelt": None}
emoji_list = []
class Select(discord.ui.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = global_data.get("data")
        options = [
            discord.SelectOption(label=char.name, value=f"char{i+1}") for i, char in enumerate(data.characters)
        ]
        super().__init__(placeholder="showcare", max_values=1, min_values=1, options=options)

    async def callback(self, Interaction: discord.Interaction):
        async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
            try:
                uid = global_data.get("uid")
                data = await api.fetch_showcase(uid)
                channel = inset_message.get('channelt')

                embed_loading = discord.Embed(color=discord.Color.yellow())
                embed_loading.add_field(name="<a:aloading:1152869299942338591> **Đang tạo thông tin..** <a:ganyurollst:1118761352064946258>", value="", inline=False)
                await Interaction.response.edit_message(content=None, embed=embed_loading)

                char_index = int(self.values[0][-1]) - 1
                charactert = data.characters[char_index]

                url_goc = "https://media.discordapp.net/attachments/1107978903294853140/1203237852570193930/Khong_Co_Tieu_e117_20240203141707.png"
                response = requests.get(url_goc)
                ime_app = BytesIO(response.content)
                image_app = Image.open(ime_app).convert("RGBA").resize((1141, 1134))
                font = ImageFont.truetype("zh-cn.ttf", 27)
                draw = ImageDraw.Draw(image_app)
        
                draw.text((38, 24), data.player.nickname, font=font, fill=(255, 255, 255)) #player name
                draw.text((38, 51), (f"UID:{uid}  AR:{data.player.level}"), font=font, fill=(255, 255, 255)) #player level
        
                #char
                response = requests.get(charactert.icon.gacha)
                image_set_schar0 = BytesIO(response.content)
                image_schar0 = Image.open(image_set_schar0).resize((744, 352))
                image_app.paste(image_schar0, (-120, 95), mask=image_schar0)
                draw.text((34, 540), charactert.name, font=font, fill=(255, 255, 255))  #name0
                draw.text((34, 607), (f"Level:{charactert.level} / {charactert.max_level}"), font=font, fill=(255, 255, 255))  #level0
                draw.text((34, 575), (f"Độ Yêu Thích: {charactert.friendship_level}"), font=font, fill=(255, 255, 255))  #độ yêu thích
        
                #vũ khí
                weapon = charactert.weapon
                response = requests.get(weapon.icon)
                image_set_vk0 = BytesIO(response.content)
                image_vk0 = Image.open(image_set_vk0).resize((144, 124))
                image_app.paste(image_vk0, (650, 33), mask=image_vk0)
        
                draw.text((820, 36), weapon.name, font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255)) #name
                draw.text((644, 33), (f"R{weapon.refinement}"), font=font, fill=(255, 255, 255)) #tinh luyện
                draw.text((970, 104), (f"{weapon.level}/{weapon.max_level}"), font=font, fill=(255, 255, 255)) #level
                draw.text((677, 146), (f"{'*'*weapon.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 38), fill=(255, 255, 0))#rate
                draw.text((842, 104), (f"{round(weapon.stats[0].value)}"), font=font, fill=(255, 255, 255))#atk#dòng chính
                if weapon.stats[1].name == "Hiệu Quả Nạp Nguyên Tố":
                    stat_name = weapon.stats[1].name.strip()[:12]
                else:
                    stat_name = weapon.stats[1].name
                draw.text((812, 150), f"{stat_name}: {weapon.stats[1].formatted_value}", font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))
                
                #stats
                characterp = charactert.stats
                FightProp = FightPropType
                fontt = ImageFont.truetype("zh-cn.ttf", 25)
                
                stat_infos = [
                    (("HP", FightProp.FIGHT_PROP_CUR_HP), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990290942951545/CHUH17121.png", (644, 245), (40, 40)),
                    (("Tấn Công", FightProp.FIGHT_PROP_CUR_ATTACK), "https://media.discordapp.net/attachments/1118977913392476210/1118990421289357452/atk.png", (644, 280), (40, 40)),
                    (("Phòng Ngự", FightProp.FIGHT_PROP_CUR_DEFENSE), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990526595727501/THFM69251.png", (644, 320), (40, 40)),
                    (("Tinh Thông Nguyên Tố", FightProp.FIGHT_PROP_ELEMENT_MASTERY), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990526247608361/ttnt.png", (644, 360), (40, 40)),
                    (("Tỉ Lệ Bạo", FightProp.FIGHT_PROP_CRITICAL), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990420903477248/cr.png", (644, 400), (40, 40)),
                    (("Sát Thương Bạo", FightProp.FIGHT_PROP_CRITICAL_HURT), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990421582954577/cd.png", (644, 440), (40, 40)),
                    (("Hiệu Quả Nạp", FightProp.FIGHT_PROP_CHARGE_EFFICIENCY), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990525501022218/hqn.png", (644, 480), (40, 40)),
                    (("Trị Liệu", FightProp.FIGHT_PROP_HEAL_ADD), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990525794619402/heal.png", (644, 520), (40, 40)),
                ]
                current_position = (688, 250)
                for stat_info in stat_infos:
                    stat_name = stat_info[0][0]
                    stat_value = characterp[stat_info[0][1]].formatted_value
                    icon_url = stat_info[1]
                    icon_position = stat_info[2]
                    icon_size = stat_info[3]
                
                    draw.text(current_position, (f"{stat_name}: {stat_value}"), font=fontt, fill=(255, 255, 255))
                
                    response = requests.get(icon_url)
                    icon = BytesIO(response.content)
                    icon_image = Image.open(icon).resize(icon_size)
                    image_app.paste(icon_image, icon_position, mask=icon_image)
                
                    current_position = (current_position[0], current_position[1] + 40)
                #stnt
                stnt_infos = [
                    (("Vật Lý", FightProp.FIGHT_PROP_PHYSICAL_ADD_HURT), "https://cdn.discordapp.com/attachments/1092394580009295952/1119211230872211476/350.png", (644, 565), (50, 50)),
                    (("Gió", FightProp.FIGHT_PROP_WIND_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026021228544.webp?size=96&quality=lossless", (766, 565), (50, 50)),
                    (("Đá", FightProp.FIGHT_PROP_ROCK_ADD_HURT), "https://cdn.discordapp.com/emojis/882253025895399504.webp?size=96&quality=lossless", (879, 565), (50, 50)),
                    (("Điện", FightProp.FIGHT_PROP_ELEC_ADD_HURT), "https://cdn.discordapp.com/emojis/882254148584759317.webp?size=96&quality=lossless", (993, 565), (50, 50)),
                    (("Thảo Mộc", FightProp.FIGHT_PROP_GRASS_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026113507349.webp?size=96&quality=lossless", (644, 625), (50, 50)),
                    (("Nước", FightProp.FIGHT_PROP_WATER_ADD_HURT), "https://cdn.discordapp.com/emojis/882254676916068393.webp?size=96&quality=lossless", (766, 625), (50, 50)),
                    (("Lửa", FightProp.FIGHT_PROP_FIRE_ADD_HURT), "https://cdn.discordapp.com/emojis/882254077361262592.webp?size=96&quality=lossless", (879, 625), (50, 50)),
                    (("Băng", FightProp.FIGHT_PROP_ICE_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026046390292.webp?size=96&quality=lossless", (993, 625), (50, 50)),
                ]
                znt = 578
                xnt = [694, 816, 929, 1043]
                tntp = 0
                txtx = 0
                for stnt_info in stnt_infos:
                    stnt_name = stnt_info[0][0]
                    stnt_value = characterp[stnt_info[0][1]].formatted_value
                    stnt_icon_url = stnt_info[1]
                    stnt_icon_position = stnt_info[2]
                    stnt_icon_size = stnt_info[3]
                    if txtx < 4:
                        draw.text((xnt[txtx], znt), (f"{stnt_value.rstrip('0')}"), font=fontt, fill=(255, 255, 255))
                    else:
                        txtx = 0
                        draw.text((xnt[txtx], znt), (f"{stnt_value.rstrip('0')}"), font=fontt, fill=(255, 255, 255))
                    txtx += 1
                    stnt_response = requests.get(stnt_icon_url)
                    stnt_icon = BytesIO(stnt_response.content)
                    stnt_icon_image = Image.open(stnt_icon).resize(stnt_icon_size)
                    image_app.paste(stnt_icon_image, stnt_icon_position, mask=stnt_icon_image)
                    tntp += 1
                    if tntp == 4 and tntp < 9:
                        znt += 63
                
                #tdv
                fonts = ImageFont.truetype("zh-cn.ttf", 16)
        
                artifact_counts = {}
                for artifact in charactert.artifacts:
                    artifact_name_set = artifact.set_name
                    if artifact_name_set in artifact_counts:
                        artifact_counts[artifact_name_set] += 1
                    else:
                        artifact_counts[artifact_name_set] = 1
                sorted_counts = dict(sorted(artifact_counts.items(), key=operator.itemgetter(1), reverse=True))
                y_position = 672
                y_offset = 28
                #set tdv
                for set_name, count in sorted_counts.items(): 
                    if count >= 2 and count < 4:
                      draw.text((95, y_position), f"{set_name} {count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(0, 205, 102))
                      y_position += y_offset
                    if count >= 4:
                      draw.text((95, 685), f"{set_name} {count}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(0, 205, 102))
                #cv      
                x_cv1 = 158
                x_cv2 = 224
                sss = 0
                crit_rate = 0
                crit_dmg = 0
                
                st_bao = 0
                tl_bao = 0
                hqn = 0
                ttnt = 0
                atk1 = 0
                atk2 = 0
                hp1 = 0
                hp2 = 0
                def1=0
                def2=0
                x_tdv_levels = 166
                for artifact in charactert.artifacts:
                    crit_rate -= crit_rate
                    crit_dmg -= crit_dmg
                    for substate in artifact.sub_stats:
                     if substate.name == "Tỷ Lệ Bạo Kích" or substate.name == "ST Bạo Kích":
                      if substate.name == "Tỷ Lệ Bạo Kích":
                        crit_rate += substate.value 
                      elif substate.name == "ST Bạo Kích":
                        crit_dmg += substate.value 
                      else:
                        return
                    cv0 = (crit_rate) * 2 + crit_dmg
                    draw.text((x_cv1, 900), (f"{cv0:.1f}CV"), font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))
                    text = (f"+{artifact.level}")
                    text_font = ImageFont.truetype("zh-cn.ttf", 23)
                    text_bbox = draw.textbbox((0, 0), text, font=text_font) 
                    box_padding = 1
                    box_width = text_bbox[2] - text_bbox[0] + 2 * box_padding
                    box_height = text_bbox[3] - text_bbox[1] + 2 * box_padding     
                    x = x_tdv_levels
                    y = 876
                    if int(cv0) >= 50:
                        color = (208, 59, 84)
                    elif int(cv0) >= 42 and int(cv0) <= 49:
                        color = (203, 208, 59)
                    elif int(cv0) >= 32 and int(cv0) <= 41:
                        color = (208, 59, 208)
                    elif int(cv0) >= 18 and int(cv0) <= 31:
                        color = (59, 123, 208)
                    else:
                        color = (210, 221, 236)                       
                    if color == (210, 221, 236):
                        fills= (0, 0, 0)
                    elif color == (203, 208, 59):
                        fills= (0, 0, 0)
                    else:
                        fills= (255, 255, 255)
                    draw.rounded_rectangle([x - 5, y - 5, x + box_width + 5, y + box_height + 5], 10, fill=color)
                    draw.text((x + box_padding, y + box_padding), text, font=text_font, fill=fills)                  
                    x_tdv_levels += 227
                    sss += 1
                    if sss <= 3:
                      x_cv1 += x_cv2
                    else:
                      x_cv1 += 226
        
                    for substate in artifact.sub_stats:
                      if substate.name == "Tỷ Lệ Bạo Kích":
                        tl_bao += substate.value 
                      elif substate.name == "ST Bạo Kích":
                        st_bao += substate.value 
                      elif substate.name == "Tinh Thông Nguyên Tố":
                        ttnt += substate.value
                      elif substate.name == "Hiệu Quả Nạp Nguyên Tố":
                        hqn += substate.value
                      elif substate.name == "HP":
                        if substate.is_percentage:
                            hp1 += substate.value
                        else:
                          hp2  += substate.value
                      elif substate.name == "Phòng Ngự":
                        if substate.is_percentage:
                            def1 += substate.value
                        else:
                           def2 += substate.value
                      elif substate.name == "Tấn Công":
                        if substate.is_percentage:
                            atk1 += substate.value
                        else:
                           atk2 += substate.value
                      else: 
                       return
                cv_a = (tl_bao * 2) + st_bao
                draw.text((16, 1083), (f"TLbạo:{tl_bao:.1f}% | STbạo:{st_bao:.1f}% | ttnt:{int(ttnt)} | hqn:{hqn}% | atk:{atk1:.1f}% | atk:{int(atk2)} | HP:{hp1:.1f}% | HP:{int(hp2)} | def:{def1:.1f}% | def:{int(def2)}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=(255, 255, 255))
        
                x_tdv = 227 #x tổng
                x_tdv_stats1 = 224
                x_tdv_icon = 43 #icon tdv
                x_tdv_level = 166
                x_tdv_rate = 30 #độ hiếm tdv
                x_tdv_stats = 26 #stats tdv
                y_tdv_stats1 = 967 #y stats tdv
                y_tdv_stats2 = 25 
                element_count = 0 #chia bảng 
                for artifact in charactert.artifacts:
                  response = requests.get(artifact.icon)
                  image_set_tdv0 = BytesIO(response.content)
                  image_tdv0 = Image.open(image_set_tdv0).resize((165, 165))
                  image_app.paste(image_tdv0, (x_tdv_icon, 756), mask=image_tdv0)
                  x_tdv_icon += x_tdv
        
                  draw.text((x_tdv_rate, 896), (f"{'*'*artifact.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 38), fill=(255, 255, 0))
                  x_tdv_rate += x_tdv
        
                  draw.text((x_tdv_stats, 932), artifact.main_stat.name, font=fonts, fill=(255, 255, 255))

                    
                  text = (f"+{artifact.level}")
                  text_font = ImageFont.truetype("zh-cn.ttf", 23)
                  text_bbox = draw.textbbox((0, 0), text, font=text_font) 
                  box_padding = 1
                  box_width = text_bbox[2] - text_bbox[0] + 2 * box_padding
                  box_height = text_bbox[3] - text_bbox[1] + 2 * box_padding     
                  x = x_tdv_level
                  y = 877
  
                  x_tdv_level += x_tdv
                  for substate in artifact.sub_stats:
                    if substate.name == "Hiệu Quả Nạp Nguyên Tố":
                      name_sst = substate.name.strip()[:12]
                    elif substate.name == "Tinh Thông Nguyên Tố":
                      name_sst = substate.name.strip()[:10]
                    else:
                      name_sst = substate.name
                    
                    draw.text((x_tdv_stats, y_tdv_stats1), (f"{name_sst} {substate.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=(255, 255, 255))
                    y_tdv_stats1 += y_tdv_stats2
                    element_count += 1
                    if element_count % 4 == 0:
                      y_tdv_stats1 = 973
                      x_tdv_stats += x_tdv_stats1    
        
                #thiên phú
                response = requests.get(charactert.talents[0].icon)  #skill1
                image_set_skill00 = BytesIO(response.content)
                image_skill00 = Image.open(image_set_skill00).resize((60, 60))
                image_app.paste(image_skill00, (532, 15), mask=image_skill00)
        
                response = requests.get(charactert.talents[1].icon)  #skill2
                image_set_skill01 = BytesIO(response.content)
                image_skill01 = Image.open(image_set_skill01).resize((60, 60))
                image_app.paste(image_skill01, (532, 84), mask=image_skill01)
        
                response = requests.get(charactert.talents[2].icon)  #skill3
                image_set_skill02 = BytesIO(response.content)
                image_skill02 = Image.open(image_set_skill02).resize((60, 60)).convert('RGBA')
                image_app.paste(image_skill02, (532, 150), mask=image_skill02)
                draw.text((534, 47), (f"     {charactert.talents[0].level}"),font=font,fill=(255, 255, 255))
                draw.text((534, 114), (f"     {charactert.talents[1].level}"),font=font,fill=(255, 255, 255))
                draw.text((534, 182), (f"     {charactert.talents[2].level}"),font=font,fill=(255, 255, 255))
        
                #cm
                Locks = 6 - (len(charactert.constellations))
                x_lock = 532
                y_lock = 569
                for _ in range(Locks):
                  response = requests.get('https://media.discordapp.net/attachments/1114095095210311680/1151759944278884352/R.png')
                  image_set_skill00 = BytesIO(response.content)
                  image_skill00 = Image.open(image_set_skill00).resize((60, 60))
                  image_app.paste(image_skill00, (x_lock, y_lock), mask=image_skill00)
                  y_lock -= 65
        
                lock = len(charactert.constellations)
                inseta = 244
                y_ts = [65,66,63,64,65]
                for k in range(lock):
                  constellation = charactert.constellations[k]
                  response = requests.get(constellation.icon) #skill1
                  image_set_skill00 = BytesIO(response.content)
                  image_skill00 = Image.open(image_set_skill00).resize((60, 60))
                  image_app.paste(image_skill00, (532, inseta), mask=image_skill00)
                  tert = y_ts[k % len(y_ts)]
                  inseta += tert
        
                buffer = BytesIO()
                image_app.save(buffer, format='png')
                buffer.seek(0)
                file = discord.File(buffer, filename="showcase.png")
                channel = inset_message.get("channelt")
                messaget = await channel.send(file=file)
                file_url = messaget.attachments[0]
                embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.now())
                embed.add_field(name=f"Name.{charactert.name}", value=f"Level.{charactert.level} \nnguyên tố.{charactert.element} C.{len(charactert.constellations)} \nLàm mới:{data.ttl}", inline=False)
                embed.set_image(url=file_url)   
                embed.set_thumbnail(url=f"{charactert.icon.front}")
                embed.set_footer(text=f"{uid}", icon_url=f"{Interaction.user.avatar}")
                messagea = inset_message.get("message")
                await messagea.edit(content=None, embed=embed)
            except Exception as e:
                traceback.print_exc()
                await channel.send(f"Error: {e}\n{traceback.format_exc()}")


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


class buttons(discord.ui.View):
  def __init__ (self, *, timeout=300):
    super().__init__(timeout=timeout) 

  @discord.ui.button(label="showcare", style=discord.ButtonStyle.gray)
  async def my_button(self, Interaction: discord.Interaction, button: discord.ui.button):
    embed=discord.Embed()
    embed.add_field(name="hãy chọn 1 options",value="__nếu tương tác không thành công vui lòng đợi 1 đến 2 giây \n**và ko cần chọn lại**__")
    await Interaction.response.edit_message(embed=embed, view=SelectView())


class scuids(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession()
  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  @app_commands.command(name="scuid", description="check dữ liệu uid genshin")
  async def scuid(self, Interaction, uid: int):
    async with enka.EnkaAPI() as api:
     try:
        uid = uid
        data = await api.fetch_showcase(uid)
        global_data["data"] = data
        global_data["uid"] = uid

        url_goc = 'https://cdn.discordapp.com/attachments/1093887180096671824/1100077580008312922/Khong_Co_Tieu_e36_20230424221522.png'
        response = requests.get(url_goc)
        ime_app = BytesIO(response.content)
        image_app = Image.open(ime_app).convert("RGBA")

        font = ImageFont.truetype("zh-cn.ttf", 14)
        draw = ImageDraw.Draw(image_app)
        emoji_thanhtuu = discord.utils.get(self.bot.emojis, name="thanhtuu_beebot")
        emoji_lahoan = discord.utils.get(self.bot.emojis, name="lahoan_beebot")
        emoji_owo = discord.utils.get(self.bot.emojis, name="kiemanh")
        emoji_enka = discord.utils.get(self.bot.emojis, name="enka_beebot")
        emoji_aspirine = discord.utils.get(self.bot.emojis, name="aspirine_beebot")
        embed = discord.Embed()
        embed.add_field(name="vui lòng đợi thông tin được sử lý", value="", inline=False)
        await Interaction.response.send_message(embed=embed, ephemeral=True)
        if data.characters is not None and len(data.characters) > 0:
            for i in range(min(len(data.characters), 8)):
                char = data.characters[i]
        
                # Character info
                response = requests.get(char.icon.circle)
                image_set_char = BytesIO(response.content)
                image_char = Image.open(image_set_char).resize((50, 50))
                image_app.paste(image_char, ((i % 4) * 181 + 10, (i // 4) * 154 + 57), mask=image_char)
        
                draw.text(((i % 4) * 181 + 14, (i // 4) * 154 + 119), char.name, font=font, fill=(0, 0, 0))
                draw.text(((i % 4) * 181 + 63, (i // 4) * 154 + 77),
                          f"level:{char.level}     C {len(char.constellations)}", font=font, fill=(0, 0, 0))
        
                # Character skills
                for j, talent in enumerate(char.talents[:3]):
                    response = requests.get(talent.icon)
                    image_set_skill = BytesIO(response.content)
                    image_skill = Image.open(image_set_skill).resize((20, 20)).convert('RGBA')
                    image_app.paste(image_skill, ((i % 4) * 181 + 61 + j * 40, (i // 4) * 154 + 94), mask=image_skill)
                    draw.text(((i % 4) * 181 + 61 + j * 40, (i // 4) * 154 + 95), f"     {talent.level}",
                              font=font, fill=(255, 255, 255))
        else:
            embed1 = discord.Embed(color=0xed0202)
            embed1.add_field(name="lỗi", value="Không tìm thấy dữ liệu cho người dùng này.", inline=False)
            embed1.add_field(
                name="Chuyện gì đã xảy ra?",
                value="Vấn đề thường gặp nhất với lỗi này đó là tài khoản bạn đang tìm kiếm chưa công khai Hồ sơ. Để sửa lỗi này, hãy bật tùy chọn ``Hiển thị chi tiết nhân vật`` trong giao diện Hồ sơ Genshin của bạn. Hãy tham khảo hình ảnh bên dưới.",
                inline=False)
            embed1.set_image(
                url="https://cdn.discordapp.com/attachments/969461764704059392/1000843651863285810/unknown.png"
            )
            await Interaction.followup.send(embed=embed1, ephemeral=True)

        embed = discord.Embed(color=0x0ad2f5)
        author_name = f"{Interaction.user.name}#{Interaction.user.discriminator}"
        embed.set_author(name=author_name, icon_url=Interaction.user.avatar)
        embed.add_field(name='✨===Player°Info===✨', value="", inline=False)
        embed.add_field(
          name=f"`UID:`||{uid}||  {str(emoji_owo)}  `AR` {data.player.level}",
          value="",
          inline=False)

        embed.set_thumbnail(url=f"{data.player.namecard.full}")
        embed.add_field(name=f"`name:` **{data.player.nickname}**",
                        value=f"",
                        inline=False)

        embed.add_field(name=f"`chữ ký:` {data.player.signature}",
                        value='',
                        inline=False)

        embed.add_field(
          name='',
          value=f' {str(emoji_thanhtuu)} `Thành Tựu:` **{data.player.achievements}**',
          inline=True)

        embed.add_field(
          name='',
          value=
          f' {str(emoji_lahoan)} `La Hoàn:` **{data.player.abyss_floor} - {data.player.abyss_level}**',
          inline=True)

        embed.add_field(name="✨=characters°preview=✨", value="", inline=False)

        embed.add_field(
          name="",
          value=
          f" {str(emoji_enka)}[chi tiết char](https://enka.network/u/{uid}/) • {str(emoji_aspirine)}[tính dame char](https://genshin.aspirine.su/#uid{uid})",
          inline=False)

        buffer = BytesIO()
        image_app.save(buffer, format='png')
        buffer.seek(0)
        filet = discord.File(buffer, filename="output.png")      
        channel = self.bot.get_channel(1118977913392476210)
        inset_message["channelt"] = channel
        saved_file = await channel.send(file=filet)
        files_url = saved_file.attachments[0]
        embed.set_image(url=files_url)
        message = await Interaction.channel.send(embed=embed, view=buttons())
        inset_message["message"] = message
     except Exception as s:
        await Interaction.channel.send(s)
        return s

async def setup(bot):
  await bot.add_cog(scuids(bot))
