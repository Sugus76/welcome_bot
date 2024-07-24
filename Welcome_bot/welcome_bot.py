import discord
from discord.ext import commands, tasks
import datetime
import aiohttp
import pytz

TOKEN = ''  # Replace with your actual bot token
intents = discord.Intents.default()
intents.members = True  # Enable the members intent

bot = commands.Bot(command_prefix='!', intents=intents)

# Role IDs
role_ids = {
    '': ,  # Replace with your role IDs
}

# Channel IDs where the bot should send the online and offline messages
online_message_channel_id = 1247911709222633503  # Replace with your channel ID
offline_message_channel_id = 1247911709222633503  # Replace with your channel ID

# Counters
join_count = 0
leave_count = 0

# Set the timezone to Bangkok (Indochina Time)
bangkok_timezone = pytz.timezone('Asia/Bangkok')

# Replace with your actual PING_URL
PING_URL = 'https://example.com/ping'

@bot.event
async def on_ready():
    global join_count, leave_count
    print(f'Bot is ready. Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Twitch!"), status=discord.Status.online)
    ping_server_task.start()  # Start the ping task

    # Fetch the channel where the bot should send the online message
    online_message_channel = bot.get_channel(online_message_channel_id)

    if online_message_channel is not None:
        logo_url = ''  # Replace with your actual logo URL
        gif_url = ''  # Replace with your actual GIF URL
        embed = discord.Embed(
            title="🟢⋯𝐁𝐎𝐓 𝐎𝐍𝐋𝐈𝐍𝐄⋯🟢",
            description=f"𝗕𝗢𝗧 𝗜𝗦 𝗡𝗢𝗪 𝗢𝗡𝗟𝗜𝗡𝗘 𝗔𝗡𝗗 𝗥𝗘𝗔𝗗𝗬 𝗧𝗢 𝗦𝗘𝗥𝗩𝗘𝗥 𝗜𝗡.",
            color=discord.Color.green()
        )
        embed.set_author(name="", icon_url=logo_url)
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Online since : {datetime.datetime.now(bangkok_timezone).strftime('%a %d %b %Y, %I:%M%p')}", icon_url=logo_url)

        # Send embed to the online message channel
        await online_message_channel.send(embed=embed)
    else:
        print(f"Could not find the channel with ID {online_message_channel_id}.")

@bot.event
async def on_disconnect():
    global leave_count
    # Fetch the channel where the bot should send the offline message
    offline_message_channel = bot.get_channel(offline_message_channel_id)

    if offline_message_channel is not None:
        logo_url = ''  # Replace with your actual logo URL
        gif_url = ''  # Replace with your actual GIF URL
        embed = discord.Embed(
            title="🔴⋯𝐁𝐎𝐓 𝐎𝐅𝐅𝐋𝐈𝐍𝐄⋯🔴",
            description=f"𝐁𝐎𝐓 𝐇𝐀𝐒 𝐆𝐎𝐍𝐄 𝐎𝐅𝐅𝐋𝐈𝐍𝐄.",
            color=discord.Color.red()
        )
        embed.set_author(name="", icon_url=logo_url)
        embed.set_thumbnail(url=logo_url)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Offline since : {datetime.datetime.now(bangkok_timezone).strftime('%a %d %b %Y, %I:%M%p')}", icon_url=logo_url)

        # Send embed to the offline message channel
        await offline_message_channel.send(embed=embed)
    else:
        print(f"Could not find the channel with ID {offline_message_channel_id}.")

@bot.event
async def on_member_join(member):
    global join_count
    join_count += 1

    welcome_channel_id = 891022262575194142  # Replace with your channel ID
    welcome_channel = bot.get_channel(welcome_channel_id)

    if welcome_channel is not None:
        logo_url = ''  # Replace with your actual logo URL
        gif_url = ''  # Replace with your actual GIF URL

        embed = discord.Embed(
            title="",
            description=(
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{join_count}"
            ),
            color=discord.Color.green()
        )
        embed.set_author(name="", icon_url=logo_url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="", value="", inline=False)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Joined from server on : {datetime.datetime.now(bangkok_timezone).strftime('%a %d %b %Y, %I:%M%p')}", icon_url=logo_url)

        await welcome_channel.send(embed=embed)

        try:
            await member.send(f"{member.mention} ")
        except discord.Forbidden:
            print(f"Failed to send DM to {member} (Forbidden)")
        except Exception as e:
            print(f"An error occurred while sending DM to {member}: {e}")

        # Assign role based on tenure in seconds
        await assign_role(member)

@bot.event
async def on_member_remove(member):
    global leave_count
    leave_count += 1

    leave_channel_id = 1248696084599930940  # Replace with your channel ID
    leave_channel = bot.get_channel(leave_channel_id)

    if leave_channel is not None:
        logo_url = ''  # Replace with your actual logo URL
        gif_url = ''  # Replace with your actual GIF URL

        embed = discord.Embed(
            title="",
            description=(
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{member.mention}\n"
                f"{leave_count}"
            ),
            color=discord.Color.red()
        )
        embed.set_author(name="", icon_url=logo_url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="", value="", inline=False)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Left the server on : {datetime.datetime.now(bangkok_timezone).strftime('%a %d %b %Y, %I:%M%p')}", icon_url=logo_url)

        await leave_channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

async def assign_role(member):
    member_tenure_seconds = (datetime.datetime.now(datetime.timezone.utc) - member.joined_at).total_seconds()
    assigned_role = None

    for role_name, threshold_seconds in role_ids.items():
        if member_tenure_seconds >= threshold_seconds:
            assigned_role = role_name

    if assigned_role is not None:
        role = discord.utils.get(member.guild.roles, id=role_ids[assigned_role])
        if role:
            try:
                await member.add_roles(role)
                print(f"Assigned {role.name} role to {member.display_name}")
            except discord.Forbidden:
                print(f"Failed to assign role {role.name} to {member} (Forbidden)")
            except discord.HTTPException:
                print(f"Failed to assign role {role.name} to {member} (HTTPException)")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='status')
async def status(ctx, mode: str):
    if mode.lower() == 'twitch':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Twitch!"))

@tasks.loop(minutes=5)  # (Adjust the interval as needed)
async def ping_server_task():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(PING_URL) as response:
                if response.status == 200:
                    print('Ping successful')
                else:
                    print(f'Ping failed with status code {response.status}')
        except aiohttp.ClientError as e:
            print(f'Ping failed with error: {e}')

bot.run(TOKEN)
