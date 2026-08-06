import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import random
import string
import json

TOKEN = "SEU_TOKEN_DO_BOT"
ADMIN_TOKEN = "sistemak-admin-2026"
API_URL = "https://sistemak.contaxuxu07.workers.dev"
ADMIN_IDS = [SEU_ID_DISCORD]  # seu ID numérico do Discord

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def gerar_key():
    partes = [''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)]
    return "POLARZ-" + "-".join(partes)

async def api_post(endpoint, body):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/{endpoint}",
            headers={
                "Authorization": f"Bearer {ADMIN_TOKEN}",
                "Content-Type": "application/json"
            },
            data=json.dumps(body)
        ) as resp:
            return await resp.json()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

@bot.tree.command(name="addkey", description="Gera uma key para um usuário")
@app_commands.describe(usuario="Usuário do Discord", dias="Dias de validade")
async def addkey(interaction: discord.Interaction, usuario: discord.Member, dias: int = 30):
    if interaction.user.id not in ADMIN_IDS:
        await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    key = gerar_key()
    result = await api_post("addkey", {
        "key": key,
        "user": str(usuario.id),
        "days": dias
    })

    if result.get("success"):
        # Manda DM pro usuário
        try:
            embed = discord.Embed(
                title="🔑 Sua key do Polarz Optimizer",
                color=0xE02040
            )
            embed.add_field(name="Key", value=f"```{key}```", inline=False)
            embed.add_field(name="Validade", value=f"{dias} dias", inline=True)
            embed.add_field(name="HWID Lock", value="Ativado na primeira vez", inline=True)
            embed.set_footer(text="Não compartilhe sua key.")
            await usuario.send(embed=embed)
            await interaction.followup.send(f"✅ Key gerada e enviada no DM de {usuario.mention}!", ephemeral=True)
        except:
            await interaction.followup.send(f"✅ Key gerada: `{key}`\n⚠️ Não consegui enviar DM para {usuario.mention}.", ephemeral=True)
    else:
        await interaction.followup.send(f"❌ Erro: {result}", ephemeral=True)

@bot.tree.command(name="removekey", description="Remove a key de um usuário")
@app_commands.describe(key="Key a remover")
async def removekey(interaction: discord.Interaction, key: str):
    if interaction.user.id not in ADMIN_IDS:
        await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    result = await api_post("removekey", {"key": key})

    if result.get("success"):
        await interaction.followup.send(f"✅ Key `{key}` removida.", ephemeral=True)
    else:
        await interaction.followup.send(f"❌ Erro: {result}", ephemeral=True)

@bot.tree.command(name="resethwid", description="Reseta o HWID de uma key")
@app_commands.describe(key="Key para resetar HWID")
async def resethwid(interaction: discord.Interaction, key: str):
    if interaction.user.id not in ADMIN_IDS:
        await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    result = await api_post("resetHWID", {"key": key})

    if result.get("success"):
        await interaction.followup.send(f"✅ HWID da key `{key}` resetado.", ephemeral=True)
    else:
        await interaction.followup.send(f"❌ Erro: {result}", ephemeral=True)

bot.run(TOKEN)
