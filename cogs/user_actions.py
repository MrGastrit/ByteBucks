from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta, timezone
from utils.database import *
from ui.views import *
from jobs_events import *

import psycopg2
import discord

import random
import math


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

    @app_commands.command(name="daily", description="Ежедневная награда")
    @app_commands.checks.has_permissions(send_messages=True)
    async def daily(self, interaction: discord.Interaction):
        cursor.execute("SELECT 1 FROM users WHERE id = %s", (interaction.user.id,))
        result = cursor.fetchone()

        if result:
            row = get_daily_time(interaction.user.id)

            now = datetime.now(timezone.utc)

            if row is None or row[0] is None:
                next_daily = now + timedelta(days=1)
                set_daily_time(interaction.user.id, next_daily)
                set_balance(interaction.user.id, get_balance(interaction.user.id) + 100)

                await interaction.response.send_message(embed=discord.Embed(title="", description=f"{interaction.user.mention} получил ежедневную награду!"))
            else:
                next_daily = row[0]
                if now >= next_daily:
                    next_daily = now + timedelta(days=1)
                    set_daily_time(interaction.user.id, next_daily)
                    set_balance(interaction.user.id, get_balance(interaction.user.id) + 100)

                    await interaction.response.send_message(embed=discord.Embed(title="", description=f"{interaction.user.mention} получил ежедневную награду!"))

                else:
                    remaining = next_daily - now
                    await interaction.response.send_message(
                        f"Время еще не пришло! До получения награды осталось: {str(remaining).split(".")[0]}",
                        ephemeral=True)

        else:
            await interaction.response.send_message("У вас нет трудовой книги, вы не можете получать деньги", ephemeral=True)

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
        word = plural(str(get_balance(interaction.user.id)).split(".")[0], words)
        if get_balance(interaction.user.id) < 1000000:
            await interaction.response.send_message(f"Ваш баланс составляет: {get_balance(interaction.user.id)} {word}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Баланс пользователя {interaction.user.mention} составляет {get_balance(interaction.user.id)} {word}")

    @app_commands.command(name="startwork", description="Начать работу")
    @app_commands.checks.has_permissions(send_messages=True)
    async def startwork(self, interaction: discord.Interaction):
        if is_on_work(interaction.user.id):
            await interaction.response.send_message("Вы уже на работе!", ephemeral=True)
        else:
            await interaction.response.send_message("Вы вышли на работу!", ephemeral=True)
            set_on_work(interaction.user.id, True)
            set_start_work(interaction.user.id, datetime.now())
            set_next_payment(interaction.user.id, datetime.now() + timedelta(hours=1))

    @app_commands.command(name="payment", description="Получить зарплату")
    @app_commands.checks.has_permissions(send_messages=True)
    async def payment(self, interaction: discord.Interaction):
        if is_on_work(interaction.user.id):
            def check_payment(user_id):
                now = datetime.now()
                max_iterations = 12
                iterations = 0

                job = get_job(user_id)
                base_salary = JOBS_SALARIES.get(job, 0)
                salary_per_hour, event = job_event(job, base_salary)

                current_balance = get_balance(user_id)
                next_payment = get_next_payment(user_id)

                total_salary = 0

                while now >= next_payment and iterations < max_iterations:
                    total_salary += salary_per_hour
                    next_payment += timedelta(hours=1)
                    iterations += 1

                if total_salary > 0:
                    set_balance(user_id, current_balance + total_salary)
                    set_next_payment(user_id, next_payment)

                return event, total_salary

            event, total_salary = check_payment(interaction.user.id)

            if total_salary > 0:
                await interaction.response.send_message(f"{event}\nЗа эту смену ты заработал {total_salary} {plural(total_salary, words)}", ephemeral=True)
            else:
                await interaction.response.send_message("Пока еще рано получать зарплату, подождите немного.", ephemeral=True)
        else:
            await interaction.response.send_message("За что вам платить? Ты даже на работу не выходил!", ephemeral=True)

    @app_commands.command(name="endwork", description="Закончить работу")
    @app_commands.checks.has_permissions(send_messages=True)
    async def endwork(self, interaction: discord.Interaction):
        if is_on_work(interaction.user.id):
            await interaction.response.send_message("Вы ушли с работы!", ephemeral=True)
        else:
            await interaction.response.send_message("Вы итак не на работе!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UserActions(bot))
