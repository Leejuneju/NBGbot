import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime, timezone

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

team_names = ["경쟁스쿼드 1팀", "경쟁스쿼드 2팀", "경쟁스쿼드 3팀", "경쟁스쿼드 4팀", "경쟁스쿼드 5팀"]
current_team_index = 0

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='팀짜기')
async def divide_teams(ctx, team_size: int):
    global current_team_index

    if team_size <= 0:
        await ctx.send("팀의 인원 수는 1 이상이어야 합니다.")
        return

    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("음성 채널에 연결되어 있지 않습니다.")
        return

    members = voice_channel.members

    if len(members) < team_size:
        await ctx.send("팀의 인원 수가 부족합니다.")
        return

    random.shuffle(members)
    num_teams = len(members) // team_size
    teams = [members[i:i + team_size] for i in range(0, len(members), team_size)]

    current_team_index = 0  # 매 호출마다 항상 0으로 설정합니다.

    for i, team in enumerate(teams):
        team_name = team_names[current_team_index]
        current_team_index = (current_team_index + 1) % len(team_names)  # 다음 팀 이름을 가져오기 위해 인덱스를 증가시킵니다.
        team_str = f"{team_name}: " + ', '.join([member.mention for member in team])
        await ctx.send(team_str)


@bot.command(name='랜덤뽑기')
async def pick_random_members(ctx, num_winners: int):
    voice_channel = ctx.author.voice.channel

    if not voice_channel:
        await ctx.send("음성 채널에 연결되어 있지 않습니다.")
        return

    members = voice_channel.members

    if not members:
        await ctx.send("음성 채널에 아무도 없습니다.")
        return

    if num_winners < 1 or num_winners > len(members):
        await ctx.send("유효하지 않은 당첨 인원 수입니다. 음성 채널의 참여 인원 수보다 작거나 같아야 합니다.")
        return

    winners = random.sample(members, num_winners)
    winners_names = [winner.nick or winner.name for winner in winners]

    await ctx.send(f"축하합니다! 당첨된 참여자들: {', '.join(winners_names)}")
    


    User
@bot.command(name='외출일지')
async def outing_journal(ctx):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = ctx.author.nick or ctx.author.name  # 사용자의 별명 또는 이름 가져오기
    user_id = ctx.author.id  # 사용자의 ID 가져오기

    async def get_user_input(prompt):
        prompt_msg = await ctx.send(prompt)
        try:
            response = await bot.wait_for('message', timeout=30.0, check=lambda message: message.author == ctx.author)
            await response.delete()  # 입력 받은 메시지 삭제
            await prompt_msg.delete()  # 봇이 보낸 메시지 삭제
            return response.content
        except asyncio.TimeoutError:
            await ctx.send("시간 초과되었습니다.")
            return None

    server_name = await get_user_input("서버 이름을 입력하세요:")
    if server_name is None:
        return

    reason = await get_user_input("외출 사유를 입력하세요:")
    if reason is None:
        return

    # 외출일지 정보를 출력
    outing_info = f"**외출일지**\n작성자: {user_name}\n날짜 및 시간: {now}\n서버 이름: {server_name}\n외출 사유: {reason}"
    await ctx.send(outing_info)

    # 사용자의 디스코드 ID 목록
    target_users = ["504614649963216908", "429636528281747457"]

    # 외출일지 정보를 DM으로 보내기
    for user_id in target_users:
        user = await bot.fetch_user(user_id)
        if user:
            dm_content = f"외출일지를 작성해주셔서 감사합니다!\n\n{outing_info}"
            await user.send(dm_content)
        else:
            await ctx.send("사용자를 찾을 수 없습니다. DM을 보낼 수 없습니다.")





# 사용자의 디스코드 ID를 여기에 입력하세요.
allowed_user_id = '504614649963216908'

@bot.command(name='삭제')
async def delete_today_messages(ctx, user_nickname):
    try:
        # 명령어를 실행하려는 사용자의 ID 확인
        user_id = str(ctx.author.id)

        # 사용자 ID 확인 후 명령어 실행 여부 결정
        if user_id == allowed_user_id:
            channel = ctx.channel

            # 현재 시간의 timestamp를 얻습니다.
            now = datetime.now(timezone.utc).timestamp()

            # 채널의 메시지를 반복하면서 해당 사용자가 오늘 보낸 메시지를 삭제합니다.
            async for message in channel.history(limit=None):
                if message.author.display_name == user_nickname:
                    # 메시지의 timestamp와 현재 시간의 timestamp를 비교하여 오늘 보낸 메시지인지 확인합니다.
                    if (now - message.created_at.timestamp()) / 3600 <= 24:
                        await message.delete()
        else:
            await ctx.send("해당 명령어를 사용할 수 있는 권한이 없습니다.")
    except asyncio.TimeoutError:
        await ctx.send("시간 초과되었습니다. 다시 시도해주세요.")



# 디스코드 봇 토큰을 사용하여 봇 로그인
# 여기에는 본인이 발급받은 디스코드 봇 토큰을 입력해야 합니다.
bot.run('MTIyNzQ1MDgwMjE0MzIzNjE4OA.GzbVmW.xhSByzDN1Y6y8fJueRhxqlfoPXfnAwtwmFoik0') 