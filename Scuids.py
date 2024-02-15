import discord
from discord.ext import commands, tasks
from discord import app_commands, PartialEmoji
import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from datetime import datetime, timedelta, time
import aiohttp
import datetime
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

async def fetch_image(session, url):
    async with session.get(url) as response:
        return await response.read()

async def download_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_image(session, url) for url in urls]
        return await asyncio.gather(*tasks)

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
    return count

async def ntscuid(nntsl):
    url_nt = [
        "https://media.discordapp.net/attachments/1107978903294853140/1206623380741038090/Khong_Co_Tieu_e151_20240212222810.png?ex=65dcae97&is=65ca3997&hm=6a770a13c7b708e78ef315cb2f42c9be341f2bbc9c5a7134fe2554899e6e7a6c&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623381131231232/Khong_Co_Tieu_e152_20240212222844.png?ex=65dcae98&is=65ca3998&hm=f9062bc6d4dc71ec6e819b12fd8b9cd319c1143346ec90616f04c3748b207da8&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623381475033098/Khong_Co_Tieu_e153_20240212222858.png?ex=65dcae98&is=65ca3998&hm=51728d2ef5a141cf3aab459db011c9337d5083cb1fb82c6ce23f466fcd50edb5&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623381861048410/Khong_Co_Tieu_e154_20240212222916.png?ex=65dcae98&is=65ca3998&hm=59378ff4f989f1e608b03590fd832138f105c258434d7a683969c1fc5a468854&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623382364360744/Khong_Co_Tieu_e155_20240212222931.png?ex=65dcae98&is=65ca3998&hm=b055faba3424ce0cae45eb6f726e38d01abfe62db6229f6034b62d46e0ccc85b&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623382976856155/Khong_Co_Tieu_e156_20240212222949.png?ex=65dcae98&is=65ca3998&hm=f698eb3d1ef4b6260bd5df3e4a721814a2a9cf9949a6eb44fb5ca4c3e529e909&a",
        "https://media.discordapp.net/attachments/1107978903294853140/1206623383614132285/Khong_Co_Tieu_e157_20240212223010.png?ex=65dcae98&is=65ca3998&hm=8ea0db5d93b5164d07427d8f9fb4b5c33beedf7f670eda151b7ed21a5819c71c&a",
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
  "FIGHT_PROP_HP": "https://cdn.discordapp.com/attachments/1118977913392476210/1118990290942951545/CHUH17121.png",
  "FIGHT_PROP_ATTACK": "https://media.discordapp.net/attachments/1118977913392476210/1118990421289357452/atk.png",
  "FIGHT_PROP_DEFENSE": 'https://cdn.discordapp.com/attachments/1118977913392476210/1118990526595727501/THFM69251.png',
  "FIGHT_PROP_HP_PERCENT": "https://cdn.discordapp.com/attachments/1107978903294853140/1206225150249402438/Khong_Co_Tieu_e138.png?ex=65db3bb6&is=65c8c6b6&hm=ce8836260a9b3e88ea7dc9c6c73450718e65ea737a82c3d68eddc1c4ab407967&a",
  "FIGHT_PROP_ATTACK_PERCENT": "https://cdn.discordapp.com/attachments/1107978903294853140/1206587924301221888/Khong_Co_Tieu_e138.png?ex=65dc8d92&is=65ca1892&hm=da11bd50fad8386daa3cff92af82998885f366bdd5cb67834d0b7680ee686f05&a",
  "FIGHT_PROP_DEFENSE_PERCENT": "https://media.discordapp.net/attachments/1107978903294853140/1206224714545111091/Khong_Co_Tieu_e138.png?ex=65db3b4e&is=65c8c64e&hm=98ff83553535e37d784074528a87560659be494784d27a31062c3322f35d114f&a",
  "FIGHT_PROP_CRITICAL": "https://cdn.discordapp.com/attachments/1118977913392476210/1118990420903477248/cr.png",
  "FIGHT_PROP_CRITICAL_HURT": "https://cdn.discordapp.com/attachments/1118977913392476210/1118990421582954577/cd.png",
  "FIGHT_PROP_CHARGE_EFFICIENCY": 'https://cdn.discordapp.com/attachments/1118977913392476210/1118990525501022218/hqn.png',
  "FIGHT_PROP_HEAL_ADD": 'https://cdn.discordapp.com/attachments/1118977913392476210/1118990525794619402/heal.png',
  "FIGHT_PROP_ELEMENT_MASTERY": "https://cdn.discordapp.com/attachments/1118977913392476210/1118990526247608361/ttnt.png",
  "FIGHT_PROP_PHYSICAL_ADD_HURT": 'https://cdn.discordapp.com/attachments/1092394580009295952/1119211230872211476/350.png',
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
                  "https://static.wikia.nocookie.net/genshin-impact/images/4/47/V%E1%BA%ADt_Ph%E1%BA%A9m_EXP_Y%C3%AAu_Th%C3%ADch.png/revision/latest?cb=20210528145929&path-prefix=vi",
                  "https://media.discordapp.net/attachments/1107978903294853140/1204653738715775056/Kgsu.png?ex=65d58438&is=65c30f38&hm=34e1aa2b6f39f02d514c3fcf1957979edf6d687b6b1169c31003228f6a04b8de&",                    
                  charactert.costume.icon.gacha if charactert.costume is not None else charactert.icon.gacha
                  ,charactert.weapon.icon,            
                  charactert.talents[0].icon,
                  charactert.talents[1].icon,
                  charactert.talents[2].icon,
                  "https://media.discordapp.net/attachments/1114095095210311680/1151759944278884352/R.png",               
              ]
              urlgoc = await ntscuid(charactert.element.value)
              responses = await download_images(urls_to_download)
              image_app = Image.open(BytesIO(urlgoc)).convert("RGBA").resize((1141, 1026))
              font = ImageFont.truetype("zh-cn.ttf", 27)
              draw = ImageDraw.Draw(image_app)
              draw.text((38, 24), data.player.nickname, font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255)) #player name
              draw.text((38, 51), (f"UID:{uid}  AR:{data.player.level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255)) #player level
              #char)           
              image_schar0 = Image.open(BytesIO(responses[2])).convert("RGBA")
              xc , yc = image_schar0.size
              image_schar0 = Image.open(BytesIO(responses[2])).convert("RGBA").resize((xc//3, yc//3))
              image_app.paste(image_schar0, (83 if charactert.costume is not None else -83, 95), mask=image_schar0)
              draw.text((34, 528), charactert.name, font=font, fill=(255, 255, 255))  #name0
              draw.text((34, 469), (f"lv.{charactert.level} / {charactert.max_level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255))  #level0
              draw.text((34, 437), (f"BFF.{charactert.friendship_level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255))  #độ yêu thích        
              #vũ khí                              
              image_vk0 = Image.open(BytesIO(responses[3])).convert("RGBA").resize((144, 124))
              image_app.paste(image_vk0, (650, 33), mask=image_vk0)
              draw.text((820, 36), weapon.name, font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255)) #name
              draw.text((644, 33), (f"R{weapon.refinement}"), font=font, fill=(255, 255, 255)) #tinh luyện
              draw.text((956, 104), (f"{weapon.level}/{weapon.max_level}"), font=font, fill=(255, 255, 255)) #level
              draw.text(((671, 146)) if weapon.rarity == 5 else (681, 146), (f"{'★'*weapon.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 0))#rate
              draw.text((840, 104), (f"{round(weapon.stats[0].value)}"), font=font, fill=(255, 255, 255))#atk#dòng chính
              stat_name = weapon.stats[1].name.strip()[:12] if weapon.stats[1].name == "Hiệu Quả Nạp Nguyên Tố" else weapon.stats[1].name
              draw.text((831, 150), f"{stat_name}: {weapon.stats[1].formatted_value}", font=ImageFont.truetype("zh-cn.ttf", 17), fill=(255, 255, 255))                
              #stats
              stat_infos = [
                  (("HP: ", FightPropType.FIGHT_PROP_MAX_HP), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990290942951545/CHUH17121.png", (644, 220-12), (40, 40)),
                  (("Tấn Công: ", FightPropType.FIGHT_PROP_CUR_ATTACK), "https://media.discordapp.net/attachments/1118977913392476210/1118990421289357452/atk.png", (644, 255-12), (40, 40)),
                  (("Phòng Ngự: ", FightPropType.FIGHT_PROP_CUR_DEFENSE), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990526595727501/THFM69251.png", (644, 295-12), (40, 40)),
                  (("Tinh Thông Nguyên Tố: ", FightPropType.FIGHT_PROP_ELEMENT_MASTERY), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990526247608361/ttnt.png", (644, 335-12), (40, 40)),
                  (("Tỉ Lệ Bạo: ", FightPropType.FIGHT_PROP_CRITICAL), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990420903477248/cr.png", (644, 375-12), (40, 40)),
                  (("Sát Thương Bạo: ", FightPropType.FIGHT_PROP_CRITICAL_HURT), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990421582954577/cd.png", (644, 415-12), (40, 40)),
                  (("Hiệu Quả Nạp: ", FightPropType.FIGHT_PROP_CHARGE_EFFICIENCY), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990525501022218/hqn.png", (644, 455-12), (40, 40)),
                  (("Trị Liệu: ", FightPropType.FIGHT_PROP_HEAL_ADD), "https://cdn.discordapp.com/attachments/1118977913392476210/1118990525794619402/heal.png", (644, 495-12), (40, 40)),
                  #stnt
                  (("", FightPropType.FIGHT_PROP_PHYSICAL_ADD_HURT), "https://cdn.discordapp.com/attachments/1092394580009295952/1119211230872211476/350.png", (644, 540-12), (50, 50)),#vật lý
                  (("", FightPropType.FIGHT_PROP_WIND_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026021228544.webp?size=96&quality=lossless", (766, 540-12), (50, 50)),#phong
                  (("", FightPropType.FIGHT_PROP_ROCK_ADD_HURT), "https://cdn.discordapp.com/emojis/882253025895399504.webp?size=96&quality=lossless", (879, 540-12), (50, 50)),#nham
                  (("", FightPropType.FIGHT_PROP_ELEC_ADD_HURT), "https://cdn.discordapp.com/emojis/882254148584759317.webp?size=96&quality=lossless", (993, 540-12), (50, 50)),#lôi
                  (("", FightPropType.FIGHT_PROP_GRASS_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026113507349.webp?size=96&quality=lossless", (644, 600-12), (50, 50)),#thảo
                  (("", FightPropType.FIGHT_PROP_WATER_ADD_HURT), "https://cdn.discordapp.com/emojis/882254676916068393.webp?size=96&quality=lossless", (766, 600-12), (50, 50)),#thuỷ
                  (("", FightPropType.FIGHT_PROP_FIRE_ADD_HURT), "https://cdn.discordapp.com/emojis/882254077361262592.webp?size=96&quality=lossless", (879, 600-12), (50, 50)),#hoả
                  (("", FightPropType.FIGHT_PROP_ICE_ADD_HURT), "https://cdn.discordapp.com/emojis/882253026046390292.webp?size=96&quality=lossless", (993, 600-12), (50, 50)),#băng
              ]                
              urls = [stat_info[1] for n, stat_info in enumerate(stat_infos[:16])]
              responset = await download_images(urls)
              current_position = (688, 210)
              txtx = 0
              xnt = [693, 815, 928, 1042]   
              for o, stat_info in enumerate(stat_infos[:16]):
                  stat_name = stat_info[0][0]
                  stat_value = charactert.stats[stat_info[0][1]].formatted_value
                  stat_value = f"{stat_value[:-3]}%" if stat_value.endswith('.0%') else stat_value.rstrip('0').rstrip('.')
                  icon_url = stat_info[1]
                  icon_position = stat_info[2]
                  icon_size = stat_info[3]
                  fontt = ImageFont.truetype("zh-cn.ttf", 25) if 12 > txtx <= 8 else ImageFont.truetype("zh-cn.ttf", 21) 
                  if txtx >= 8 and txtx < 12:
                      current_position = (xnt[txtx-8], 570-12) 
                  elif txtx >= 12:
                      current_position = (xnt[txtx-12], 623-12)                              
                  draw.text(current_position, (f"{stat_name}{stat_value}"), font=fontt, fill=(255, 255, 255))                         
                  icon_image = Image.open(BytesIO(responset[txtx])).convert("RGBA").resize(icon_size)
                  image_app.paste(icon_image, icon_position, mask=icon_image)
                  if txtx < 8:
                      current_position = (current_position[0], current_position[1] + 40)                 
                  txtx += 1                
              #tdv
              fonts = ImageFont.truetype("zh-cn.ttf", 16)      
              artifact_counts = {}
              for p, artifact in enumerate(charactert.artifacts[:5]):
                  artifact_name_set = artifact.set_name
                  if artifact_name_set in artifact_counts:
                      artifact_counts[artifact_name_set] += 1
                  else:
                      artifact_counts[artifact_name_set] = 1
              sorted_counts = dict(sorted(artifact_counts.items(), key=operator.itemgetter(1), reverse=True))
              y_position, y_offset = 571, 32
              #set tdv
              for set_name, count in sorted_counts.items(): 
                  if count >= 2 and count < 4:
                    draw.text((72, y_position), f"{set_name} x{count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(0, 205, 102))
                    y_position += y_offset
                  if count >= 4:
                    draw.text((72, 586), f"{set_name} x{count}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(0, 205, 102))
              #cv      
              x_cv1, x_cv2, sss = 158, 224, 0
              x_tdv_levels = 166
              for v, artifact in enumerate (charactert.artifacts[:5]):
                  crit_dmg, crit_rate = 0, 0
                  for c, substate in enumerate(artifact.sub_stats[:4]):
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
                  draw.rounded_rectangle([x_cv1 - 5, 818 - 5, x_cv1 + 68 + 5, 818 + 18 + 5], 10, fill=color)
                  draw.text((x_tdv_levels, 790), f"+{artifact.level}", font=ImageFont.truetype("zh-cn.ttf", 23), fill=(255, 255, 255))
                  draw.text((x_cv1 + 1, 818 + 1), f"{cv0:.1f}CV", font=ImageFont.truetype("zh-cn.ttf", 17), fill=fills)
                  x_tdv_levels += 227
                  sss += 1
                  x_cv1 += x_cv2 if sss <= 3 else 226              
              x_tdv, x_tdv_stats1, x_tdv_icon, x_tdv_level = 227, 224, 43, 166
              x_tdv_rate, x_tdv_stats = 25, 30
              y_tdv_stats1, y_tdv_stats2 = 850, 40
              element_count = 0
              for b, artifact in enumerate(charactert.artifacts[:5]):
                  response = await fetch_image(session, artifact.icon)
                  image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((165, 165))
                  image_app.paste(image_tdv0, (x_tdv_icon-20, 674), mask=image_tdv0)
                  response = await licon(artifact.main_stat.type.value)
                  image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((50, 50))
                  image_app.paste(image_tdv0, (x_tdv_stats+139, 659), mask=image_tdv0)            
                  draw.text((x_tdv_rate, 814), (f"{'★'*artifact.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 0))
                  draw.text((x_tdv_stats-11, 654), (f"{artifact.main_stat.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 28), fill=(255, 255, 250))                  
                  x_tdv_icon += x_tdv
                  x_tdv_rate += x_tdv
                  x_tdv_level += x_tdv
                  for n, substate in enumerate(artifact.sub_stats[:4]):
                      response = await licon(substate.type.value)
                      image_tdv0 = Image.open(BytesIO(response)).convert("RGBA").resize((40, 40))
                      image_app.paste(image_tdv0, (x_tdv_stats, y_tdv_stats1), mask=image_tdv0)                    
                      occurrence = await count_occurrences(float(substate.formatted_value.replace('%', '')), substate.type.value)                  
                      draw.text((x_tdv_stats+45, y_tdv_stats1+10), (f"+{substate.formatted_value}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=((255, 255, 255) if occurrence >= 2 else (149, 149, 149)))
                      draw.text((x_tdv_stats+128, y_tdv_stats1+14), (f"{'*'*occurrence}"), font=ImageFont.truetype("zh-cn.ttf", 21), fill=((255, 255, 255) if occurrence >= 2 else (149, 149, 149)))                 
                      y_tdv_stats1 += y_tdv_stats2
                      element_count += 1
                      if element_count % 4 == 0: 
                        y_tdv_stats1 = 850
                        x_tdv_stats += x_tdv_stats1 if element_count < 16 else (x_tdv_stats1 - 4)
              #thiên phú
              skill_positions = [(538, 18), (538, 84), (538, 150)]                
              for i in range(3):
                  image_skill = Image.open(BytesIO(responses[i + 4])).convert("RGBA").resize((60, 60))
                  image_app.paste(image_skill, skill_positions[i], mask=image_skill)
                  draw.text((534 if charactert.talents[i].level > 9 else 536, 47 + i * 67), (f"     {charactert.talents[i].level}"), font=font, fill=(255, 255, 255))                                
              #cm
              Locks = (len(charactert.constellations))          
              x_lock, y_lock = 538, 566
              for _ in range(6 - Locks):
                image_skill00 = Image.open(BytesIO(responses[7])).convert("RGBA").resize((60, 60))
                image_app.paste(image_skill00, (x_lock, y_lock), mask=image_skill00)
                y_lock -= 65        
              inseta = 244
              y_ts = [65,66,63,64,65] 
              for k in range(Locks):                                             
                response = await fetch_image(session, charactert.constellations[k].icon)
                image_skill00 = Image.open(BytesIO(response)).convert("RGBA").resize((60, 60))
                image_app.paste(image_skill00, (538, inseta), mask=image_skill00)
                tert = y_ts[k % len(y_ts)]
                inseta += tert      
              buffer = BytesIO()
              image_app.save(buffer, format='png')
              buffer.seek(0)
              file = discord.File(buffer, filename="showcase.png")
              channel = inset_message.get("channelt")
              messaget = await channel.send(file=file)
              file_url = messaget.attachments[0]
              return file_url

async def generate_image(data):
    async with aiohttp.ClientSession() as session:
        uid = global_data.get("uid")
        urlgoc = await fetch_image(session, 'https://media.discordapp.net/attachments/1107978903294853140/1206074586098176010/F7C59933-6074-48A1-8422-A66E5B12B81F.png?ex=65daaf7d&is=65c83a7d&hm=bf8a3b1baedfa274063937d09302701f079f5691e37a88261013e7e44067f11a&')
        image_appt = Image.open(BytesIO(urlgoc)).convert("RGBA").resize((600, 850))
        draw = ImageDraw.Draw(image_appt)
        player_icon_data = await fetch_image(session, data.player.profile_picture_icon.side)
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
        filet = discord.File(buffer, filename="output.png")      
        channel = inset_message.get("channelt")
        return filet

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
                data = global_data.get("data")
                channel = inset_message.get('channelt')
                messagea = inset_message.get("message")
                now = datetime.datetime.now()
                embed_loading = discord.Embed(title="<a:aloading:1152869299942338591> **Đang tạo thông tin..__Hãy kiên nhẫn__** <a:ganyurollst:1118761352064946258>", color=discord.Color.yellow())
                await Interaction.response.edit_message(content=None, embed=embed_loading)
                char_index = int(self.values[0][-1]) - 1
                charactert = data.characters[char_index]
                embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.datetime.now())
                reload_time = now + datetime.timedelta(seconds=data.ttl)
                embed.add_field(name=f"Name.{charactert.name}", value=f"Level.{charactert.level} \nnguyên tố.{charactert.element} C.{len(charactert.constellations)} \nLàm mới: <t:{int(reload_time.timestamp())}:R>", inline=False) 
                embed.set_thumbnail(url=f"{charactert.icon.front}")
                embed.set_footer(text=f"{uid}", icon_url=f"{Interaction.user.avatar}")
                file_url = await image_dcuid(data.characters[char_index])
                embed.set_image(url=file_url)
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
    async with enka.EnkaAPI(lang=Language.VIETNAMESE) as api:
     try:
        uid = uid
        data = await api.fetch_showcase(uid)
        global_data["data"] = data
        global_data["uid"] = uid
        embed = discord.Embed()
        embed.add_field(name="vui lòng đợi thông tin được sử lý", value="", inline=False)
        await Interaction.response.send_message(embed=embed, ephemeral=True)
        embed1 = discord.Embed(color=0xed0202)
        embed1.add_field(name="lỗi", value="Không tìm thấy dữ liệu cho người dùng này.", inline=False)
        embed1.add_field(name="Chuyện gì đã xảy ra?", value="Vấn đề thường gặp nhất với lỗi này đó là tài khoản bạn đang tìm kiếm chưa công khai Hồ sơ. Để sửa lỗi này, hãy bật tùy chọn ``Hiển thị chi tiết nhân vật`` trong giao diện Hồ sơ Genshin của bạn. Hãy tham khảo hình ảnh bên dưới", inline=False)
        embed1.set_image(url="https://cdn.discordapp.com/attachments/969461764704059392/1000843651863285810/unknown.png"
        )
        filet= await generate_image(data) if data.characters is not None and len(data.characters) > 0 else await Interaction.followup.send(embed=embed1, ephemeral=True)
        channel = self.bot.get_channel(1118977913392476210)
        inset_message["channelt"] = channel
        saved_file = await channel.send(file=filet)
        files_url = saved_file.attachments[0]
        embed= discord.Embed()
        embed.set_image(url=files_url)
        message = await Interaction.channel.send(embed=embed, view=SelectView())
        inset_message["message"] = message
     except Exception as s:
        await channel.send(s)

async def setup(bot):
  await bot.add_cog(scuids(bot))