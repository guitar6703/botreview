import discord
from discord.ext import commands
from discord import app_commands
import json

# โหลดการตั้งค่าจากไฟล์ settings.json
with open('settings.json', 'r') as f:
    config = json.load(f)

TOKEN = config['TOKEN']
REVIEW_CHANNEL_ID = config['REVIEW_CHANNEL_ID']
SETUP_CHANNEL_ID = config['SETUP_CHANNEL_ID']
SETUP_IMAGE_URL = config['SETUP_IMAGE_URL']

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class ReviewButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="เขียนรีวิว", style=discord.ButtonStyle.primary)
    async def review_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ReviewModal()
        await interaction.response.send_modal(modal)

class ReviewModal(discord.ui.Modal, title="กรอกรีวิวของคุณ"):
    review = discord.ui.TextInput(label="รีวิว", style=discord.TextStyle.paragraph, placeholder="พิมพ์รีวิวของคุณที่นี่...")

    async def on_submit(self, interaction: discord.Interaction):
        review_channel = interaction.guild.get_channel(REVIEW_CHANNEL_ID)
        if review_channel:
            embed = discord.Embed(title="Drexm Credit", description=f"```+1 {self.review.value}```", color=discord.Color.purple())
            embed.set_footer(text=f"Review By {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            await review_channel.send(embed=embed)
            await interaction.response.send_message("✅ รีวิวของคุณถูกส่งเรียบร้อยแล้ว!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ ไม่สามารถส่งรีวิวได้ เนื่องจากไม่พบห้องที่กำหนด", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="drexmvaloshop.xyz/"))
    print(f'บอท {bot.user} ออนไลน์แล้ว!')

@bot.command()
async def review(ctx):
    view = ReviewButton()
    await ctx.send("คลิกเพื่อเขียนรีวิว", view=view)

@bot.command()
async def setup(ctx):
    if ctx.channel.id == SETUP_CHANNEL_ID:
        view = ReviewButton()
        embed = discord.Embed(title="! Review System", description="กรุณากดปุ่มด้านล่างเพื่อเขียนรีวิวของคุณ", color=discord.Color.purple())
        embed.set_image(url=SETUP_IMAGE_URL)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("❌ คุณไม่สามารถใช้คำสั่งนี้ในห้องนี้ได้")

bot.run(TOKEN)