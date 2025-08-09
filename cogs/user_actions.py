from discord.ext import commands
from discord import app_commands, SelectOption
from utils.database import *
from datetime import datetime, timedelta, timezone
from ui.views import *

import psycopg2
import discord


JOBS_NAMES = {
    "courier": "🚶 Курьер",
    "cleaner": "🧹 Уборщик",
    "fastfood": "🍔 Работник фастфуда",
    "loader": "📦 Грузчик",

    "artist": "🎨 Художник",
    "writer": "✍️ Писатель",
    "mechanic": "🔧 Механик",
    "programmer": "💻 Программист",
    "blogger": "📹 Видеоблогер",
}


class UserActions(commands.Cog):
    @app_commands.command(name="start", description="Начать зарабатывать")
    @app_commands.checks.has_permissions(send_messages=True)
    async def start(self, interaction: discord.Interaction):
        cursor.execute("SELECT 1 FROM users WHERE id = %s", (interaction.user.id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (id, balance) VALUES (%s, %s)", (interaction.user.id, 0,))
            await interaction.response.send_message("Вы создали трудовую книгу. Теперь вы можете устроиться на работу и получать деньги", ephemeral=True)
        else:
            await interaction.response.send_message("У вас уже есть трудовая книга!", ephemeral=True)

        conn.commit()


    @app_commands.command(name="balance", description="Узнать свой баланс")
    @app_commands.checks.has_permissions(send_messages=True)
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Ваш баланс составляет: {get_balance(interaction.user.id)}", ephemeral=True)


    @app_commands.command(name="job", description="Узнать информацию о вашей работе")
    @app_commands.checks.has_permissions(send_messages=True)
    async def job(self, interaction: discord.Interaction):
        if get_job(interaction.user.id) is None:
            await interaction.response.send_message("Вы безработный!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Ваша нынешняя работа: {JOBS_NAMES[get_job(interaction.user.id)]}", ephemeral=True)


    @app_commands.command(name="dismiss", description="Уволиться с работы")
    @app_commands.checks.has_permissions(send_messages=True)
    async def dismiss(self, interaction: discord.Interaction):
        async def dismiss_callback(interaction: discord.Interaction, options, prof):
            await interaction.response.edit_message(content="Вы уволились! Теперь вы безработный", view=None)
            set_job(interaction.user.id, None)

        await interaction.response.send_message(content="Вы действительно хотите уволиться?", view=ButtonView("Уволиться", [], "", dismiss_callback, discord.ButtonStyle.danger), ephemeral=True)


    @app_commands.command(name="balance", description="Узнать свой баланс")
    @app_commands.checks.has_permissions(send_messages=True)
    async def balance(self, interaction: discord.Interaction):
        try:
            word = plural(str(get_balance(interaction.user.id)).split(".")[0], ["долла́р", "долла́ра", "долла́ров"])
            if get_balance(interaction.user.id) < 1000000:
                await interaction.response.send_message(f"Ваш баланс составляет: {get_balance(interaction.user.id)} {word}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Баланс пользователя {interaction.user.mention} составляет {get_balance(interaction.user.id)} {word}")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(UserActions(bot))



def plural(n, forms):
    n = abs(int(n)) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return forms[2]
    if 1 == n1:
        return forms[0]
    if 2 <= n1 <= 4:
        return forms[1]
    return forms[2]