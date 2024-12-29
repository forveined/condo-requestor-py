import discord
from discord import app_commands
from roblox import RobloxAPI
from discord.ext import commands
import os
from dotenv import load_dotenv

# NOTE THIS A SHITTY REQUESTOR YOU NEED A UNBLACKLISTER FOR 1 FOR 2 A BASIC KEY SYSTEM AND MORE USE THIS AS A BASE STARTING POINT.


'''

made by @forveined | discord.gg/baller | ball.lgbt


'''

print("condo requestor made by forveined")

load_dotenv()
roblox_api = RobloxAPI()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.tree.command(name="upload", description="example condo requestor")
async def upload(interaction: discord.Interaction, cookie: str):
    await interaction.response.defer(ephemeral=True)
    try:
        csrf_token = await roblox_api.get_csrf_token(cookie)
        if not csrf_token: return await interaction.followup.send("Failed to get CSRF token")
        universe_data = await roblox_api.create_universe(cookie, csrf_token)
        if not universe_data: return await interaction.followup.send("Failed to create universe")
        if not await roblox_api.activate_universe(universe_data["universeId"], csrf_token, cookie): 
            return await interaction.followup.send("Failed to activate universe")
        result = await roblox_api.upload_game(universe_data["universeId"], universe_data["rootPlaceId"], 
                                            open("game.rbxl", "rb").read(), csrf_token, cookie)
        await interaction.followup.send(f"Game uploaded! URL: https://www.roblox.com/games/{universe_data['rootPlaceId']}" 
                                      if result else "Failed to upload game")
    except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.event
async def on_ready(): print(f'{bot.user} is online!'); await bot.tree.sync()

bot.run(os.getenv('token')) # PLEASE FOR FUCKS SAKE USE .ENV