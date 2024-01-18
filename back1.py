#ghep pvp
import random
@bot.tree.command(name="pvp",
                  description="Dùng để ghép với một người ngẫu nhiên")
async def pvp(Interaction):
  embed = discord.Embed(title='Ghép đối thủ', color=discord.Color.blue())
  embed.add_field(name=f"bởi {Interaction.user.name}", value="Nhấn vào ✅ để tham gia")
  channel = Interaction.channel
  message = await channel.send(embed=embed)
  await Interaction.response.send_message("sửa dụng lệnh thành công", ephemeral=True)
  await message.add_reaction('✅')
  await asyncio.sleep(60)

  await asyncio.sleep(1)
  message = await Interaction.channel.fetch_message(message.id)
  reactions = [
    reaction for reaction in message.reactions if str(reaction.emoji) == '✅'
  ]
  participants = []
  for reaction in reactions:
    async for user in reaction.users():
      if not user.bot:
        participants.append(user)

  if len(participants) < 2:
    await Interaction.response.send_message('Không có ai tham gia.')
  else:
      channel_tg = bot.get_channel(1102862665061253120)
      topic_tg = await channel_tg.create_thread(
      name=f'Room So Tài', type=discord.ChannelType.private_thread)
      winner = random.choice(participants)
      await topic_tg.send(
      f"Cuộc so tài {Interaction.user.mention} vs {winner.mention}")

      topic_mention = topic_tg.mention
      response_embed = discord.Embed(title="Tạo Room thành công", description=f"{Interaction.user.mention} vs {winner.mention} | Hãy vào {topic_mention} để giao tiếp với đối thủ", color=0x00ff00)
      await channel.send(embed=response_embed)


from enkanetwork.model.stats import Stats

embed1.add_field(name="**/pvp**", value="> dùng để ghép đối thủ ngẫu nhiên", inline=False)

@bot.tree.command(name="test", description="dùng để trao đổi với quản lý guild")
async def test(Interaction):
  embed = discord.Embed(title="Chào mừng mọi người đã đến với server HIVE Teyvat, dưới đây là rule server",
                      description="✧1. Tên và avatar\n> • Tên và avatar phải đúng quy định của Discord và không được chứa nội dung khiêu dâm, tục tĩu, xúc phạm đến một cá nhân hay tổ chức nào đó.\n✧2. Nhân bản và giả danh người khác\n> •  Nghiêm cấm sử dụng acc clone hay giả danh người khác.\n✧3. ách ứng xử và tương tác\n> • Sử dụng kênh đúng nơi đúng chỗ và đúng chủ đề.\n> • Hạn chế nói tục, \n> • Không xúc phạm, lăng mạ, có ngôn từ gây thù ghét nhằm công kích một cá nhân hay một tập thể nào đó.\n> • Không spam \n✧4. Các nội dung nghiêm cấm\n> • Nghiêm cấm gửi những link và ảnh nsfw, link chứa virus, link server khác. \n> • Nghiếm cấm mua bán acc game; nitro;..., quảng cáo hay chèo kéo khách hàng. \n> • Nghiêm cấm ping everyone, ping ghost. Chỉ thật sự ping admin và mod khi có trường hợp cần thiết.\n\n**Lưu ý**. \n> • Lệnh của mod và admin là tuyệt đối nên nghiêm cấm lách luật dưới mọi hình thức, nếu bạn lách luật chúng tớ sẽ không ngần ngại cho bạn ra đảo.\n> • Nếu phát hiện ai vi phạm và muốn góp ý về server có thể phản hồi lại cho chúng tớ.\n> • Dùng lệnh /token để trao đổi với mod và admin server\n**Hình thức sử phạt**.\n> Lần 1: Nhắc nhở\n> Lần 2: Mute hoặc hạ level tùy theo mức độ nghiêm trọng của vấn đề\n> Lần 3: Kick ra khỏi server\n\n**[Quay lại đầu trang](https://discord.com/channels/550601755709407233/898419988396920852)**",
                      colour=0xc365af,
                      timestamp=datetime.now())

  embed.set_footer(text="ngày cập nhật",
                 icon_url="https://media.discordapp.net/attachments/1114929862050852925/1117077305228001280/Untitled1_20230604095651.png?width=412&height=412")
  channel = Interaction.channel
  await channel.send(embed=embed)

            max_retries = 3
            retry_count = 0      
            while retry_count < max_retries:
                try:
                    await Interaction.response.edit_message(embed=embed)
                    break
                except discord.NotFound:
                    retry_count += 1
                    await asyncio.sleep(15)
                    continue
                except discord.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(15)
                        continue
                    else:
                        raise e
            
            if retry_count >= max_retries:
                await Interaction.channel.send("Đã đạt tới số lần lặp tối đa. Không thể chỉnh sửa tin nhắn.")
            else:
                try:
                    message = await Interaction.followup.send(file=file, ephemeral=True)
                    await asyncio.sleep(10)
                    await message.delete()
                except discord.NotFound:
                    await Interaction.channel.send("Tin nhắn không tìm thấy.")

          new_nickname = f"[TT{new_level}] {message.author.display_name}"
          try:
            if not message.author.guild.get_role(1091384393727229972) in message.author.roles:
              await message.author.edit(nick=new_nickname)
            else:
              return
          except discord.Forbidden:
            return

  if "b!info" in message.content:
    channel_info = message.channel
    server_count = len(bot.guilds)
    bot_ping = round(bot.latency * 1000)
    embed_info = discord.Embed(title="Thông tin bot",
                               color=discord.Color.blue())
    embed_info.add_field(name=f"Số lượng bot {server_count}", value="")
    embed_info.add_field(name="", value=f"ping: {bot_ping}ms", inline=False)
    embed_info.add_field(name="", value="prefix `b!`", inline=False)
    embed_info.set_footer(
      text="Bot onwer: BEEMIN#1475",
      icon_url=
      "https://cdn.discordapp.com/avatars/480986687712002058/04755a0b1bf34cca99415cb33e89f52a.png"
    )
    button1 = discord.ui.Button(label="support", url="https://discord.gg/HIVETeyvat")

    button2 = discord.ui.Button(label="invitation", url="https://discord.com/api/oauth2/authorize?client_id=1111140087770664960&permissions=8&scope=bot")

    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    await channel_info.send(embed=embed_info, view=view)



@tasks.loop(seconds=60)
async def url():
    url = "https://caytg.thanh-datdat39.repl.co"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Website accessed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error accessing website: {e}")



#token trảo đổi
@bot.tree.command(name="token", description="dùng để trao đổi với quản lý guild")
async def token(Interaction):
  channel = bot.get_channel(699305290289381477)

  if not channel:
    return await Interaction.respond("Không tìm thấy kênh chỉ định.")

  anonymous_topic = await channel.create_thread(
    name=f'Tiket {Interaction.user.name}',
    type=discord.ChannelType.private_thread)

  role = Interaction.guild.get_role(1087675803170525254)

  await anonymous_topic.send(
    f"Cuộc trao đổi giữ {Interaction.user.mention} với {role.mention}! hãy bắt đầu bằng điều bạn muốn nói"
  )

  topic_mention = anonymous_topic.mention
  response_embed = discord.Embed(
    title="tạo token thành công",
    description=f"hãy vào {topic_mention} để trao đổi với quản lý guild",
    color=0x00ff00)
  await Interaction.response.send_message(embed=response_embed, ephemeral=True)


  @commands.command()
  async def sync(slef, ctx) -> None:
    synced = await self.bot.tree.sync()
    await ctx.send(f"ĐÃ KẾT NỐI THÀNH CÔNG VỚI {len(synced)} SLASH COMMANDS")
    return



#scuid
@bot.tree.command(name="scuid", description="check dữ liệu uid genshin")
async def scuid(Interaction, uid: int):
  try:
      data = await client.fetch_user(uid)
      async def mycallback(Interaction):
        async def showcallback(ctx):  
          try:
            emoji_loading = discord.utils.get(bot.emojis, name="ganyurollst")
            embed_loading = discord.Embed(color=discord.Color.dark_theme())
            embed_loading.add_field(name=f"Đang tạo thông tin {str(emoji_loading)}",value="", inline=False)
            await messages.edit(content=None, embed=embed_loading)
          
            embed=discord.Embed()
            if selects.values[0] == "char1":
                charactert = data.characters[0]
            if selects.values[0] == "char2":
                charactert = data.characters[1]
            if selects.values[0] == "char3":
                charactert = data.characters[2]
            if selects.values[0] == "char4":
                charactert = data.characters[3]
            if selects.values[0] == "char5":
                charactert = data.characters[4]
            if selects.values[0] == "char6":
                charactert = data.characters[5]
            if selects.values[0] == "char7":
                charactert = data.characters[6]
            if selects.values[0] == "char8":
                charactert = data.characters[7]   

          
            embed.add_field(name=f"name: {charactert.name}", value=f"độ yêu thích: {charactert.friendship_level}", inline=False)
            embed.add_field(name=f"level: {charactert.level} / {charactert.max_level}", value="", inline=False)
            embed.set_thumbnail(url=charactert.image.icon.url)
    
            url_goc = "https://cdn.discordapp.com/attachments/1108343090072264826/1114785684641812490/06429B1A-2111-4409-87CF-61067CE180E9.png"
            response = requests.get(url_goc)
            ime_app = BytesIO(response.content)
            image_app = Image.open(ime_app).convert("RGBA").resize((1141, 1134))
            
            font = ImageFont.truetype("zh-cn.ttf", 27)
            draw = ImageDraw.Draw(image_app)
            
            draw.text((38, 24), data.player.nickname, font=font, fill=(255, 255, 255)) #player name
            draw.text((425, 24), (f"AR:{data.player.level}"), font=font, fill=(255, 255, 255)) #player level
            
            #char
            response = requests.get(charactert.image.banner.url)
            image_set_schar0 = BytesIO(response.content)
            image_schar0 = Image.open(image_set_schar0).resize((744, 372))
            image_app.paste(image_schar0, (-120, 135), mask=image_schar0)
            draw.text((34, 572), charactert.name, font=font, fill=(255, 255, 255))  #name0
            draw.text((34, 607), (f"Level:{charactert.level} / {charactert.max_level}"), font=font, fill=(255, 255, 255))  #level0
            draw.text((34, 642), (f"Độ Yêu Thích: {charactert.friendship_level}"), font=font, fill=(255, 255, 255))  #độ yêu thích
            
            #vũ khí
            weapon = charactert.equipments[-1]
            response = requests.get(weapon.detail.icon.url)
            image_set_vk0 = BytesIO(response.content)
            image_vk0 = Image.open(image_set_vk0).resize((144, 144))
            image_app.paste(image_vk0, (654, 82), mask=image_vk0)
          
            draw.text((820, 100), weapon.detail.name, font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255)) #name
            draw.text((644, 98), (f"R{weapon.refinement}"), font=font, fill=(255, 255, 255)) #tinh luyện
            draw.text((970, 164), (f"{weapon.level}/{weapon.max_level}"), font=font, fill=(255, 255, 255)) #level
            draw.text((677, 208), (f"{'*'*weapon.detail.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 38), fill=(255, 255, 0))#rate
            draw.text((842, 164), (f"{weapon.detail.mainstats.value}{'%' if weapon.detail.mainstats.type == DigitType.PERCENT else ''}"), font=font, fill=(255, 255, 255))#atk
            for substate in weapon.detail.substats: #dòng chính
                if substate.name == "Hiệu Quả Nạp Nguyên Tố":
                  draw.text((812, 208), (f"{substate.name.strip()[:12]}: {substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=(255, 255, 255))
                else:
                  draw.text((812, 208), (f"{substate.name}: {substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"), font=ImageFont.truetype("zh-cn.ttf", 19), fill=(255, 255, 255))
          
            
            #Stats
            fontt=ImageFont.truetype("zh-cn.ttf", 25)
            draw.text((688, 280), (f"HP: {int(charactert.stats.FIGHT_PROP_MAX_HP.value)}"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990290942951545/CHUH17121.png")
            hp = BytesIO(response.content)
            hp1 = Image.open(hp).resize((40, 40))
            image_app.paste(hp1, (644, 275), mask=hp1)
  
            draw.text((688, 315), (f"Tân Công: {int(charactert.stats.FIGHT_PROP_CUR_ATTACK.value)}"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://media.discordapp.net/attachments/1118977913392476210/1118990421289357452/atk.png")
            atk = BytesIO(response.content)
            atk1 = Image.open(atk).resize((40, 40))
            image_app.paste(atk1, (644, 310), mask=atk1)
  
            draw.text((688, 355), (f"Phòng Ngự: {int(charactert.stats.FIGHT_PROP_CUR_DEFENSE.value)}"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990526595727501/THFM69251.png")
            def2 = BytesIO(response.content)
            def1 = Image.open(def2).resize((40, 40))
            image_app.paste(def1, (644, 350), mask=def1)
  
            draw.text((688, 395), (f"Tinh Thông Nguyên Tố: {int(charactert.stats.FIGHT_PROP_ELEMENT_MASTERY.value)}"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990526247608361/ttnt.png")
            tt = BytesIO(response.content)
            tt1 = Image.open(tt).resize((40, 40))
            image_app.paste(tt1, (644, 390), mask=tt1)
  
            draw.text((688, 435),(f"Tỉ Lệ Bạo: {charactert.stats.FIGHT_PROP_CRITICAL.value* 100:.0f}%"), font=font, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990420903477248/cr.png")
            tl = BytesIO(response.content)
            tl1 = Image.open(tl).resize((40, 40))
            image_app.paste(tl1, (644, 430), mask=tl1)
  
            draw.text((688, 475),(f"Sát Thương Bạo: {charactert.stats.FIGHT_PROP_CRITICAL_HURT.value* 100:.0f}%"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990421582954577/cd.png")
            st = BytesIO(response.content)
            st1 = Image.open(st).resize((40, 40))
            image_app.paste(st1, (644, 470), mask=st1)
  
            draw.text((688, 515),(f"Hiệu Quả Nạp: {charactert.stats.FIGHT_PROP_CHARGE_EFFICIENCY.value* 100:.0f}%"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990525501022218/hqn.png")
            hqn = BytesIO(response.content)
            hqn1 = Image.open(hqn).resize((40, 40))
            image_app.paste(hqn1, (644, 510), mask=hqn1)

            draw.text((688, 555),(f"trị liệu: {int(charactert.stats.FIGHT_PROP_HEAL_ADD.value * 100)}%"), font=fontt, fill=(255, 255, 255))
            response = requests.get("https://cdn.discordapp.com/attachments/1118977913392476210/1118990525794619402/heal.png")
            tl = BytesIO(response.content)
            tl1 = Image.open(tl).resize((40, 40))
            image_app.paste(tl1, (644, 550), mask=tl1)
            #stnt
            draw.text((710, 605),(f"{int(charactert.stats.FIGHT_PROP_PHYSICAL_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/attachments/1092394580009295952/1119211230872211476/350.png")
            svl = BytesIO(response.content)
            svl1 = Image.open(svl).resize((50, 50))
            image_app.paste(svl1, (660, 585), mask=svl1)

            draw.text((830, 605),(f"{int(charactert.stats.FIGHT_PROP_WIND_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882253026021228544.webp?size=96&quality=lossless")
            stp = BytesIO(response.content)
            stp1 = Image.open(stp).resize((50, 50))
            image_app.paste(stp1, (780, 585), mask=stp1)
            
            draw.text((940, 605),(f"{int(charactert.stats.FIGHT_PROP_ROCK_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882253025895399504.webp?size=96&quality=lossless")
            stn = BytesIO(response.content)
            stn1 = Image.open(stn).resize((50, 50))
            image_app.paste(stn1, (890, 585), mask=stn1)
           
            draw.text((1050, 605),(f"{int(charactert.stats.FIGHT_PROP_ELEC_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882254148584759317.webp?size=96&quality=lossless")
            stl = BytesIO(response.content)
            stl1 = Image.open(stl).resize((50, 50))
            image_app.paste(stl1, (1000, 585), mask=stl1)
           
            draw.text((710, 665),(f"{int(charactert.stats.FIGHT_PROP_GRASS_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882253026113507349.webp?size=96&quality=lossless")
            stt = BytesIO(response.content)
            stt1 = Image.open(stt).resize((50, 50))
            image_app.paste(stt1, (660, 645), mask=stt1)           
          
            draw.text((830, 665),(f"{int(charactert.stats.FIGHT_PROP_WATER_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882254676916068393.webp?size=96&quality=lossless")
            stt2 = BytesIO(response.content)
            stt3 = Image.open(stt2).resize((50, 50))
            image_app.paste(stt3, (780, 645), mask=stt3)          
           
            draw.text((940, 665),(f"{int(charactert.stats.FIGHT_PROP_FIRE_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255)) 
  
            response = requests.get("https://cdn.discordapp.com/emojis/882254077361262592.webp?size=96&quality=lossless")
            sth = BytesIO(response.content)
            sth1 = Image.open(sth).resize((50, 50))
            image_app.paste(sth1, (890, 645), mask=sth1)          
           
            draw.text((1050, 665),(f"{int(charactert.stats.FIGHT_PROP_ICE_ADD_HURT.value * 100)}%"), font=fontt, fill=(255, 255, 255))
  
            response = requests.get("https://cdn.discordapp.com/emojis/882253026046390292.webp?size=96&quality=lossless")
            stb = BytesIO(response.content)
            stb1 = Image.open(stb).resize((50, 50))
            image_app.paste(stb1, (1000, 645), mask=stb1)
          
            #tdv
            fonts = ImageFont.truetype("zh-cn.ttf", 16)
            
            artifact_counts = {}
            for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, charactert.equipments):
                artifact_name_set = artifact.detail.artifact_name_set
                if artifact_name_set in artifact_counts:
                    artifact_counts[artifact_name_set] += 1
                else:
                    artifact_counts[artifact_name_set] = 1
            y_position = 692
            y_offset = 28
            #set tdv
            for artifact_name_set, count in artifact_counts.items(): 
                if count > 1 and count < 4:
                  draw.text((100, y_position), f"{artifact_name_set} {count}", font=ImageFont.truetype("zh-cn.ttf", 24), fill=(37, 247, 128))
                  y_position += y_offset
                if count > 3:
                  draw.text((100, 705), f"{artifact_name_set} {count}", font=ImageFont.truetype("zh-cn.ttf", 26), fill=(37, 247, 128))
            #cv      
            x_cv1 = 26
            x_cv2 = 224
            for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, charactert.equipments):
                crit_rate = 0
                crit_dmg = 0
                for substate in artifact.detail.substats:
                    if substate.name == "Tỷ Lệ Bạo Kích" or substate.name == "ST Bạo Kích":
                        if substate.name == "Tỷ Lệ Bạo Kích":
                            crit_rate = substate.value
                        elif substate.name == "ST Bạo Kích":
                            crit_dmg = substate.value
                cv0 = (crit_rate * 2) + crit_dmg
                draw.text((x_cv1, 1091), (f"CV.{cv0:.1f}"), font=ImageFont.truetype("zh-cn.ttf", 22), fill=(255, 255, 255))
                x_cv1 += x_cv2
            
            x_tdv = 227 #x tổng
            x_tdv_stats1 = 224
            x_tdv_icon = 43 #icon tdv
            x_tdv_level = 36
            x_tdv_rate = 80 #độ hiếm tdv
            x_tdv_stats = 26 #stats tdv
            y_tdv_stats1 = 973 #y stats tdv
            y_tdv_stats2 = 28 
            element_count = 0 #chia bảng 
            for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, charactert.equipments):
              response = requests.get(artifact.detail.icon.url)
              image_set_tdv0 = BytesIO(response.content)
              image_tdv0 = Image.open(image_set_tdv0).resize((165, 165))
              image_app.paste(image_tdv0, (x_tdv_icon, 775), mask=image_tdv0)
              x_tdv_icon += x_tdv
  
              draw.text((x_tdv_rate, 910), (f"{'*'*artifact.detail.rarity}"), font=ImageFont.truetype("zh-cn.ttf", 38), fill=(255, 255, 0))
              x_tdv_rate += x_tdv
              
              draw.text((x_tdv_stats, 945), artifact.detail.mainstats.name, font=fonts, fill=(255, 255, 255))
  
              draw.text((x_tdv_level, 795), (f"+{artifact.level}"), font=ImageFont.truetype("zh-cn.ttf", 24), fill=(255, 255, 255))
              x_tdv_level += x_tdv
              for substate in artifact.detail.substats:
                if substate.name == "Hiệu Quả Nạp Nguyên Tố":
                  name_sst = substate.name.strip()[:12]
                elif substate.name == "Tinh Thông Nguyên Tố":
                  name_sst = substate.name.strip()[:10]
                else:
                  name_sst = substate.name
                draw.text((x_tdv_stats, y_tdv_stats1), (f"{name_sst} {substate.value}{'%' if substate.type == DigitType.PERCENT else ''}"), font=ImageFont.truetype("zh-cn.ttf", 18), fill=(255, 255, 255))
                y_tdv_stats1 += y_tdv_stats2
                element_count += 1
                if element_count % 4 == 0:
                  y_tdv_stats1 = 973
                  x_tdv_stats += x_tdv_stats1
                
  
          
            #thiên phú
            response = requests.get(charactert.skills[0].icon.url)  #skill1
            image_set_skill00 = BytesIO(response.content)
            image_skill00 = Image.open(image_set_skill00).resize((60, 60))
            image_app.paste(image_skill00, (532, 83), mask=image_skill00)
          
            response = requests.get(charactert.skills[1].icon.url)  #skill2
            image_set_skill01 = BytesIO(response.content)
            image_skill01 = Image.open(image_set_skill01).resize((60, 60))
            image_app.paste(image_skill01, (532, 142), mask=image_skill01)
          
            response = requests.get(charactert.skills[2].icon.url)  #skill3
            image_set_skill02 = BytesIO(response.content)
            image_skill02 = Image.open(image_set_skill02).resize((60, 60)).convert('RGBA')
            image_app.paste(image_skill02, (532, 204), mask=image_skill02)
            draw.text((534, 116), (f"     {charactert.skills[0].level}"),font=font,fill=(255, 255, 255))
            draw.text((534, 176), (f"     {charactert.skills[1].level}"),font=font,fill=(255, 255, 255))
            draw.text((534, 238), (f"     {charactert.skills[2].level}"),font=font,fill=(255, 255, 255))
          
            if charactert.constellations_unlocked > 0:
            #cung  mệnh 1
              constellation = charactert.constellations[0]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 291), mask=image_skill00)
          
            if charactert.constellations_unlocked > 1:
              #cung  mệnh 2
              constellation = charactert.constellations[1]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 356), mask=image_skill00)
          
            if charactert.constellations_unlocked > 2:
              #cung  mệnh 3
              constellation = charactert.constellations[2]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 418), mask=image_skill00)
          
            if charactert.constellations_unlocked > 3:
              #cung  mệnh 4
              constellation = charactert.constellations[3]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 480), mask=image_skill00)
          
            if charactert.constellations_unlocked > 4:
              #cung  mệnh 5
              constellation = charactert.constellations[4]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 540), mask=image_skill00)
          
            
            #cung  mệnh 6
            if charactert.constellations_unlocked > 5:
              constellation = charactert.constellations[5]
              response = requests.get(constellation.icon.url) #skill1
              image_set_skill00 = BytesIO(response.content)
              image_skill00 = Image.open(image_set_skill00).resize((60, 60))
              image_app.paste(image_skill00, (532, 599), mask=image_skill00) 
            
            buffer = BytesIO()
            image_app.save(buffer, format='png')
            buffer.seek(0)
            file = discord.File(buffer, filename="showcase.png")
          
            embed.add_field(name="showcase", value="", inline=False)
            channel = bot.get_channel(1118613556938678282)
            message = await channel.send(file=file)
            file_url = message.attachments[0].url
            embed = discord.Embed(color=discord.Color.dark_theme(), timestamp=datetime.now())
            embed.add_field(name=f"Name.{charactert.name}", value=f"Level.{charactert.level} \nnguyên tố.{charactert.element} C.{charactert.constellations_unlocked} \nrate.{'⭐'*charactert.rarity}", inline=False)
            embed.set_image(url=file_url)   
            embed.set_thumbnail(url=f"{charactert.image.icon.url}")
            embed.set_footer(text=f"{uid}", icon_url=f"{ctx.user.avatar}")
            await messages.edit(content=None, embed=embed)
          except Exception as b:
            print(b)
            return b

        options = []
        if len(data.characters) > 0:
          options.append(discord.SelectOption(label=f"{data.characters[0].name}", value="char1"))
        if len(data.characters) > 1:
          options.append(discord.SelectOption(label=f"{data.characters[1].name}", value="char2"))
        if len(data.characters) > 2:
          options.append(discord.SelectOption(label=f"{data.characters[2].name}", value="char3"))
        if len(data.characters) > 3:
          options.append(discord.SelectOption(label=f"{data.characters[3].name}", value="char4"))
        if len(data.characters) > 4:
          options.append(discord.SelectOption(label=f"{data.characters[4].name}", value="char5"))
        if len(data.characters) > 5:
          options.append(discord.SelectOption(label=f"{data.characters[5].name}", value="char6"))
        if len(data.characters) > 6:
          options.append(discord.SelectOption(label=f"{data.characters[6].name}", value="char7"))
        if len(data.characters) > 7:
          options.append(discord.SelectOption(label=f"{data.characters[7].name}", value="char8"))
    
        selects = discord.ui.Select(placeholder="showcase", options=options)
        selects.callback = showcallback
        views = discord.ui.View()
        views.add_item(selects)

        embed=discord.Embed()
        embed.add_field(name="hãy chọn 1 options",value="__nếu tương tác không thành công vui lòng đợi 1 đến 2 giây \n**và ko cần chọn lại**__")
        messages = await Interaction.channel.send(embed=embed, view=views)
        await message_scuid.delete()
  
      url_goc = 'https://cdn.discordapp.com/attachments/1093887180096671824/1100077580008312922/Khong_Co_Tieu_e36_20230424221522.png'
      response = requests.get(url_goc)
      ime_app = BytesIO(response.content)
      image_app = Image.open(ime_app).convert("RGBA")
    
      font = ImageFont.truetype("zh-cn.ttf", 14)
      draw = ImageDraw.Draw(image_app)
    
      emoji_thanhtuu = discord.utils.get(bot.emojis, name="thanhtuu_beebot")
      emoji_lahoan = discord.utils.get(bot.emojis, name="lahoan_beebot")
      emoji_owo = discord.utils.get(bot.emojis, name="kiemanh")
      emoji_enka = discord.utils.get(bot.emojis, name="enka_beebot")
      emoji_aspirine = discord.utils.get(bot.emojis, name="aspirine_beebot")
      embed = discord.Embed()
      embed.add_field(name="vui lòng đợi thông tin được sử lý",
                      value="",
                      inline=False)
      await Interaction.response.send_message(embed=embed, ephemeral=True)
      if data.characters is not None and len(data.characters) > 0:
        if len(data.characters) > 0:
          #char0
          response = requests.get(data.characters[0].image.icon.url)
          image_set_char0 = BytesIO(response.content)
          image_char0 = Image.open(image_set_char0).resize((50, 50))
          image_app.paste(image_char0, (10, 60), mask=image_char0)
          draw.text((12, 122), data.characters[0].name, font=font,
                    fill=(0, 0, 0))  #name0
          draw.text((63, 80), (
            f"level:{data.characters[0].level}     C {data.characters[0].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level0
          #skill_char0
          response = requests.get(data.characters[0].skills[0].icon.url)  #skill1
          image_set_skill00 = BytesIO(response.content)
          image_skill00 = Image.open(image_set_skill00).resize((20, 20))
          image_app.paste(image_skill00, (61, 97), mask=image_skill00)
    
          response = requests.get(data.characters[0].skills[1].icon.url)  #skill2
          image_set_skill01 = BytesIO(response.content)
          image_skill01 = Image.open(image_set_skill01).resize((20, 20))
          image_app.paste(image_skill01, (101, 97), mask=image_skill01)
    
          response = requests.get(data.characters[0].skills[2].icon.url)  #skill3
          image_set_skill02 = BytesIO(response.content)
          image_skill02 = Image.open(image_set_skill02).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill02, (137, 97), mask=image_skill02)
          draw.text((61, 98), (f"     {data.characters[0].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((101, 98), (f"     {data.characters[0].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((137, 98), (f"     {data.characters[0].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 1:
          #char1
          response = requests.get(data.characters[1].image.icon.url)
          image_set_char1 = BytesIO(response.content)
          image_char1 = Image.open(image_set_char1).resize((50, 50))
          image_app.paste(image_char1, (191, 60), mask=image_char1)
          draw.text((195, 122), data.characters[1].name, font=font,
                    fill=(0, 0, 0))  #name1
          draw.text((244, 80), (
            f"level:{data.characters[1].level}     C {data.characters[1].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level1
          #skill_char1
          response = requests.get(data.characters[1].skills[0].icon.url)  #skill1
          image_set_skill10 = BytesIO(response.content)
          image_skill10 = Image.open(image_set_skill10).resize((20, 20))
          image_app.paste(image_skill10, (241, 97), mask=image_skill10)
    
          response = requests.get(data.characters[1].skills[1].icon.url)  #skill2
          image_set_skill11 = BytesIO(response.content)
          image_skill11 = Image.open(image_set_skill11).resize((20, 20))
          image_app.paste(image_skill11, (282, 97), mask=image_skill11)
    
          response = requests.get(data.characters[1].skills[2].icon.url)  #skill3
          image_set_skill12 = BytesIO(response.content)
          image_skill12 = Image.open(image_set_skill12).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill12, (320, 97), mask=image_skill12)
          draw.text((241, 98), (f"     {data.characters[1].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((282, 98), (f"     {data.characters[1].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((320, 98), (f"     {data.characters[1].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 2:
          #char2
          response = requests.get(data.characters[2].image.icon.url)
          image_set_char2 = BytesIO(response.content)
          image_char2 = Image.open(image_set_char2).resize((50, 50))
          image_app.paste(image_char2, (372, 60), mask=image_char2)
          draw.text((378, 122), data.characters[2].name, font=font,
                    fill=(0, 0, 0))  #name2
          draw.text((425, 80), (
            f"level:{data.characters[2].level}     C {data.characters[2].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level2
          #skill_char2
          response = requests.get(data.characters[2].skills[0].icon.url)  #skill1
          image_set_skill20 = BytesIO(response.content)
          image_skill20 = Image.open(image_set_skill20).resize((20, 20))
          image_app.paste(image_skill20, (423, 97), mask=image_skill20)
    
          response = requests.get(data.characters[2].skills[1].icon.url)  #skill2
          image_set_skill21 = BytesIO(response.content)
          image_skill21 = Image.open(image_set_skill21).resize((20, 20))
          image_app.paste(image_skill21, (463, 97), mask=image_skill21)
    
          response = requests.get(data.characters[2].skills[2].icon.url)  #skill3
          image_set_skill22 = BytesIO(response.content)
          image_skill22 = Image.open(image_set_skill22).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill22, (503, 97), mask=image_skill22)
          draw.text((423, 98), (f"     {data.characters[2].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((463, 98), (f"     {data.characters[2].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((502, 98), (f"     {data.characters[2].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 3:
          #char3
          response = requests.get(data.characters[3].image.icon.url)
          image_set_char3 = BytesIO(response.content)
          image_char3 = Image.open(image_set_char3).resize((50, 50))
          image_app.paste(image_char3, (553, 60), mask=image_char3)
          draw.text((561, 122), data.characters[3].name, font=font,
                    fill=(0, 0, 0))  #name3
          draw.text((606, 80), (
            f"level:{data.characters[3].level}     C {data.characters[3].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level3
          #skill_char3
          response = requests.get(data.characters[3].skills[0].icon.url)  #skill1
          image_set_skill30 = BytesIO(response.content)
          image_skill30 = Image.open(image_set_skill30).resize((20, 20))
          image_app.paste(image_skill30, (605, 97), mask=image_skill30)
    
          response = requests.get(data.characters[3].skills[1].icon.url)  #skill2
          image_set_skill31 = BytesIO(response.content)
          image_skill31 = Image.open(image_set_skill31).resize((20, 20))
          image_app.paste(image_skill31, (645, 97), mask=image_skill31)
    
          response = requests.get(data.characters[3].skills[2].icon.url)  #skill3
          image_set_skill32 = BytesIO(response.content)
          image_skill32 = Image.open(image_set_skill32).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill32, (684, 97), mask=image_skill32)
          draw.text((605, 98), (f"     {data.characters[3].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((645, 98), (f"     {data.characters[3].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((684, 98), (f"     {data.characters[3].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 4:
          #char4
          response = requests.get(data.characters[4].image.icon.url)
          image_set_char4 = BytesIO(response.content)
          image_char4 = Image.open(image_set_char4).resize((50, 50))
          image_app.paste(image_char4, (10, 214), mask=image_char4)
          draw.text((12, 273), data.characters[4].name, font=font,
                    fill=(0, 0, 0))  #name4
          draw.text((63, 230), (
            f"level:{data.characters[4].level}     C {data.characters[4].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level4
          #skill_char4
          response = requests.get(data.characters[4].skills[0].icon.url)  #skill1
          image_set_skill40 = BytesIO(response.content)
          image_skill40 = Image.open(image_set_skill40).resize((20, 20))
          image_app.paste(image_skill40, (61, 247), mask=image_skill40)
    
          response = requests.get(data.characters[4].skills[1].icon.url)  #skill2
          image_set_skill41 = BytesIO(response.content)
          image_skill41 = Image.open(image_set_skill41).resize((20, 20))
          image_app.paste(image_skill41, (102, 247), mask=image_skill41)
    
          response = requests.get(data.characters[4].skills[2].icon.url)  #skill3
          image_set_skill42 = BytesIO(response.content)
          image_skill42 = Image.open(image_set_skill42).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill42, (140, 247), mask=image_skill42)
          draw.text((61, 248), (f"     {data.characters[4].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((102, 248), (f"     {data.characters[4].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((140, 248), (f"     {data.characters[4].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 5:
          #char5
          response = requests.get(data.characters[5].image.icon.url)
          image_set_char5 = BytesIO(response.content)
          image_char5 = Image.open(image_set_char5).resize((50, 50))
          image_app.paste(image_char5, (193, 214), mask=image_char5)
          draw.text((195, 273), data.characters[5].name, font=font,
                    fill=(0, 0, 0))  #name5
          draw.text((244, 230), (
            f"level:{data.characters[5].level}     C {data.characters[5].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level5
          #skill_char5
          response = requests.get(data.characters[5].skills[0].icon.url)  #skill1
          image_set_skill50 = BytesIO(response.content)
          image_skill50 = Image.open(image_set_skill50).resize((20, 20))
          image_app.paste(image_skill50, (243, 247), mask=image_skill50)
    
          response = requests.get(data.characters[5].skills[1].icon.url)  #skill2
          image_set_skill51 = BytesIO(response.content)
          image_skill51 = Image.open(image_set_skill51).resize((20, 20))
          image_app.paste(image_skill51, (285, 247), mask=image_skill51)
    
          response = requests.get(data.characters[5].skills[2].icon.url)  #skill3
          image_set_skill52 = BytesIO(response.content)
          image_skill52 = Image.open(image_set_skill52).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill52, (323, 247), mask=image_skill52)
          draw.text((243, 248), (f"     {data.characters[5].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((285, 248), (f"     {data.characters[5].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((323, 248), (f"     {data.characters[5].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 6:
          #char6
          response = requests.get(data.characters[6].image.icon.url)
          image_set_char6 = BytesIO(response.content)
          image_char6 = Image.open(image_set_char6).resize((50, 50))
          image_app.paste(image_char6, (374, 214), mask=image_char6)
          draw.text((378, 273), data.characters[6].name, font=font,
                    fill=(0, 0, 0))  #name6
          draw.text((425, 230), (
            f"level:{data.characters[6].level}     C {data.characters[6].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level6
          #skill_char6
          response = requests.get(data.characters[6].skills[0].icon.url)  #skill1
          image_set_skill60 = BytesIO(response.content)
          image_skill60 = Image.open(image_set_skill60).resize((20, 20))
          image_app.paste(image_skill60, (426, 247), mask=image_skill60)
    
          response = requests.get(data.characters[6].skills[1].icon.url)  #skill2
          image_set_skill61 = BytesIO(response.content)
          image_skill61 = Image.open(image_set_skill61).resize((20, 20))
          image_app.paste(image_skill61, (467, 247), mask=image_skill61)
    
          response = requests.get(data.characters[6].skills[2].icon.url)  #skill3
          image_set_skill62 = BytesIO(response.content)
          image_skill62 = Image.open(image_set_skill62).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill62, (506, 247), mask=image_skill62)
          draw.text((426, 248), (f"     {data.characters[6].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((467, 248), (f"     {data.characters[6].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((506, 248), (f"     {data.characters[6].skills[2].level}"),
                    font=font,
                    fill=(255, 255, 255))
        if len(data.characters) > 7:
          #char7
          response = requests.get(data.characters[7].image.icon.url)
          image_set_char7 = BytesIO(response.content)
          image_char7 = Image.open(image_set_char7).resize((50, 50))
          image_app.paste(image_char7, (558, 214), mask=image_char7)
          draw.text((561, 273), data.characters[7].name, font=font,
                    fill=(0, 0, 0))  #name7
          draw.text((606, 230), (
            f"level:{data.characters[7].level}     C {data.characters[7].constellations_unlocked}"
          ),
                    font=font,
                    fill=(0, 0, 0))  #level7
          #skill_char7
          response = requests.get(data.characters[7].skills[0].icon.url)  #skill1
          image_set_skill70 = BytesIO(response.content)
          image_skill70 = Image.open(image_set_skill70).resize((20, 20))
          image_app.paste(image_skill70, (608, 247), mask=image_skill70)
    
          response = requests.get(data.characters[7].skills[1].icon.url)  #skill2
          image_set_skill71 = BytesIO(response.content)
          image_skill71 = Image.open(image_set_skill71).resize((20, 20))
          image_app.paste(image_skill71, (648, 247), mask=image_skill71)
    
          response = requests.get(data.characters[7].skills[2].icon.url)  #skill3
          image_set_skill72 = BytesIO(response.content)
          image_skill72 = Image.open(image_set_skill72).resize(
            (20, 20)).convert('RGBA')
          image_app.paste(image_skill72, (687, 247), mask=image_skill72)
          draw.text((608, 248), (f"     {data.characters[7].skills[0].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((648, 248), (f"     {data.characters[7].skills[1].level}"),
                    font=font,
                    fill=(255, 255, 255))
          draw.text((687, 248), (f"     {data.characters[7].skills[2].level}"),
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
    
      embed.set_thumbnail(url=f"{data.player.avatar.icon.url}")
      embed.add_field(name=f"`name:` **{data.player.nickname}**",
                      value=f"",
                      inline=False)
    
      embed.add_field(name=f"`chữ ký:` {data.player.signature}",
                      value='',
                      inline=False)
    
      embed.add_field(
        name='',
        value=f' {str(emoji_thanhtuu)} `Thành Tựu:` **{data.player.achievement}**',
        inline=True)
    
      embed.add_field(
        name='',
        value=
        f' {str(emoji_lahoan)} `La Hoàn:` **{data.player.abyss_floor} - {data.player.abyss_room}**',
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
      channel = Interaction.channel
    
      
      buttonst1 = discord.ui.Button(label="showcase", style=discord.ButtonStyle.green)
      buttonst1.callback = mycallback
      view = discord.ui.View()
      if len(data.characters) > 0:
        view.add_item(buttonst1)

      channel = bot.get_channel(1118613556938678282)
      saved_file = await channel.send(file=filet)
            
       # Lấy link của file
      files_url = saved_file.attachments[0].url
      embed.set_image(url=files_url)
      
      channel = Interaction.channel
      message_scuid = await channel.send(embed=embed, view=view)
  except Exception as s:
      await Interaction.channel.send(s)
      return s





          TSA = 0
          emoji_list = []
          for TS in data.characters:
              charnames = data.characters[TSA].name
              NAMES = charnames.replace(' ', '')
              emoji_url = data.characters[TSA].image.icon.url
              old_emoji = discord.utils.get(guild.emojis, name=NAMES)
              async with self.session.get(emoji_url) as resp:
                  if resp.status == 200:
                      image_data = await resp.read()
                      guild = self.bot.get_guild(1092371021908152390)
                      emoji = await guild.create_custom_emoji(name=NAMES, image=image_data)
                      emoji_list.append(emoji)
                      TSA += 1
                  else:
                      print(f"Không thể tải hình ảnh từ URL cho emoji {NAMES}.")

        TSA = 0
        for TS in data.characters:
            NAMES = f"char{TSA}"
            emoji_url = data.characters[TSA].image.icon.url
            async with self.session.get(emoji_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    guild = self.bot.get_guild(1092371021908152390)
                    old_emoji = discord.utils.get(self.bot.emojis, name=NAMES)
                    if old_emoji is not None:
                      await old_emoji.delete()
                    emoji = await guild.create_custom_emoji(name=NAMES, image=image_data)
                    emoji_list.append(emoji)
                    TSA += 1
                else:
                    print(f"Không thể tải hình ảnh từ URL cho emoji {NAMES}.")

    
          options = []
          
          for i in range(min(len(data.characters), 8)):
              char = data.characters[i]
              options.append(discord.SelectOption(label=char.name, value=f"char{i+1}", emoji=emoji_list[i]))




import discord
from discord import app_commands
from discord.ext import commands
import os 

class token(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  
  @commands.Cog.listener()
  async def on_ready(self):
    filename = os.path.basename(__file__)
    print(f"[OK] {self.bot.user.name}#{self.bot.user.discriminator} - {filename} sᴜᴄᴄᴇssғᴜʟʟʏ")
    print('='* 50)

  
  @app_commands.command(name="token", description="dùng để trao đổi với quản lý guild!!!")
  async def token(self, Interaction):

    channel = self.bot.get_channel(699305290289381477)

    if not channel:
      return await Interaction.respond.send_message("Không tìm thấy kênh chỉ định.")
    
    anonymous_topic = await channel.create_thread(
      name=f'Tiket {Interaction.user.name}',
      type=discord.ChannelType.private_thread)
  
    role = Interaction.guild.get_role(1087675803170525254)
  
    await anonymous_topic.send(
      f"Cuộc trao đổi giữ {Interaction.user.mention} với {role.mention}! hãy bắt đầu bằng điều bạn muốn nói"
    )
  
    topic_mention = anonymous_topic.mention
    response_embed = discord.Embed(
      title="tạo token thành công",
      description=f"hãy vào {topic_mention} để trao đổi với quản lý guild",
      color=0x00ff00)
    await Interaction.response.send_message(embed=response_embed, ephemeral=True)

async def setup(bot):
  await bot.add_cog(token(bot))


 @app_commands.command(name='redeem')
  @app_commands.describe(games='game code redeem')
  @app_commands.choices(games=[
    discord.app_commands.Choice(name="GENSHIN", value=1),
    discord.app_commands.Choice(name="STARRAIL", value=2),])
  async def code(self, Interaction, code: str, games: discord.app_commands.Choice[int]):



@tasks.loop(seconds=30)
async def run_data():
  await test_diary()
  await test_diarys()


async def test_diary():
  emoji_nthach = discord.utils.get(bot.emojis, name="nthach")
  emoji_nas = discord.utils.get(bot.emojis, name="nas")
  emoji_smkp = discord.utils.get(bot.emojis, name="smkp")
  emoji_nhua = discord.utils.get(bot.emojis, name="nhua")
  emoji_xuam = discord.utils.get(bot.emojis, name="xuam")
  emoji_uythac = discord.utils.get(bot.emojis, name="uythac")
  emoji_bosstuan = discord.utils.get(bot.emojis, name="bosstuan")
  client1 = genshin.Client(
    {
      "ltuid_v2": 139734936,
      "ltoken_v2":
      'v2_CAISDGM5b3FhcTNzM2d1OBokYWRmZDE3ZTMtMDc1Ny00ZTI2LTgxY2ItZDhhY2Y2MTYxNGY3IMfa96cGKL_NlzEwmN_QQg==',
      "ltmid_v2": '1kvjdm9qmp_hy',
      "cookie_token_v2":
      'v2_CAQSDGM5b3FhcTNzM2d1OBokYWRmZDE3ZTMtMDc1Ny00ZTI2LTgxY2ItZDhhY2Y2MTYxNGY3IMfa96cGKJbYt-EFMJjf0EI=',
      "account_mid_v2": '1kvjdm9qmp_hy',
      "account_id_v2": 139734936
    },
    lang="vi-vn")
  data = await client1.get_notes(831335713)

  date = await client1.get_starrail_notes(800064954)

  embed = discord.Embed()
  datasss = await client1.get_hoyolab_user()
  embed.add_field(name=f'Name: {datasss.nickname}', value='', inline=False)

  diary2 = await client1.get_starrail_diary()
  embed.add_field(
    name=
    f"{str(emoji_nas)} **Ngọc sao trong tháng:** ``{diary2.data.current_hcoin}``",
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_smkp)} **Sức mạnh khai phá:** ``{date.current_stamina}/{date.max_stamina}`` __{date.stamina_recover_time}__',
    value='',
    inline=False)

  signed_ins, claimed_rewardss = await client1.get_reward_info(
    game=genshin.types.Game.STARRAIL)
  embed.add_field(
    name=
    f"[STARRAIL] **Đã nhận:** ``{signed_ins}`` | **Ngày đã nhận:** ``{claimed_rewardss}``",
    value='',
    inline=False)

  diary1 = await client1.get_genshin_diary()
  embed.add_field(
    name=
    f"{str(emoji_nthach)} **Nguyên thạch trong tháng:** ``{diary1.data.current_primogems}``",
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_nhua)} **Nhựa:** ``{data.current_resin}/{data.max_resin}`` __{data.remaining_resin_recovery_time}__',
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_xuam)} **Xu ấm:** ``{data.current_realm_currency}/{data.max_realm_currency}`` __{data.remaining_realm_currency_recovery_time}__',
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_uythac)} **Ủy thác:** ``{data.completed_commissions}/{data.max_commissions}`` **Nhận thưởng:**``{data.claimed_commission_reward}``',
    value='',
    inline=False)

  embed.add_field(
    name=
    f"{str(emoji_bosstuan)} **Boss tuần:** ``{data.remaining_resin_discounts}/{data.max_resin_discounts}``",
    value='',
    inline=False)

  signed_in, claimed_rewards = await client1.get_reward_info(
    game=genshin.types.Game.GENSHIN)
  embed.add_field(
    name=
    f"[GENSHIN] **Đã nhận:** ``{signed_in}`` | **Ngày đã nhận:** ``{claimed_rewards}``",
    value='',
    inline=False)

  channel = bot.get_channel(1118613556938678282)
  message = await channel.fetch_message(1151107614667706388)
  await message.edit(content=None, embed=embed)


async def test_diarys():
  emoji_nthach = discord.utils.get(bot.emojis, name="nthach")
  emoji_nhua = discord.utils.get(bot.emojis, name="nhua")
  emoji_xuam = discord.utils.get(bot.emojis, name="xuam")
  emoji_uythac = discord.utils.get(bot.emojis, name="uythac")
  emoji_bosstuan = discord.utils.get(bot.emojis, name="bosstuan")
  client2 = genshin.Client(
    {
      "ltuid": 89595259,
      "ltoken": 'W26k5CAFSzoR5UHCXMNXBoLdgWahoe2VNIKEIsjb'
    },
    lang="vi-vn")
  data = await client2.get_notes(816851810)

  embed = discord.Embed()
  datasss = await client2.get_hoyolab_user()
  embed.add_field(name=f'Name: {datasss.nickname}', value='', inline=False)

  diary = await client2.get_genshin_diary()
  embed.add_field(
    name=
    f"{str(emoji_nthach)} **Nguyên thạch trong tháng:** ``{diary.data.current_primogems}``",
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_nhua)} **Nhựa:** ``{data.current_resin}/{data.max_resin}`` __{data.remaining_resin_recovery_time}__',
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_xuam)} **Xu ấm:** ``{data.current_realm_currency}/{data.max_realm_currency}`` __{data.remaining_realm_currency_recovery_time}__',
    value='',
    inline=False)

  embed.add_field(
    name=
    f'{str(emoji_uythac)} **Ủy thác:** ``{data.completed_commissions}/{data.max_commissions}`` **Nhận thưởng:**``{data.claimed_commission_reward}``',
    value='',
    inline=False)

  embed.add_field(
    name=
    f"{str(emoji_bosstuan)} **Boss tuần:** ``{data.remaining_resin_discounts}/{data.max_resin_discounts}``",
    value='',
    inline=False)

  signed_in, claimed_rewards = await client2.get_reward_info(
    game=genshin.types.Game.GENSHIN)
  embed.add_field(
    name=
    f"[GENSHIN] **Đã nhận:** ``{signed_in}`` | **Ngày đã nhận:** ``{claimed_rewards}``",
    value='',
    inline=False)

  signed_ins, claimed_rewardss = await client2.get_reward_info(
    game=genshin.types.Game.STARRAIL)
  embed.add_field(
    name=
    f"[STARRAIL] **Đã nhận:** ``{signed_ins}`` | **Ngày đã nhận:** ``{claimed_rewardss}``",
    value='',
    inline=False)

  channel = bot.get_channel(1118613556938678282)
  message = await channel.fetch_message(1151107627418390621)
  await message.edit(content=None, embed=embed)


