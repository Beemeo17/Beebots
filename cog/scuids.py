import discord
from discord.ext import commands, tasks
from discord import app_commands, PartialEmoji
import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, time
import aiohttp
import enka
import asyncio
import traceback

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
        options = []
        TSS = 0
        for _ in data.characters:
          TSS +=1
        for i in range(min(len(data.characters), TSS)):
          char = data.characters[i]
          options.append(discord.SelectOption(label=char.name, value=f"char{i+1}"))
        super().__init__(placeholder="showcare", max_values=1, min_values=1, options=options)
    async def callback(self, Interaction: discord.Interaction):
     async with enka.EnkaAPI() as api:
       try:
        uid = global_data.get("uid")
        data = await api.fetch_showcase(uid)
        channel = inset_message.get('channelt')
      
        embed_loading = discord.Embed(color=discord.Color.yellow())
        embed_loading.add_field(name="<a:aloading:1152869299942338591> **Đang tạo thông tin..** <a:ganyurollst:1118761352064946258>",value="", inline=False)
        await Interaction.response.edit_message(content=None, embed=embed_loading)
        embed=discord.Embed()
        if self.values[0] == "char1":
            charactert = data.characters[0]              
        elif self.values[0] == "char2":
            charactert = data.characters[1]  
        elif self.values[0] == "char3":
            charactert = data.characters[2]             
        elif self.values[0] == "char4":
            charactert = data.characters[3]
        elif self.values[0] == "char5":
            charactert = data.characters[4]
        elif self.values[0] == "char6":
            charactert = data.characters[5]
        elif self.values[0] == "char7":
            charactert = data.characters[6]
        elif self.values[0] == "char8":
            charactert = data.characters[7]  
        embed.add_field(name=f"name: {charactert.name}", value=f"độ yêu thích: {charactert.friendship_level}", inline=False)
        embed.add_field(name=f"level: {charactert.level} / 90", value="", inline=False)
        embed.set_thumbnail(url=charactert.icon)

        url_goc = "https://media.discordapp.net/attachments/1107978903294853140/1151815890334134303/Khong_Co_Tieu_e62_20230914164310.png"
        response = requests.get(url_goc)
        ime_app = BytesIO(response.content)
        image_app = Image.open(ime_app).convert("RGBA").resize((1141, 1134))

        font = ImageFont.truetype("zh-cn.ttf", 27)
        draw = ImageDraw.Draw(image_app)

        draw.text((38, 24), data.player.nickname, font=font, fill=(255, 255, 255)) #player name
        draw.text((38, 51), (f"AR:{data.player.level}"), font=font, fill=(255, 255, 255)) #player level

        #char
        response = requests.get(charactert.art)
        image_set_schar0 = BytesIO(response.content)
        image_schar0 = Image.open(image_set_schar0).resize((744, 352))
        image_app.paste(image_schar0, (-120, 95), mask=image_schar0)
        draw.text((34, 540), charactert.name, font=font, fill=(255, 255, 255))  #name0
        draw.text((34, 607), (f"Level:{charactert.level} / 90"), font=font, fill=(255, 255, 255))  #level0
        draw.text((34, 575), (f"Độ Yêu Thích: {charactert.friendship_level}"), font=font, fill=(255, 255, 255))  #độ yêu thích

        #vũ khí
        weapon = charactert.weapon
        response = requests.get(weapon.icon)
        image_set_vk0 = BytesIO(response.content)
        image_vk0 = Image.open(image_set_vk0).resize((144, 124))
        image_app.paste(image_vk0, (650, 33), mask=image_vk0)

        draw.text((820, 36), weapon.name, font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255)) #name
        draw.text((644, 33), (f"R{weapon.refinement}"), font=font, fill=(255, 255, 255)) #tinh luyện
        draw.text((970, 104), (f"{weapon.level}/90"), font=font, fill=(255, 255, 255)) #level
        draw.text((677, 146), (f"{'*'*weapon.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 38), fill=(255, 255, 0))#rate
        draw.text((842, 104), (f"{weapon.stats[0].value}"), font=font, fill=(255, 255, 255))#atk#dòng chính
        if weapon.stats[1].name == "Hiệu Quả Nạp Nguyên Tố":
              draw.text((812, 150), (f"{weapon.stats[1].name.strip()[:12]}: {weapon.stats[1].value}"), font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))
        else:
              draw.text((812, 150), (f"{weapon.stats[1].name}: {weapon.stats[1].value}"), font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))

        #Stats
        for charactert in charactert.stats:
         fontt=ImageFont.truetype("zh-cn.ttf", 25)
         draw.text((688, 250), (f"HP: {int(charactert.stats.FIGHT_PROP_HP.value)}"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990290942951545/CHUH17121.png")
         hp = BytesIO(response.content)
         hp1 = Image.open(hp).resize((40, 40))
         image_app.paste(hp1, (644, 245), mask=hp1)

         draw.text((688, 285), (f"Tân Công: {int(charactert.stats.FIGHT_PROP_ATTACK.value)}"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://media.discordapp.net/attachments/1118977913392476210/1118990421289357452/atk.png")
         atk = BytesIO(response.content)
         atk1 = Image.open(atk).resize((40, 40))
         image_app.paste(atk1, (644, 280), mask=atk1)

         draw.text((688, 325), (f"Phòng Ngự: {int(charactert.stats.FIGHT_PROP_DEFENSE.value)}"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990526595727501/THFM69251.png")
         def2 = BytesIO(response.content)
         def1 = Image.open(def2).resize((40, 40))
         image_app.paste(def1, (644, 320), mask=def1)

         draw.text((688, 365), (f"Tinh Thông Nguyên Tố: {int(charactert.stats.FIGHT_PROP_ELEMENT_MASTERY.value)}"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990526247608361/ttnt.png")
         tt = BytesIO(response.content)
         tt1 = Image.open(tt).resize((40, 40))
         image_app.paste(tt1, (644, 360), mask=tt1)

         draw.text((688, 405),(f"Tỉ Lệ Bạo: {charactert.stats.FIGHT_PROP_CRITICAL.value* 100:.0f}%"), font=font, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990420903477248/cr.png")
         tl = BytesIO(response.content)
         tl1 = Image.open(tl).resize((40, 40))
         image_app.paste(tl1, (644, 400), mask=tl1)

         draw.text((688, 445),(f"Sát Thương Bạo: {charactert.stats.FIGHT_PROP_CRITICAL_HURT.value* 100:.0f}%"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990421582954577/cd.png")
         st = BytesIO(response.content)
         st1 = Image.open(st).resize((40, 40))
         image_app.paste(st1, (644, 440), mask=st1)

         draw.text((688, 485),(f"Hiệu Quả Nạp: {charactert.stats.FIGHT_PROP_CHARGE_EFFICIENCY.value* 100:.0f}%"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990525501022218/hqn.png")
         hqn = BytesIO(response.content)
         hqn1 = Image.open(hqn).resize((40, 40))
         image_app.paste(hqn1, (644, 480), mask=hqn1)

         draw.text((688, 525),(f"trị liệu: {int(charactert.stats.FIGHT_PROP_HEAL_ADD.value * 100)}%"), font=fontt, fill=(255, 255, 255))
         response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990525794619402/heal.png")
         tl = BytesIO(response.content)
         tl1 = Image.open(tl).resize((40, 40))
         image_app.paste(tl1, (644, 520), mask=tl1)
        #stnt
         draw.text((710, 578),(f"{int(charactert.stats.FIGHT_PROP_PHYSICAL_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/attachments/1092394580009295952/1119211230872211476/350.png")
         svl = BytesIO(response.content)
         svl1 = Image.open(svl).resize((50, 50))
         image_app.paste(svl1, (660, 565), mask=svl1)

         draw.text((830, 578),(f"{int(charactert.stats.FIGHT_PROP_WIND_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882253026021228544.webp?size=96&quality=lossless")
         stp = BytesIO(response.content)
         stp1 = Image.open(stp).resize((50, 50))
         image_app.paste(stp1, (780, 565), mask=stp1)

         draw.text((940, 578),(f"{int(charactert.stats.FIGHT_PROP_ROCK_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882253025895399504.webp?size=96&quality=lossless")
         stn = BytesIO(response.content)
         stn1 = Image.open(stn).resize((50, 50))
         image_app.paste(stn1, (890, 565), mask=stn1)

         draw.text((1050, 578),(f"{int(charactert.stats.FIGHT_PROP_ELEC_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882254148584759317.webp?size=96&quality=lossless")
         stl = BytesIO(response.content)
         stl1 = Image.open(stl).resize((50, 50))
         image_app.paste(stl1, (1000, 565), mask=stl1)

         draw.text((710, 638),(f"{int(charactert.stats.FIGHT_PROP_GRASS_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882253026113507349.webp?size=96&quality=lossless")
         stt = BytesIO(response.content)
         stt1 = Image.open(stt).resize((50, 50))
         image_app.paste(stt1, (660, 625), mask=stt1)           

         draw.text((830, 638),(f"{int(charactert.stats.FIGHT_PROP_WATER_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882254676916068393.webp?size=96&quality=lossless")
         stt2 = BytesIO(response.content)
         stt3 = Image.open(stt2).resize((50, 50))
         image_app.paste(stt3, (780, 625), mask=stt3)          

         draw.text((940, 638),(f"{int(charactert.stats.FIGHT_PROP_FIRE_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255)) 

         response = requests.get("https://cdn.discordapp.com/emojis/882254077361262592.webp?size=96&quality=lossless")
         sth = BytesIO(response.content)
         sth1 = Image.open(sth).resize((50, 50))
         image_app.paste(sth1, (890, 625), mask=sth1)          

         draw.text((1050, 638),(f"{int(charactert.stats.FIGHT_PROP_ICE_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))

         response = requests.get("https://cdn.discordapp.com/emojis/882253026046390292.webp?size=96&quality=lossless")
         stb = BytesIO(response.content)
         stb1 = Image.open(stb).resize((50, 50))
         image_app.paste(stb1, (1000, 625), mask=stb1)

        #tdv
        fonts = ImageFont.truetype("zh-cn.ttf", 16)

        artifact_counts = {}
        for artifact in charactert.artifacts:
            artifact_name_set = artifact.set_name
            if artifact_name_set in artifact_counts:
                artifact_counts[artifact_name_set] += 1
            else:
                artifact_counts[artifact_name_set] = 1
        y_position = 672
        y_offset = 28
        #set tdv
        for set_name, count in artifact_counts.items(): 
            if count > 1 and count < 4:
              draw.text((95, y_position), f"{artifact_name_set} {count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(0, 205, 102))
              y_position += y_offset
            if count > 3:
              draw.text((95, 685), f"{artifact_name_set} {count}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(0, 205, 102))
        #cv      
        x_cv1 = 158
        x_cv2 = 224
        sss = 0
        for artifact in charactert.artifacts:
            crit_rate = 0
            crit_dmg = 0
            for substate in artifact.sub_stats:
                if substate.name == "Tỷ Lệ Bạo Kích" or substate.name == "ST Bạo Kích":
                    if substate.name == "Tỷ Lệ Bạo Kích":
                        crit_rate = substate.value
                    elif substate.name == "ST Bạo Kích":
                        crit_dmg = substate.value
            cv0 = (crit_rate * 2) + crit_dmg
            draw.text((x_cv1, 900), (f"{cv0:.1f}CV"), font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))
            sss += 1
            if sss <= 3:
              x_cv1 += x_cv2
            else:
              x_cv1 += 226


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

          draw.text((x_tdv_level, 877), (f"+{artifact.level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255))
          x_tdv_level += x_tdv
          for substate in artifact.sub_stats:
            if substate.name == "Hiệu Quả Nạp Nguyên Tố":
              name_sst = substate.name.strip()[:12]
            elif substate.name == "Tinh Thông Nguyên Tố":
              name_sst = substate.name.strip()[:10]
            else:
              name_sst = substate.name
            draw.text((x_tdv_stats, y_tdv_stats1), (f"{name_sst} {substate.value}"), font=ImageFont.truetype("zh-cn.ttf", 18), fill=(255, 255, 255))
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
        embed.add_field(name="showcase", value="", inline=False)
        channel = inset_message.get("channelt")
        messaget = await channel.send(file=file)
        file_url = messaget.attachments[0]
        embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.now())
        embed.add_field(name=f"Name.{charactert.name}", value=f"Level.{charactert.level} \nnguyên tố.{charactert.element} C.{len(charactert.constellations)}", inline=False)
        embed.set_image(url=file_url)   
        embed.set_thumbnail(url=f"{charactert.icon}")
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
  def __init__ (self, *, timeout=180):
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
          if len(data.characters) > 0:
            #char0
            response = requests.get(data.characters[0].icon)
            image_set_char0 = BytesIO(response.content)
            image_char0 = Image.open(image_set_char0).resize((50, 50))
            image_app.paste(image_char0, (10, 60), mask=image_char0)
            draw.text((12, 122), data.characters[0].name, font=font,
                      fill=(0, 0, 0))  #name0
            draw.text((63, 80), (
              f"level:{data.characters[0].level}     C {len(data.characters[0].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level0
            #skill_char0
            response = requests.get(data.characters[0].talents[0].icon)  #skill1
            image_set_skill00 = BytesIO(response.content)
            image_skill00 = Image.open(image_set_skill00).resize((20, 20))
            image_app.paste(image_skill00, (61, 97), mask=image_skill00)

            response = requests.get(data.characters[0].talents[1].icon)  #skill2
            image_set_skill01 = BytesIO(response.content)
            image_skill01 = Image.open(image_set_skill01).resize((20, 20))
            image_app.paste(image_skill01, (101, 97), mask=image_skill01)

            response = requests.get(data.characters[0].talents[2].icon)  #skill3
            image_set_skill02 = BytesIO(response.content)
            image_skill02 = Image.open(image_set_skill02).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill02, (137, 97), mask=image_skill02)
            draw.text((61, 98), (f"     {data.characters[0].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((101, 98), (f"     {data.characters[0].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((137, 98), (f"     {data.characters[0].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 1:
            #char1
            response = requests.get(data.characters[1].icon)
            image_set_char1 = BytesIO(response.content)
            image_char1 = Image.open(image_set_char1).resize((50, 50))
            image_app.paste(image_char1, (191, 60), mask=image_char1)
            draw.text((195, 122), data.characters[1].name, font=font,
                      fill=(0, 0, 0))  #name1
            draw.text((244, 80), (
              f"level:{data.characters[1].level}     C {len(data.characters[1].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level1
            #skill_char1
            response = requests.get(data.characters[1].talents[0].icon)  #skill1
            image_set_skill10 = BytesIO(response.content)
            image_skill10 = Image.open(image_set_skill10).resize((20, 20))
            image_app.paste(image_skill10, (241, 97), mask=image_skill10)

            response = requests.get(data.characters[1].talents[1].icon)  #skill2
            image_set_skill11 = BytesIO(response.content)
            image_skill11 = Image.open(image_set_skill11).resize((20, 20))
            image_app.paste(image_skill11, (282, 97), mask=image_skill11)

            response = requests.get(data.characters[1].talents[2].icon)  #skill3
            image_set_skill12 = BytesIO(response.content)
            image_skill12 = Image.open(image_set_skill12).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill12, (320, 97), mask=image_skill12)
            draw.text((241, 98), (f"     {data.characters[1].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((282, 98), (f"     {data.characters[1].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((320, 98), (f"     {data.characters[1].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 2:
            #char2
            response = requests.get(data.characters[2].icon)
            image_set_char2 = BytesIO(response.content)
            image_char2 = Image.open(image_set_char2).resize((50, 50))
            image_app.paste(image_char2, (372, 60), mask=image_char2)
            draw.text((378, 122), data.characters[2].name, font=font,
                      fill=(0, 0, 0))  #name2
            draw.text((425, 80), (
              f"level:{data.characters[2].level}     C {len(data.characters[2].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level2
            #skill_char2
            response = requests.get(data.characters[2].talents[0].icon)  #skill1
            image_set_skill20 = BytesIO(response.content)
            image_skill20 = Image.open(image_set_skill20).resize((20, 20))
            image_app.paste(image_skill20, (423, 97), mask=image_skill20)

            response = requests.get(data.characters[2].talents[1].icon)  #skill2
            image_set_skill21 = BytesIO(response.content)
            image_skill21 = Image.open(image_set_skill21).resize((20, 20))
            image_app.paste(image_skill21, (463, 97), mask=image_skill21)

            response = requests.get(data.characters[2].talents[2].icon)  #skill3
            image_set_skill22 = BytesIO(response.content)
            image_skill22 = Image.open(image_set_skill22).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill22, (503, 97), mask=image_skill22)
            draw.text((423, 98), (f"     {data.characters[2].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((463, 98), (f"     {data.characters[2].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((502, 98), (f"     {data.characters[2].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 3:
            #char3
            response = requests.get(data.characters[3].icon)
            image_set_char3 = BytesIO(response.content)
            image_char3 = Image.open(image_set_char3).resize((50, 50))
            image_app.paste(image_char3, (553, 60), mask=image_char3)
            draw.text((561, 122), data.characters[3].name, font=font,
                      fill=(0, 0, 0))  #name3
            draw.text((606, 80), (
              f"level:{data.characters[3].level}     C {len(data.characters[3].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level3
            #skill_char3
            response = requests.get(data.characters[3].talents[0].icon)  #skill1
            image_set_skill30 = BytesIO(response.content)
            image_skill30 = Image.open(image_set_skill30).resize((20, 20))
            image_app.paste(image_skill30, (605, 97), mask=image_skill30)

            response = requests.get(data.characters[3].talents[1].icon)  #skill2
            image_set_skill31 = BytesIO(response.content)
            image_skill31 = Image.open(image_set_skill31).resize((20, 20))
            image_app.paste(image_skill31, (645, 97), mask=image_skill31)

            response = requests.get(data.characters[3].talents[2].icon)  #skill3
            image_set_skill32 = BytesIO(response.content)
            image_skill32 = Image.open(image_set_skill32).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill32, (684, 97), mask=image_skill32)
            draw.text((605, 98), (f"     {data.characters[3].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((645, 98), (f"     {data.characters[3].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((684, 98), (f"     {data.characters[3].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 4:
            #char4
            response = requests.get(data.characters[4].icon)
            image_set_char4 = BytesIO(response.content)
            image_char4 = Image.open(image_set_char4).resize((50, 50))
            image_app.paste(image_char4, (10, 214), mask=image_char4)
            draw.text((12, 273), data.characters[4].name, font=font,
                      fill=(0, 0, 0))  #name4
            draw.text((63, 230), (
              f"level:{data.characters[4].level}     C {len(data.characters[4].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level4
            #skill_char4
            response = requests.get(data.characters[4].talents[0].icon)  #skill1
            image_set_skill40 = BytesIO(response.content)
            image_skill40 = Image.open(image_set_skill40).resize((20, 20))
            image_app.paste(image_skill40, (61, 247), mask=image_skill40)

            response = requests.get(data.characters[4].talents[1].icon)  #skill2
            image_set_skill41 = BytesIO(response.content)
            image_skill41 = Image.open(image_set_skill41).resize((20, 20))
            image_app.paste(image_skill41, (102, 247), mask=image_skill41)

            response = requests.get(data.characters[4].talents[2].icon)  #skill3
            image_set_skill42 = BytesIO(response.content)
            image_skill42 = Image.open(image_set_skill42).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill42, (140, 247), mask=image_skill42)
            draw.text((61, 248), (f"     {data.characters[4].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((102, 248), (f"     {data.characters[4].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((140, 248), (f"     {data.characters[4].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 5:
            #char5
            response = requests.get(data.characters[5].icon)
            image_set_char5 = BytesIO(response.content)
            image_char5 = Image.open(image_set_char5).resize((50, 50))
            image_app.paste(image_char5, (193, 214), mask=image_char5)
            draw.text((195, 273), data.characters[5].name, font=font,
                      fill=(0, 0, 0))  #name5
            draw.text((244, 230), (
              f"level:{data.characters[5].level}     C {len(data.characters[5].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level5
            #skill_char5
            response = requests.get(data.characters[5].talents[0].icon)  #skill1
            image_set_skill50 = BytesIO(response.content)
            image_skill50 = Image.open(image_set_skill50).resize((20, 20))
            image_app.paste(image_skill50, (243, 247), mask=image_skill50)

            response = requests.get(data.characters[5].talents[1].icon)  #skill2
            image_set_skill51 = BytesIO(response.content)
            image_skill51 = Image.open(image_set_skill51).resize((20, 20))
            image_app.paste(image_skill51, (285, 247), mask=image_skill51)

            response = requests.get(data.characters[5].talents[2].icon)  #skill3
            image_set_skill52 = BytesIO(response.content)
            image_skill52 = Image.open(image_set_skill52).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill52, (323, 247), mask=image_skill52)
            draw.text((243, 248), (f"     {data.characters[5].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((285, 248), (f"     {data.characters[5].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((323, 248), (f"     {data.characters[5].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 6:
            #char6
            response = requests.get(data.characters[6].icon)
            image_set_char6 = BytesIO(response.content)
            image_char6 = Image.open(image_set_char6).resize((50, 50))
            image_app.paste(image_char6, (374, 214), mask=image_char6)
            draw.text((378, 273), data.characters[6].name, font=font,
                      fill=(0, 0, 0))  #name6
            draw.text((425, 230), (
              f"level:{data.characters[6].level}     C {len(data.characters[6].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level6
            #skill_char6
            response = requests.get(data.characters[6].talents[0].icon)  #skill1
            image_set_skill60 = BytesIO(response.content)
            image_skill60 = Image.open(image_set_skill60).resize((20, 20))
            image_app.paste(image_skill60, (426, 247), mask=image_skill60)

            response = requests.get(data.characters[6].talents[1].icon)  #skill2
            image_set_skill61 = BytesIO(response.content)
            image_skill61 = Image.open(image_set_skill61).resize((20, 20))
            image_app.paste(image_skill61, (467, 247), mask=image_skill61)

            response = requests.get(data.characters[6].talents[2].icon)  #skill3
            image_set_skill62 = BytesIO(response.content)
            image_skill62 = Image.open(image_set_skill62).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill62, (506, 247), mask=image_skill62)
            draw.text((426, 248), (f"     {data.characters[6].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((467, 248), (f"     {data.characters[6].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((506, 248), (f"     {data.characters[6].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
          if len(data.characters) > 7:
            #char7
            response = requests.get(data.characters[7].icon)
            image_set_char7 = BytesIO(response.content)
            image_char7 = Image.open(image_set_char7).resize((50, 50))
            image_app.paste(image_char7, (558, 214), mask=image_char7)
            draw.text((561, 273), data.characters[7].name, font=font,
                      fill=(0, 0, 0))  #name7
            draw.text((606, 230), (
              f"level:{data.characters[7].level}     C {len(data.characters[7].constellations)}"
            ),
                      font=font,
                      fill=(0, 0, 0))  #level7
            #skill_char7
            response = requests.get(data.characters[7].talents[0].icon)  #skill1
            image_set_skill70 = BytesIO(response.content)
            image_skill70 = Image.open(image_set_skill70).resize((20, 20))
            image_app.paste(image_skill70, (608, 247), mask=image_skill70)

            response = requests.get(data.characters[7].talents[1].icon)  #skill2
            image_set_skill71 = BytesIO(response.content)
            image_skill71 = Image.open(image_set_skill71).resize((20, 20))
            image_app.paste(image_skill71, (648, 247), mask=image_skill71)

            response = requests.get(data.characters[7].talents[2].icon)  #skill3
            image_set_skill72 = BytesIO(response.content)
            image_skill72 = Image.open(image_set_skill72).resize(
              (20, 20)).convert('RGBA')
            image_app.paste(image_skill72, (687, 247), mask=image_skill72)
            draw.text((608, 248), (f"     {data.characters[7].talents[0].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((648, 248), (f"     {data.characters[7].talents[1].level}"),
                      font=font,
                      fill=(255, 255, 255))
            draw.text((687, 248), (f"     {data.characters[7].talents[2].level}"),
                      font=font,
                      fill=(255, 255, 255))
        else:
          embed1 = discord.Embed(color=0xed0202)
          embed1.add_field(name="lỗi",
                           value="Không tìm thấy dữ liệu cho người dùng này.",
                           inline=False)
          embed1.add_field(
            name="Chuyện gì đã xảy ra?",
            value=
            "Vấn đề thường gặp nhất với lỗi này đó là tài khoản bạn đang tìm kiếm chưa công khai Hồ sơ. Để sửa lỗi này, hãy bật tùy chọn ``Hiển thị chi tiết nhân vật`` trong giao diện Hồ sơ Genshin của bạn. Hãy tham khảo hình ảnh bên dưới.",
            inline=False)
          embed1.set_image(
            url=
            "https://cdn.discordapp.com/attachments/969461764704059392/1000843651863285810/unknown.png"
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

        embed.set_thumbnail(url=f"{data.player.namecard_icon}")
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
